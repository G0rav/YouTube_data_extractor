"""
Python script for scrapping YouTube video data given url of the videos.

Input: Query and number of videos for which you want to scrap data.

Output: csv file containing url, Timestamp, Title, Views, upload_date, Likes, Dislikes and Comments.

"""
#!pip install selenium          #To install selenium remove #

#importing necessary libraries
from selenium import webdriver
import time
from datetime import datetime
import pandas as pd

drivepath = "C:\chromedriver\chromedriver.exe"           #path of chromedriver

#setting chrome options for using chrome without opening chrome 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('incognito')

driver = webdriver.Chrome(drivepath,options=chrome_options)

query = 'gate 2020'           #enter your query for which you want to scrap videos
no_of_videos = 501            #enter number of videos you want to scrap.

driver.get('https://www.youtube.com/results?search_query='+query)
print('You quered for:',driver.title)

#loop for extracting first n links for the query appeared on YouTube search
while True:
    driver.execute_script("window.scrollTo(0, window.scrollY + 5000);")
    tn = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
    links = []
    for i in tn:
        links.append(i.get_attribute('href'))
    len(links)
    if len(links)> no_of_videos + 10:           #i have set the limit 10 more than req. for safety
        break


Links = links[1:no_of_videos+1]          
print('Total scrapped links are:',len(links))


#function to return video data except comments (comments extraction takes time so make seperate function)

def Scrap(url):                      
    
    """ Just pass the url of the youtube video you want to scrap data for except comments.

        input: url of the video

        return: Dictionary containing url,
                              timestamp at which it is extracted, 
                              title of the video,
                              views on the video,
                              upload date,
                              likes and dislikes.
   """
    
    
    dct = {}
  
    dct['url'] = url
 
    Timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")           #Time at which url is extracted
    dct['Timestamp'] = Timestamp
 
    driver.get(url)
    time.sleep(2)
    
    try:
        title =  driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
        Title = title.text
        dct['Title'] = Title
    except:
        dct['Title'] = ''
 
    try:
        views =  driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer')
        Views = views.text
        dct['Views'] = Views
    except:
        dct['Views'] = ''
 
    try:
        date =  driver.find_element_by_xpath('//*[@id="date"]/yt-formatted-string')
        upload_date = date.text
        dct['upload_date'] = upload_date
    except:
        dct['upload_date'] = ''
 
    try:
        likes =  driver.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a')
        Likes = likes.text
        dct['Likes'] = Likes
    except:
        dct['Likes'] = ''
 
    try:
        dislikes =  driver.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]/a')
        Dislikes = dislikes.text
        dct['Dislikes'] = Dislikes
    except:
        dct['Dislikes'] = ''
 
 
    return dct


#print(Scrap('https://youtu.be/XhZ1w3saRiI'))          #for testing purpose remove # to see output


#function to return video data except comments (comments extraction takes time so make seperate function)

def comments(url):
    
    
    """ Just pass the url of the youtube video you want to scrap comments for.

        input: url of the video.

        return: Dictionary containing url and comments on the video seperated by ' || 
    '"""

    dct = {}
  
    driver.get(url)  
    time.sleep(2)           #wait 2 sec for the html to load
   
    dct['url'] = url

    driver.execute_script("window.scrollTo(0, window.scrollY + 50000);")
    comments =  driver.find_element_by_xpath('//*[@id="comments"]')
    driver.execute_script("arguments[0].scrollIntoView();", comments)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

#loop to load all comments on the webpage 

    while True:
       
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        
        time.sleep(2)          #wait 2 sec for the html to load
 
        new_height = driver.execute_script("return document.documentElement.scrollHeight")          # Calculate new scroll height and compare with last scroll height.
        if new_height == last_height:
            break
        last_height = new_height

    try:
        username = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except:
        username = []
        comment = []

    Comments = []
    for user, comment in zip(username, comment):
        Comments.append("{} - {}".format(user.text,comment.text))

    All_comments = ' || '.join(Comments)          #converting list of comments to a single string seperated by ' || '
    dct['Comments'] = All_comments
 
    return dct


#print(comments('https://www.youtube.com/watch?v=ytCWVUmb0d0'))          #for testing purpose remove # to see output


#loop for scraping data except comments for 501 links
print('start scraping data loop...., will run 501 times.')
data = []
iter = 1
for i in Links[:501]:          #scraping 501 videos    
    try:
        dt = Scrap(i)
        display(dt)
        data.append(dt)
        print('completed - ',iter)
        iter = iter + 1
    except:
        print('error at- ',iter)
        iter = iter + 1
        pass


data_without_comments = pd.DataFrame(data)          #converting to dataframe
print('Dataframe containing data')
display(data_without_comments)


#loop for scraping comments for 501 links 
print('start scraping comments loop...., will run 501 times.')
com = []
iter = 1
for i in Links[:501]:          #scraping 501 videos
    try:
        dt = comments(i)
        com.append(dt)
        print(dt)
        print('comments completed - ',iter)
        iter = iter +1
    except:
        print('comments error - ',iter)
        iter = iter + 1
        pass


data_comments = pd.DataFrame(com)          #converting to dataframe
print('Dataframe containing comments')
display(data_comments)


#merge both the dataframes on common urls
df = data_without_comments.merge(data_comments, on = 'url', how = 'outer')
print('Final data')
display(df)

#making csv file of the whole data
df.to_csv('YouTube_data.csv', index= False)


""" Thanks have a great life ahead."""
