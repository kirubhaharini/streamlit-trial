from altair.vegalite.v4.schema.core import DataFormat
from numpy.core.numeric import NaN
from numpy.lib.function_base import place
import streamlit as st
from google.cloud import firestore
import json
import pandas as pd
import itertools
import numpy as np

def app():
    st.title('posts')

     # Authenticate to Firestore with the JSON account key.
    db = firestore.Client.from_service_account_json("firestore-key.json")

    doc_id = db.collection("users")
    my_dict = {}
    usernames = []
    documents = db.collection(u'users')
    #print(documents)
    for doc in documents.stream():
        print(doc.id)
        usernames.append(doc.id)
        collections = documents.document(doc.id).collections()
        for collection in collections:
            
            for doc in collection.stream():
                my_dict[doc.id] = doc.to_dict()


    print(my_dict)
    df = pd.DataFrame.from_dict(my_dict)
    df = df.transpose()
    df.insert(0, 'username', usernames)

    placeholder = st.empty()
    #placeholder.dataframe(df)
    for col in df: 
        df[col] = df[col].fillna('NA')
        column = df.columns.get_loc(col)
        print(type(df.iat[0,column]))
    df['engagement_comments'] = df['engagement_comments'].astype(str)
    df['engagement_likes'] = df['engagement_likes'].astype(str)

    filtered_df = df

    

    #engagement rate - comments
    comments_df = pd.DataFrame()
    comments = st.sidebar.slider(
        'Select engagement rate for comments',
    0,100, (0,100), step=5
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
    0,100, (0,100), step=5
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
