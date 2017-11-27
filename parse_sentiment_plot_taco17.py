# Sentiment Analysis Using the Movie Ratings Data (Python)

# prepare for Python version 3x features and functions
from __future__ import division, print_function

# import packages for text processing and machine learning
import os  # operating system commands
import re  # regular expressions
import nltk  # draw on the Python natural language toolkit
import pandas as pd  # DataFrame structure and operations
import matplotlib.pyplot as plt  # 2D plotting

# list files in directory omitting hidden files
def listdir_no_hidden(path):
    start_list = os.listdir(path)
    end_list = []
    for file in start_list:
        if (not file.startswith('.')):
            end_list.append(file)
    return(end_list)            
            

# define list of codes to be dropped from document
# carriage-returns, line-feeds, tabs
codelist = ['\r', '\n', '\t']    

# there are certain words we will ignore in subsequent
# text processing... these are called stop-words 
# and they consist of prepositions, pronouns, and 
# conjunctions, interrogatives, ...
# we begin with the list from the natural language toolkit
# examine this initial list of stopwords
nltk.download('stopwords')

# let's look at that list 
# print(nltk.corpus.stopwords.words('english'))

# previous analysis of a list of top terms showed a number of words, along 
# with contractions and other word strings to drop from further analysis, we add
# these to the usual English stopwords to be dropped from a document collection
more_stop_words = ['cant','didnt','doesnt','dont','goes','isnt','hes',\
    'shes','thats','theres','theyre','wont','youll','youre','youve', 'br'\
    've', 're', 'vs'] 

# start with the initial list and add to it for movie text work 
stoplist = nltk.corpus.stopwords.words('english') + more_stop_words

# text parsing function for creating text documents 
# there is more we could do for data preparation 
# stemming... looking for contractions... possessives... 
# but we will work with what we have in this parsing function
# if we want to do stemming at a later time, we can use
#     porter = nltk.PorterStemmer()  
# in a construction like this
#     words_stemmed =  [porter.stem(word) for word in initial_words]  
def text_parse(string):
    # replace non-alphanumeric with space 
    temp_string = re.sub('[^a-zA-Z]', '  ', string)    
    # replace codes with space
    for i in range(len(codelist)):
        stopstring = ' ' + codelist[i] + '  '
        temp_string = re.sub(stopstring, '  ', temp_string)      
    # replace single-character words with space
    temp_string = re.sub('\s.\s', ' ', temp_string)   
    # convert uppercase to lowercase
    temp_string = temp_string.lower()    
    # replace selected character strings/stop-words with space
    for i in range(len(stoplist)):
        stopstring = ' ' + str(stoplist[i]) + ' '
        temp_string = re.sub(stopstring, ' ', temp_string)        
    # replace multiple blank characters with one blank character
    temp_string = re.sub('\s+', ' ', temp_string)    
    return(temp_string)    

os.listdir(".")
os.chdir("C:/projectFall17/TeamRed_final/")

# read in positive and negative word lists from Hu and Liu (2004)
with open('ref_files/Hu_Liu_positive_word_list.txt','rt') as f:
    positive_word_list = f.read().split() 
with open('ref_files/Hu_Liu_negative_word_list.txt','rt') as f:
    negative_word_list = f.read().split()   
    
# define counts of positive, negative, and total words in text document 
def count_positive(text):    
    positive = [w for w in text.split() if w in positive_word_list]
    return(len(positive))

# define text measure for negative score as percentage of negative words   
def count_negative(text):    
    negative = [w for w in text.split() if w in negative_word_list]
    return(len(negative))
    
# count number of words   
def count_total(text):    
    total = [w for w in text.split()]
    return(len(total))    

# define text measure for positive score as percentage of positive words    
def score_positive(text):    
    positive = [w for w in text.split() if w in positive_word_list]
    total = [w for w in text.split()]
    if len(total) > 0:
        return 100 * len(positive)/len(total)
    else:
        return 0

# define text measure for negative score as percentage of negative words   
def score_negative(text):    
    negative = [w for w in text.split() if w in negative_word_list]
    total = [w for w in text.split()]
    if len(total) > 0:
        return 100 * len(negative)/len(total)
    else:
        return 0

def compute_scores(corpus):
    # use the complete word lists for POSITIVE and NEGATIVE measures
    # to score all documents in a corpus or list of documents
    positive = []
    negative = []
    days = []
    count = 0
    for document in corpus:
        positive.append(score_positive(document)) 
        negative.append(score_negative(document))
        days.append(count)
        count = count+1
    return(positive, negative, days)
                           
# we use movie ratings data from Mass et al. (2011) 
# available at http://ai.stanford.edu/~amaas/data/sentiment/

# function for creating corpus and aggregate document 
# input is directory path for documents
# document parsing accomplished by text_parse function
# directory of parsed files set up for manual inspection
def corpus_creator (input_directory_path, output_directory_path):
    # identify the file names in unsup directory
    file_names = listdir_no_hidden(path = input_directory_path)
    # create list structure for storing parsed documents 
    document_collection = [] 
    # initialize aggregate document for all documents in set
    aggregate_document = ''
    # create a directory for parsed files 
    parsed_file_directory = output_directory_path
    os.mkdir(parsed_file_directory)
    # parse each file and write to directory of parsed files
    for filename in file_names:
        with open(os.path.join(input_directory_path, filename), 'r') as infile:        
            this_document = text_parse(infile.read())
            aggregate_document = aggregate_document + this_document
            document_collection.append(this_document)
            outfile = parsed_file_directory + filename
            with open(outfile, 'wt') as f:
                f.write(str(this_document)) 
    aggregate_words = [w for w in aggregate_document.split()]   
    aggregate_corpus = nltk.Text(aggregate_words)    
    return(file_names, document_collection, aggregate_corpus)
    
    
# begin working with the unsup corpus
unsup_file_names, unsup_corpus, unsup_aggregate_corpus = \
    corpus_creator(input_directory_path = 'input_raw_data/twitter_taco_17/',\
        output_directory_path = 'output_parsed_data/taco_17_v4/')
                    
# examine frequency distribution of words in unsup corpus
unsup_freq = nltk.FreqDist(unsup_corpus)
print('\nNumber of Unique Words in unsup corpus',len(unsup_freq.keys()))
# Number of Unique Words in unsup corpus 12518
# print('\nTop Fifty Words in unsup Corpus:',unsup_freq.keys()[0:50])

#initial_words = unsup_aggregate_corpus
# stemming... looking for contractions... possessives... 
porter = nltk.PorterStemmer()  
# and make it a unique list
words_stemmed = [porter.stem(word) for word in unsup_corpus] 

 
# examine frequency distribution of words in unsup corpus
unsup_freq = nltk.FreqDist(unsup_aggregate_corpus)
print('\nNumber of Unique Words in unsup aggregate corpus',len(unsup_freq.keys()))
# Number of Unique Words in unsup corpus 93000
print('\nTop Fifty Words in unsup aggregate Corpus:',unsup_freq.keys()[0:50])
  

# identify the most frequent unsup words from the positive word list
# here we use set intersection to find a list of the top 25 positive words 
length_test = 0  # initialize test length
nkeys = 0  # slicing index for frequency table extent
while (length_test < 25):
    length_test =\
        len(set(unsup_freq.keys()[:nkeys]) & set(positive_word_list))
    nkeys = nkeys + 1
print(nkeys)
# nkeys reached to 1353 to get 25 positive words; 
selected_positive_set =\
    set(unsup_freq.keys()[:nkeys]) & set(positive_word_list)
selected_positive_words = list(selected_positive_set)
selected_positive_words.sort()
print('\nSelected Positive Words:', selected_positive_words)
print(len(selected_positive_words))

# identify the most frequent unsup words from the negative word list
# here we use set intersection to find a list of the top 25 negative words 
length_test = 0  # initialize test length
nkeys = 0 # slicing index for frequency table extent
while (length_test < 25):
    length_test =\
        len(set(unsup_freq.keys()[:nkeys]) & set(negative_word_list))
    nkeys = nkeys + 1
print(nkeys)
# nkeys is 1121 to get 25 negative words
selected_negative_set =\
    set(unsup_freq.keys()[:nkeys]) & set(negative_word_list)
# list is actually 25 items 
selected_negative_words = list(selected_negative_set)
selected_negative_words.sort()
print('\nSelected Negative Words:', selected_negative_words)
print(len(selected_negative_words))

# use the complete word lists for POSITIVE and NEGATIVE measures/scores

positive, negative, days = compute_scores(unsup_corpus)

# create data frame to explore POSITIVE and NEGATIVE measures
unsup_data = {'POSITIVE': positive, 'NEGATIVE': negative}    
# unsup_data = {'file': unsup_file_names,\
#    'POSITIVE': positive, 'NEGATIVE': negative} 
# pd.DataFrame({'A': a, 'B': b}, index=[0])   
# not working with index=[0]
# unsup_data_frame = pd.DataFrame(unsup_data, index=[0])
unsup_data_frame = pd.DataFrame(unsup_data)

# summary of distributions of POSITIVE and NEGATIVE scores for unsup corpus
print(unsup_data_frame.describe())

# -----------------------results looks reasonable
print('\nCorrelation between POSITIVE and NEGATIVE',\
    round(unsup_data_frame['POSITIVE'].corr(unsup_data_frame['NEGATIVE']),3))

# scatter plot of POSITIVE and NEGATIVE scores for unsup_aggregate_corpus2
ax = plt.axes()
ax.scatter(unsup_data_frame['NEGATIVE'], unsup_data_frame['POSITIVE'],\
    facecolors = 'none', edgecolors = 'blue')
ax.set_xlabel('NEGATIVE')
ax.set_ylabel('POSITIVE')   
plt.savefig('fig_sentiment_text_measures_scatter_plot_taco17.pdf', 
    bbox_inches = 'tight', dpi=None, facecolor='none', edgecolor='blue', 
    orientation='portrait', papertype=None, format=None, 
    transparent=True, pad_inches=0.25, frameon=None)  

plt.figure()
t = days
s = positive
s2 = negative
plt.plot(t, s2, 'r-', t, s, 'b--')
plt.xlabel('days from 8/1/2017 - 10/31/2017 (Taco Bell)')
plt.ylabel('sentiment %, blue-positive, red-negative') 
plt.show()  
plt.savefig('fig_line_plot_taco17.pdf', 
    bbox_inches = 'tight', dpi=None, facecolor='none', edgecolor='blue', 
    orientation='portrait', papertype=None, format=None, 
    transparent=True, pad_inches=0.25, frameon=None) 
# Suggestions for the student:
# Employ stemming prior to the creation of terms-by-document matrices.
# Try alternative positive and negative word sets for sentiment scoring.
# Try word sets that relate to a wider variety of emotional or opinion states.
# Better still, move beyond a bag-of-words approach to sentiment. Use
# the tools of natural language processing and define text features
# based upon combinations of words such as bigrams (pairs of words)
# and taking note of parts of speech.  Yet another approach would be
# to define ignore negative and positive word lists and work directly 
# with identified text features that correlate with movie review ratings or
# do a good job of classifying reviews into positive and negative groups.
# Text features within text classification problems may be defined 
# on term document frequency alone or on measures of term document
# frequency adjusted by term corpus frequency. Using alternative 
# features and text measures as well as alternative classification methods,
# run a true benchmark within a loop, using hundreds or thousands of iterations.
# See if you can improve upon the performance of modeling methods by
# modifying the values of arguments to algorithms used here.
# Use various methods of classifier performance to evaluate classifiers.
# Try text classification for the movie reviews without using initial
# lists of positive an negative words. That is, identify text features
# for thumbs up/down text classification directly from the training set.


