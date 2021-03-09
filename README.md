# YouTube_data_extractor

Python script for scrapping YouTube video data given url of the videos.

Libraries modules:
```
- selenium
- pandas 
```

`!pip install selenium`

#How to use.

Here is the code in `query.py` file. Replace your topic (gate 2020) for which you want to extract data and specify no of videos.(here 501)
It will go to the YouTube, search for that query and extract data for the first 501 videos.

```python
query = 'gate 2020'           #enter your query for which you want to scrap videos
no_of_videos = 501            #enter number of videos you want to scrap.
```

## Input: 

Query and number of videos for which you want to scrap data.

## Output: 
csv file containing url, Timestamp, Title, Views, upload_date, Likes, Dislikes and Comments.

- Timestamp: Date and time at which data is extracted

Here I have extracted data for 501 videos for Query - 'gate 2020' and provided in the .csv file.

## NOTE: Comments extraction from different urls takes time. 
## Time taken to complete and number of videos you want to scrap have positive coorelation ..:slightly_smiling_face:


# Go Ahead try yourself and contribute to <a href= 'https://www.kaggle.com/gaurav2022/youtube-scrapped-data'>kaggle dataset</a>

Connect with me:

<a href= 'https://www.linkedin.com/in/gaurav2022'>Linkedin</a>

<a href= 'https://www.kaggle.com/gaurav2022'>Kaggle</a>
