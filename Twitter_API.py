from urllib.parse import urlencode
import oauth2
import json

#API Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
TOKEN_KEY = ''
TOKEN_SECRET = ''

#Make an API Call with OAuth Authenthication

def oauth_req(url, http_method="GET", post_body=b"", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=TOKEN_KEY, secret=TOKEN_SECRET)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

#Create the search url (contains the query and the number of tweets to get)
def create_search_url(q, count):
    parameters = {
        'q': q,
        'count': count
        }
    url = 'https://api.twitter.com/1.1/search/tweets.json?'
    final_url = url + urlencode(parameters)
    return final_url

#Make the API Call and get the  response back
def get_search_response(search_string, count):
    url = create_search_url(search_string, count)
    response = oauth_req(url)
    response = response.decode('utf-8')
    return response

#Full content of tweets to a file
def write_full_content_to_file(tweet, file_name):
    with open(file_name, 'wt', encoding = 'utf8') as out:
        out.write(json.dumps(tweet['statuses'], indent = 2))

#Write the text of tweets to a file.  Has Tweet id and text
def write_text_to_file(tweet, file_name):
    tweets = tweet['statuses']
    tweets_texts = []
    for tweet in tweets:
        tweets_texts.append({
            'id': tweet['id'],
            'text': tweet['text']
            })
    with open(file_name, 'wt', encoding = 'utf8') as out:
        out.write(json.dumps(tweets_texts, indent = 2))

#Main - get the search string, get the count, get the results and write the results to files
if __name__ == '__main__':
    search_string = input('Please enter the search string: ')
    count = -1
    while count < 1 or count > 100:
        count = eval(input('Please enter the number of tweets to get(1 - 100): '))
        if count < 1 or count > 100:
            print('Please enter a number between 1 and 100')
    #Get the results
    search_results = get_search_response(search_string, count)

    #Conver the results to json
    search_results_json = json.loads(search_results)

    #Write full tweets to full_tweets.txt file
    write_full_content_to_file(search_results_json, 'full_tweets.txt')

    #Write tweets texts to tweets_texts.txt file
    write_text_to_file(search_results_json, 'tweets_texts.txt')
