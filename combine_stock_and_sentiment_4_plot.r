# prepare sentiment data
getwd()
#filename_a <- "taco2017.csv"
#filename_b <- "YUM_2017_price.csv"
#out_filename <- "taco2017_plot_data.csv"

path <- "C:/projectFall17/TeamRed_final2"
filename_a <- file.path(path, "sentiment_4_files/chipotle2017.csv")
filename_b <- file.path(path, "stock_data_4_files/CMG_2017_price.csv")
out_filename <- file.path(path, 
                          "plot_data_4_files/chipotle2017_plot_data.csv")
path_a <- file.path(filename_a)
a <- read.csv(path_a)
head(a)
a_date <- ymd(a$Date)  # convert charactor to date
c1 <- subset(a, select = c(1,5,6))  # select scores
head(c1)
# bring date column into dataframe and make sure
# dates matches
df_a <- data.frame(date=a_date, c1)
head(df_a)


path_b <- file.path(filename_b)
b <- read.csv(path_b)
head(b)
b_date <- ymd(b$Date)
b_date
# select close price as stock price
c2<- subset(b, select = c(1,5))
head(c2)
# add date column and bring into dataframe b
df_b <- data.frame(date2=b_date, c2) 
head(df_b)

# merge the two datasets, note stock price missing on weekends
m<- merge(df_a, df_b, 
          by.x="date", 
          by.y ="date2", all.x = T )
head(m)
# drop extra date columns
df_m <- subset(m, select = c(1, 3, 4, 6))
head(df_m)
# process NA Close price, make it as mean
# is.na(df_m$Close)
# df_m$Close[is.na(df_m$Close)] <- mean(df_m$Close, na.rm = T)
# rename headings
colnames(df_m) <- c("Date", "positive_score", 
                    "negative_score","stock_price")
head(df_m)
# save to combined csv file
out_filename
write.csv(df_m, out_filename, row.names = F)
