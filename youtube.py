import googleapiclient.discovery 
import pandas as pd
import mysql.connector
import streamlit as st
import re
from datetime import datetime 


api_service_name = "youtube"
api_version = "v3"
api_key = 'AIzaSyA6fl6k1Ahaa7d0mO--yCb59ttpcLKWD7c'
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


client = mysql.connector.connect(host = "localhost",
                                    user = "root",
                                    password = "Farshi@25",
                                    database = "Youtube_Data")
cursor = client.cursor()


with st.sidebar:
    st.title(":blue[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
    st.header("Skills Takeaway")
    st.caption("- Python scripting\n- Data Collection\n- Streamlit\n- API integration\n- Data Management using SQL")
    st.header("Domain")
    st.caption("Social Media")


channel_ID = st.text_input("Enter the channel ID: ")


def convert_duration(duration):
    regex = r'PT(\d+H)?(\d+M)?(\d+S)?'
    match = re.match(regex, duration)
    if not match:
        return '00:00:00'

    hours, minutes, seconds = match.groups()
    hours = int(hours[:-1]) if hours else 0
    minutes = int(minutes[:-1]) if minutes else 0
    seconds = int(seconds[:-1]) if seconds else 0

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def get_channel_data(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()
    data = {
            "channel_name":response['items'][0]['snippet']['title'],
            "channel_des":response['items'][0]['snippet']['description'],
            "channel_p_id":response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
            "channel_pat":(response['items'][0]['snippet']['publishedAt']).replace("T"," ").replace("Z",""),
            "channel_sub_count":response['items'][0]['statistics']['subscriberCount'],
            "channel_vcount":response['items'][0]['statistics']['viewCount'],
            "channel_vid_count":response['items'][0]['statistics']['videoCount'],
            "channel_id":response['items'][0]['id']
    }
    return data


def get_video_ids(channel_id):
    video_ids = []

    request = youtube.channels().list(
                                     part = "contentDetails",
                                     id = channel_id 
    )
    response = request.execute()
    platlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None

    while True:
        response1 = youtube.playlistItems().list(
            playlistId = platlist_id,
            part = "snippet",
            maxResults = 50,
            pageToken = next_page_token
        ).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = response1.get('nextPageToken')
        if next_page_token is None:
            break
    return video_ids



def get_video_data(video_Ids):
    video_data = []
    for video_id in video_Ids:
        request = youtube.videos().list(
                                    part="snippet,contentDetails,statistics",
                                    id=video_id
                                    )
        response1 = request.execute()
        data1 = {"channel_id":response1['items'][0]['snippet']['channelId'],
                "channel_name":response1['items'][0]['snippet']['channelTitle'],
                "video_id":response1['items'][0]['id'],
                "video_title":response1['items'][0]['snippet']['title'],
                "video_pat":(response1['items'][0]['snippet']['publishedAt']).replace("T"," ").replace("Z",""),
                "video_des":response1['items'][0]['snippet'].get('description'),
                "video_captionstatus":response1['items'][0]['contentDetails']['caption'],
                "video_def":response1['items'][0]['contentDetails']['definition'],
                "video_duration":convert_duration(response1['items'][0]['contentDetails']['duration']),
                "video_lc":response1['items'][0]['statistics'].get('likeCount'),
                "video_vc":response1['items'][0]['statistics']['viewCount'],
                "video_cc":response1['items'][0]['statistics'].get('commentCount'),
                "video_fc":response1['items'][0]['statistics']['favoriteCount']

            }
        video_data.append(data1)

    return video_data


def get_comment_data(video_Ids):
    comment_data = []
    try:
        for video_id in video_Ids:
            request = youtube.commentThreads().list(
                                                    part="snippet",
                                                    videoId=video_id,
                                                    maxResults = 50
                                                    )
            response = request.execute()
            data2 = {"comment_id":response['items'][0]['id'],
                    "video_id":response['items'][0]['snippet']['videoId'],
                    "comment_text":response['items'][0]['snippet']['topLevelComment']['snippet']['textDisplay'],
                    "comment_author":response['items'][0]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    "comment_pat":response['items'][0]['snippet']['topLevelComment']['snippet']['publishedAt']}
            comment_data.append(data2)
    except:
        pass
    return comment_data


if st.button("View Details"):
    extracted_details = get_channel_data(channel_id=channel_ID)
    st.write(":blue[Channel name]: ",extracted_details['channel_name'])
    st.write(":blue[Description]: ",extracted_details['channel_des'])
    st.write(":blue[Published At]: ",extracted_details['channel_pat'])
    st.write(":blue[Total videos]: ",extracted_details['channel_vid_count'])
    st.write(":blue[Subscriber's count]: ",extracted_details['channel_sub_count'])
    st.write(":blue[Total views]: ",extracted_details['channel_vcount'])



if st.button("Upload to MYSQL"): 
    Df_channel = pd.DataFrame(get_channel_data(channel_id = channel_ID),index=[0])
    video_Ids = get_video_ids(channel_id=channel_ID)
    Df_videos = pd.DataFrame(get_video_data(video_Ids))
    Df_comment = pd.DataFrame(get_comment_data(video_Ids))


    cursor.execute( """create table if not exists channel_details(channel_name varchar(255),
                                            channel_des text,
                                            channel_p_id varchar(255),
                                            channel_pat timestamp,
                                            channel_sub_count bigint,
                                            channel_vcount bigint,
                                            channel_vid_count bigint,
                                            channel_id varchar(255) primary key
                                            )""")
    
                

    cursor.execute("""create table if not exists video_details(channel_id varchar(255),
                                                        channel_name varchar(255),
                                                        video_id varchar(255) primary key,
                                                        video_title varchar(255),
                                                        video_pat timestamp,
                                                        video_des text,
                                                        video_captionstatus varchar(255),
                                                        video_def varchar(255),
                                                        video_duration varchar(10),
                                                        video_lc bigint,
                                                        video_vc bigint,
                                                        video_cc bigint,
                                                        video_fc int,
                                                        Foreign key (channel_id) references channel_details(channel_id)
                                                        )""")

    

    cursor.execute("""create table if not exists comment_details(comment_id varchar(255),
                                                        video_id varchar(255) ,
                                                        comment_text text,
                                                        comment_author varchar(255),
                                                        comment_pat varchar(255),
                                                        Foreign key (video_id) references video_details(video_id))""")



    query1 = """insert into channel_details values(%s,%s,%s,%s,%s,%s,%s,%s)"""
    values = [tuple(row) for row in Df_channel.values]
    cursor.executemany(query1,values)


    query2 = """insert into video_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    values = [tuple(row) for row in Df_videos.values]
    cursor.executemany(query2,values)


    query3 = """insert into comment_details values(%s,%s,%s,%s,%s)"""
    values = [tuple(row) for row in Df_comment.values]
    cursor.executemany(query3,values)
    client.commit()

    st.success("uploaded successfully")


Questions = st.selectbox("Select your question",("1. What are the names of all the videos and their corresponding channels?",
                                                 "2. Which channels have the most number of videos and how many videos do they have?",
                                                 "3. What are the top 10 most viewed videos and their respective channels?",
                                                 "4. How many comments were made on each video and what are their corresponding video names?",
                                                 "5. Which videos have the highest number of likes and what are their corresponding channel names?",
                                                 "6. What is the total number of likes for each video and what are their corresponding video names?",
                                                 "7. What is the total number of views for each channel and what are their corresponding channel names?",
                                                 "8. What are the names of all the channels that have published videos in the year 2022?",
                                                 "9. What is the average duration of all videos in each channel and what are their corresponding channel names?",
                                                 "10. Which videos have the highest number of comments and what are their corresponding channel names?"))


if Questions=="1. What are the names of all the videos and their corresponding channels?":
    query1= '''select video_title as videosnames, channel_name as channelname from video_details'''
    cursor.execute(query1)
    table1 = cursor.fetchall()
    df1 = pd.DataFrame(table1,columns=["Videos names","Channel name"])
    st.write(df1)


elif Questions=="2. Which channels have the most number of videos and how many videos do they have?":
    query2= '''select channel_vid_count as no_videos, channel_name as channelname from channel_details
               order by channel_vid_count desc'''
    cursor.execute(query2)
    table2 = cursor.fetchall()
    df2 = pd.DataFrame(table2,columns=["No. of videos","Channel name"])
    st.write(df2)


elif Questions=="3. What are the top 10 most viewed videos and their respective channels?":
    query3 = '''select video_vc as views,channel_name as channelname,video_title as title from video_details
                where video_vc is not null order by video_vc desc limit 10'''
    cursor.execute(query3)
    table3 = cursor.fetchall()
    df3 = pd.DataFrame(table3,columns=["Views","Channel name","Video title"])
    st.write(df3)


elif Questions=="4. How many comments were made on each video and what are their corresponding video names?":
    query4 = '''select video_cc as no_comments,video_title as title from video_details 
                where video_cc is not null'''
    cursor.execute(query4)
    table4 = cursor.fetchall()
    df4 = pd.DataFrame(table4,columns=["No. of comments","Video title"])
    st.write(df4)


elif Questions=="5. Which videos have the highest number of likes and what are their corresponding channel names?":
    query5 = '''select video_lc as likes, video_title as title, channel_name as channelname
                from video_details where video_lc is not null order by video_lc desc'''
    cursor.execute(query5)
    table5 = cursor.fetchall()
    df5 = pd.DataFrame(table5,columns=["No. of likes","Video title","Channel name"])
    st.write(df5)


elif Questions=="6. What is the total number of likes for each video and what are their corresponding video names?":
    query6 = '''select video_lc as likes,video_title as title from video_details
                where video_lc is not null'''
    cursor.execute(query6)
    table6 = cursor.fetchall()
    df6 = pd.DataFrame(table6,columns=["No. of likes","Video title"])
    st.write(df6)


elif Questions=="7. What is the total number of views for each channel and what are their corresponding channel names?":
    query7 = '''select video_vc as views, channel_name as channelname from video_details'''
    cursor.execute(query7)
    table7 = cursor.fetchall()
    df7 = pd.DataFrame(table7,columns=["Total views","Channel name"])
    st.write(df7)


elif Questions=="8. What are the names of all the channels that have published videos in the year 2022?":
    query8 = '''select video_pat as published,channel_name as channelname,video_title as title
                from video_details where year(video_pat)=2022'''
    cursor.execute(query8)
    table8 = cursor.fetchall()
    df8 = pd.DataFrame(table8,columns=["Published date","Channel name","Video title"])
    st.write(df8)


elif Questions=="9. What is the average duration of all videos in each channel and what are their corresponding channel names?":
    query9 = '''select AVG(video_duration) as duration,channel_name as channelname from video_details
                group by channel_name'''
    cursor.execute(query9)
    table9 = cursor.fetchall()
    df9 = pd.DataFrame(table9,columns=["Average duration","Channel name"])
    st.write(df9)


elif Questions=="10. Which videos have the highest number of comments and what are their corresponding channel names?":
    query10 = '''select video_title as title, channel_name as channelname, video_cc as comments from video_details
                 where video_cc is not null order by video_cc desc'''
    cursor.execute(query10)
    table10 = cursor.fetchall()
    df10 = pd.DataFrame(table10,columns=["Video title","Channel name","No. of comments"])
    st.write(df10)

