import re
import pandas as pd

def preprocessing(data):
    pattern='\d{2}/\d{2}/\d{4},\s*\d{1,2}:\d{2}\s*[APap][Mm]\s*-'

    message= re.split(pattern,data)[1:]
    dates= re.findall(pattern,data)

    dt= pd.DataFrame({"Users_message":message, "Dates":dates})

    dt['Dates'] = dt['Dates'].astype(str)
    dt['Dates'] = dt['Dates'].str.replace('\u202f', ' ')
    dt['Dates'] = pd.to_datetime(dt['Dates'], format='%d/%m/%Y, %I:%M %p -', errors='coerce')


    user=[]
    mesg= []

    for i in dt['Users_message']:
     entry= re.split('([\w\W]+?):\s', i)
     if entry[1:]:
        user.append(entry[1])
        mesg.append(entry[2])
     else:
        user.append('Group NOtification')
        mesg.append(entry[0])

    dt['users']= user
    dt['messages']= mesg
    dt.drop(columns=['Users_message'],  inplace=True)


    dt['year']=dt['Dates'].dt.year
    dt['month']= dt['Dates'].dt.month_name()
    dt['Day']= dt['Dates'].dt.day
    dt['hour']= dt['Dates'].dt.hour
    dt['Mint']= dt['Dates'].dt.minute


    return dt
