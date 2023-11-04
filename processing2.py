import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def preprocessing(data,key):
        split_formats = {
        '12hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
        '24hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        'custom' : ''
    }
        datetime_formats = {
        '12hr' : '%d/%m/%Y, %I:%M %p - ',
        '24hr' : '%d/%m/%Y, %H:%M - ',
        'custom': ''
    }
        
        with open(data,'r',encoding='utf-8') as raw_data:
                raw_string=raw_data.read()
                messages=re.split(split_formats[key],raw_string)[1:]
                dates=re.findall(split_formats[key],raw_string)

                dt=pd.DataFrame({'messages': messages,'dates': dates})

                dt['dates']= pd.to_datetime(dt['dates'],format=datetime_formats[key])

                messages=[]
                users=[]
                for i in dt['messages']:
                    a = re.split('([\w\W]+?):\s', i)
                    if(a[1:]):
                           users.append(a[1])
                           messages.append(a[2])
                    else:
                           users.append('Group Notification')
                           messages.append(a[0])


                
                
               


                dt['users']= users
                dt['messages']=  messages
                #dt.drop(columns=['Users_message'],  inplace=True)

                sentiments=SentimentIntensityAnalyzer()
                dt["positive"]=[sentiments.polarity_scores(i)["pos"] for i in dt["messages"]]
                dt["negative"]=[sentiments.polarity_scores(i)["neg"] for i in dt["messages"]]
                dt["neutral"]=[sentiments.polarity_scores(i)["neu"] for i in dt["messages"]]

                dt['date_name']= dt['dates'].dt.day_name()
                dt['year']=dt['dates'].dt.year
                dt['num_month']=dt['dates'].dt.month
                dt['date']= dt['dates'].dt.date
                dt['month']= dt['dates'].dt.month_name()
                dt['Day']= dt['dates'].dt.day
                dt['hour']= dt['dates'].dt.hour
                dt['Mint']= dt['dates'].dt.minute


                period = []
                for hour in dt[['date_name', 'hour']]['hour']:
                    if hour == 23:
                        period.append(str(hour) + "-" + str('00'))
                    elif hour == 0:
                        period.append(str('00') + "-" + str(hour + 1))
                    else:
                        period.append(str(hour) + "-" + str(hour + 1))

                dt['period'] = period


              

                return dt

data = 'Dataset/w0hatsapp-chat-data.txt'  
key = '12hr'
result= preprocessing(data,key)

def unwanted_data(result):
  lst=['messages and calls are end-to-end encrypted. no one outside of this chat, not even whatsapp, can read or listen to them. tap to learn more.',
    "you joined using this group's invite link",
    "+91 99871 38558 joined using this group's invite link",
    "+91 91680 38866 joined using this group's invite link",
    "+91 72762 35231 joined using this group's invite link",
    "+91 88392 06534 joined using this group's invite link",
    "+91 98709 38217 joined using this group's invite link",
    "+91 98702 02065 joined using this group's invite link",
    "+91 91370 44426 joined using this group's invite link",
    "+91 86559 19035 joined using this group's invite link",
    "+91 79778 39093 joined using this group's invite link",
    "+91 98670 44401 joined using this group's invite link",
    "+91 84828 26061 joined using this group's invite link",
    "+91 96191 55044 joined using this group's invite link",
    "+91 99201 75875 joined using this group's invite link",
    "+91 87799 77656 joined using this group's invite link",
    "+91 91372 82638 joined using this group's invite link",
    "+91 75069 97789 joined using this group's invite link",
    "+91 98234 51436 joined using this group's invite link",
    "+91 87796 70896 joined using this group's invite link",
    "+91 98208 31051 joined using this group's invite link",
    "+91 99675 58551 joined using this group's invite link",
    "ishneet (tsec, chem) joined using this group's invite link",
    "swaraj (tsec, cs) joined using this group's invite link",
    "+91 99672 39663 joined using this group's invite link",
    "+91 88889 25915 joined using this group's invite link",
    "+91 79778 76844 joined using this group's invite link",
    "+91 82080 03744 joined using this group's invite link",
    "+91 98337 61116 joined using this group's invite link",
    "+91 75078 05454 joined using this group's invite link",
    "+91 86059 72817 joined using this group's invite link",
    "+91 90678 93300 joined using this group's invite link",
    "+91 97306 65646 joined using this group's invite link",
    "+91 88273 12155 joined using this group's invite link",
    "shobit (tsec, cs) joined using this group's invite link",
    "+91 90290 16010 joined using this group's invite link",
    "+91 97022 69539 joined using this group's invite link",
    "+91 91677 97590 joined using this group's invite link",
    "kritanjali joined using this group's invite link",
    "+91 75064 59162 joined using this group's invite link",
    "+91 98212 97215 joined using this group's invite link",
    "+91 93242 72022 joined using this group's invite link",
    "+91 99692 93643 joined using this group's invite link",
    "+91 98923 74688 joined using this group's invite link",
    "+91 93728 12301 joined using this group's invite link",
    '+91 96536 93868 removed saket (tsec, cs)',
    "+91 75061 80036 joined using this group's invite link",
    '+91 96536 93868 added saket (tsec, cs)',
    "+91 88507 19064 joined using this group's invite link",
    "+91 97735 69400 joined using this group's invite link",
    '+91 96536 93868 left',
    "+91 99205 75511 joined using this group's invite link",
    "hardik raheja (tsec, cs) joined using this group's invite link",
    "+91 77384 72938 joined using this group's invite link",
    "darshan rander (tsec, it) joined using this group's invite link",
    "+91 79770 56210 joined using this group's invite link",
    "+91 90499 38860 joined using this group's invite link",
    "+91 80801 39870 joined using this group's invite link",
    "+91 96648 44643 joined using this group's invite link",
    "+91 96992 89993 joined using this group's invite link",
    "+91 91363 39446 joined using this group's invite link",
    "riddhi shah (tsec, cs) joined using this group's invite link",
    "+91 84335 18102 joined using this group's invite link",
    "+91 88284 70904 joined using this group's invite link",
    "+91 96197 60216 joined using this group's invite link",
    "chirag sharma (tsec, cs) joined using this group's invite link",
    "+91 88795 52797 joined using this group's invite link",
    "+91 83789 81107 joined using this group's invite link",
    "+91 6380 608 411 joined using this group's invite link",
    "anushree (tsec, cs) joined using this group's invite link",
    "+91 80820 81616 joined using this group's invite link",
    "+91 86556 33169 joined using this group's invite link",
    "+91 80979 26321 joined using this group's invite link",
    "+91 92842 87810 joined using this group's invite link",
    "+91 76208 56877 joined using this group's invite link",
    "+91 81696 22410 joined using this group's invite link",
    "+91 97308 52191 joined using this group's invite link",
    "+91 83690 21693 joined using this group's invite link",
    "+91 96194 00980 joined using this group's invite link",
    "+91 76667 91772 joined using this group's invite link",
    "aneri shah (tsec, cs) joined using this group's invite link",
    "+91 77699 70908 joined using this group's invite link",
    "shreya (tsec, it) joined using this group's invite link",
    "mittul dasani (tsec, cs) joined using this group's invite link",
    "+91 83292 66084 joined using this group's invite link",
    "+91 87799 49518 joined using this group's invite link",
    "+91 70394 60876 joined using this group's invite link",
    "+91 90282 48673 joined using this group's invite link",
    "pranay thakur (tsec, cs) joined using this group's invite link",
    "+91 96536 93868 joined using this group's invite link",
    "+91 79776 23387 joined using this group's invite link",
    "+91 95187 88109 joined using this group's invite link",
    "+91 94044 50783 joined using this group's invite link",
    "mohammed (tsec, extc) joined using this group's invite link",
    "+91 88792 49540 joined using this group's invite link",
    "+91 82375 09868 joined using this group's invite link",
    "+91 82080 02653 joined using this group's invite link",
    "+91 97697 60869 joined using this group's invite link",
    "+91 77568 95072 joined using this group's invite link",
    "hamzah (tsec, cs) joined using this group's invite link",
    "+91 98204 33166 joined using this group's invite link",
    "+91 96896 27597 joined using this group's invite link",
    "+91 88988 92174 joined using this group's invite link",
    "+91 98676 12302 joined using this group's invite link",
    "+91 99875 91581 joined using this group's invite link",
    "keyul jain (tsec, cs) joined using this group's invite link",
    "+91 75064 86714 joined using this group's invite link",
    'prithvi rohira (tsec, cs) left',
    "+91 90822 59476 joined using this group's invite link",
    "+91 72495 29889 joined using this group's invite link",
    "+91 88790 69347 joined using this group's invite link",
    "+91 99202 79905 joined using this group's invite link",
    "<Media omitted>"]
  
  

  mask = result['messages'].str.contains('|'.join(map(re.escape, lst)), case=False, na=False, regex=True)
  result= result[~mask]

  return result


dtt=unwanted_data(result)

dtt
                

        
        
