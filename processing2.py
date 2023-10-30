import pandas as pd
import re

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
                

        
        
