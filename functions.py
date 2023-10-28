from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import re



def stats(selected_usr,df):
    if selected_usr != "Overall":
        df=df[df['users']== selected_usr]

    num_message=df.shape[0]

    word=[]

    for wrd in df['messages']:
        word.extend(wrd.split())

    media_mesg= df[df['messages']== '<Media omitted>\n'].shape[0]

    
    extractor=URLExtract()
    links=[]
    for m in df['messages']:
        links.extend(extractor.find_urls(m))





    return num_message, len(word), media_mesg, len(links)


def user_activity(df):
    data=df['users'].value_counts().head()
    df=round((df['users'].value_counts()/df.shape[0])* 100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return data,df

def word_cloud(selected_usr,df):
    if selected_usr != 'Overall':
        df= df[df['users']== selected_usr]

    wc=WordCloud(width=500, height=500,min_font_size=10,background_color='white')

    df_wc=wc.generate(df['messages'].str.cat(sep=" "))

    

    return df_wc

def most_used_words(selected_usr,df):

    f= open('D:\chat_Analyzer\punjabi_stopwords.txt','r')
    stopwords= f.read()

    if selected_usr != 'Overall':
        df=df[df['users']== selected_usr]
    
    temp= df[df['messages'] !='<Media omitted>\n']
    temp= temp[temp['users'] != 'Group NOtification']

    word=[]
    for message in temp['messages']:
        for wrd in message.lower().split():
            if wrd not in stopwords:
                word.append(wrd)


    r_df=pd.DataFrame(Counter(word).most_common(20))

    return r_df


def user_emoji(selected_usr,df):

    if selected_usr != 'Overall':
        df= df[df[df['users']== selected_usr]]
    

    emojis=[]
    

    # Define a regular expression to match emojis
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # Emoticons
                           u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
                           u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                           u"\U0001F700-\U0001F77F"  # Alphabetic Presentation Forms
                           "]+", flags=re.UNICODE)

    for message in df['messages']:
        emojis.extend(emoji_pattern.findall(message))


    emoji_df=pd.DataFrame(Counter(emojis).most_common(20))
    return emoji_df


def user_timeline(selected_usr,df):
    if selected_usr != 'Overall':
        df= df[df['users']==selected_usr]
    
    timeline= df.groupby(['year','num_month','month']).count()['messages'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time']= time

    
    return timeline


def daily_timeline(selected_usr,df):
    if selected_usr !='Overall':
        df= df[df['users']== selected_usr]
    
    mon_timeline= df.groupby(['date']).count()['messages'].reset_index()

    return mon_timeline

def weekly_activity(selected_usr,df):
    if selected_usr !='Overall':
        df= df[df['users']==selected_usr]
    
    return df['date_name'].value_counts()

def montly_activity(selected_usr,df):
    if selected_usr !='Overall':
        df= df[df['users']== selected_usr]
    
    return df['month'].value_counts()

def heatmap(selected_usr,df):
    if selected_usr !='Overall':
        df= df[df['users']==selected_usr]
    
    user_heatmap = df.pivot_table(index='date_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap


                    




    

    
    


        





    