from altair.vegalite.v4.schema.core import DataFormat
from numpy.core.numeric import NaN
from numpy.lib.function_base import place
import streamlit as st
from google.cloud import firestore
import json
import pandas as pd
import itertools
import numpy as np



st.title('influencers:')
# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

doc_id = db.collection("users")

docs = doc_id.stream()
# print(docs)
# for doc in docs:
#     print(doc.to_dict())
my_dict = { doc.id: doc.to_dict() for doc in docs }
#print(my_dict)
df = pd.DataFrame.from_dict(my_dict)
df = df.transpose()
placeholder = st.empty()
#placeholder.dataframe(df)
for col in df: 
    df[col] = df[col].fillna('NA')
    column = df.columns.get_loc(col)
    print(type(df.iat[0,column]))
df['engagement_comments'] = df['engagement_comments'].astype(str)
df['engagement_likes'] = df['engagement_likes'].astype(str)
df['follower_count'] = df['follower_count'].astype(str)
df['location'] = df['location'].astype(str)
df['no_of_posts'] = df['no_of_posts'].astype(str)
df['username'] = df['username'].astype(str)

filtered_df = df

hash = df['hashtags'].tolist()
hash = list(itertools.chain.from_iterable(hash))
col = df.columns.get_loc("hashtags")

hashtag_df = pd.DataFrame()

#Hashtag
hashtag_filter = st.sidebar.multiselect(
    'Select hashtag',
    options=hash
)
#apply filter
filtered_df['hashtags'] = filtered_df['hashtags'].apply(tuple)
if hashtag_filter:
    for hash in hashtag_filter:
        for row in range((df.shape)[0]): 
            if hash in df.iat[row,col]:
                hashtag_df = hashtag_df.append(df.iloc[row,:])
    if hashtag_df.empty == False:
        filtered_df = pd.merge(hashtag_df,filtered_df, how = 'inner')
        placeholder.table(filtered_df)
    else:
        for col in hashtag_df: 
            hashtag_df[col] = hashtag_df[col].fillna('NA')


#Location
locations = df['location'].tolist()
locations = [x for x in locations if type(x) != float]
#print(locations) 
locations_filter = st.sidebar.multiselect(
    'Select country',
    options=locations
)

#apply filter
location_df = pd.DataFrame()
col = df.columns.get_loc("location")
if locations_filter:
    for row in range((df.shape)[0]): 
        if (df.iat[row,col]) in (locations_filter):
            location_df = location_df.append(df.iloc[row,:])
    if (location_df.empty == False):
        #print(filtered_df)
        filtered_df = pd.merge(location_df,filtered_df, how = 'inner')
        #print(filtered_df)
        placeholder.table(filtered_df)
    else:
        for col in location_df: 
            location_df[col] = location_df[col].fillna('NA')
    


#Followers
followers_df = pd.DataFrame()
followers = st.sidebar.slider(
    'Select follower range',
    1000, 10000, (2500, 7500), step=100
)
min_fol = followers[0]
max_fol = followers[1]
col = df.columns.get_loc("follower_count")
#print(col)

if followers:
    for row in range((df.shape)[0]): 
        followers_count = df.iat[row,col]
        # print(min_fol)
        # print(max_fol)
        if followers_count == 'NA':
            followers_count = np.NaN
        if min_fol <= int(followers_count) <= max_fol:
            #apply filter
            followers_df = followers_df.append(df.iloc[row,:])

    if followers_df.empty == True:
        filtered_df = pd.DataFrame()
        for col in followers_df: 
            followers_df[col] = followers_df[col].fillna('NA')
    if (filtered_df.empty == False and followers_df.empty == False):
        print(followers_df)
        print(filtered_df)
        filtered_df["follower_count"] = filtered_df["follower_count"].astype(int)
        followers_df["follower_count"] = followers_df["follower_count"].astype(int)

        filtered_df = pd.merge(followers_df,filtered_df, how = 'inner')
        print(filtered_df)

       
        
    placeholder.table(filtered_df)


#engagement rate - comments
comments_df = pd.DataFrame()
comments = st.sidebar.slider(
    'Select engagement rate for comments',
   0,100, (25,75), step=5
)
min_fol = comments[0]
max_fol = comments[1]
col = df.columns.get_loc("engagement_comments")
#print(col)

if comments:
    for row in range((df.shape)[0]): 
        rate = df.iat[row,col]
        # print(min_fol)
        # print(max_fol)
        if rate == 'NA':
            rate = 0
        if min_fol <= float(rate) <= max_fol:
            #apply filter
            comments_df = comments_df.append(df.iloc[row,:])

    if comments_df.empty == True:
        filtered_df = pd.DataFrame()
        for col in comments_df: 
            comments_df[col] = comments_df[col].fillna('NA')
    if (filtered_df.empty == False and comments_df.empty == False):
        print(comments_df)
        print(filtered_df)
        filtered_df["engagement_comments"] = filtered_df["engagement_comments"].astype(str)
        comments_df["engagement_comments"] = comments_df["engagement_comments"].astype(str)

        filtered_df = pd.merge(comments_df,filtered_df, how = 'inner')
        print(filtered_df)

       
        
    placeholder.table(filtered_df)



#engagement rate - likes
likes_df = pd.DataFrame()
likes = st.sidebar.slider(
    'Select engagement rate for likes',
   0,100, (25,75), step=5
)
min_fol = likes[0]
max_fol = likes[1]
col = df.columns.get_loc("engagement_likes")
#print(col)

if likes:
    for row in range((df.shape)[0]): 
        rate = df.iat[row,col]
        # print(min_fol)
        # print(max_fol)
        if rate == 'NA':
            rate = 0
        if min_fol <= float(rate) <= max_fol:
            #apply filter
            likes_df = likes_df.append(df.iloc[row,:])

    if likes_df.empty == True:
        filtered_df = pd.DataFrame()
        for col in likes_df: 
            likes_df[col] = likes_df[col].fillna('NA')
    if (filtered_df.empty == False and likes_df.empty == False):
        print(likes_df)
        print(filtered_df)
        filtered_df["engagement_likes"] = filtered_df["engagement_likes"].astype(str)
        likes_df["engagement_likes"] = likes_df["engagement_likes"].astype(str)

        filtered_df = pd.merge(likes_df,filtered_df, how = 'inner')
        print(filtered_df)

       
        
    placeholder.table(filtered_df)


    
placeholder.table(filtered_df)