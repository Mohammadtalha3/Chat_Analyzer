import streamlit as st
import processing2,functions
import matplotlib.pyplot as plt 
import seaborn as sns
import tempfile
import sentiment_Analysis
import pandas as pd


st.sidebar.title("Chat Analyzer")



uploaded_file = st.sidebar.file_uploader("Choose a file")


'''if uploaded_file is not None:
    bytes_Data= uploaded_file.getvalue()
    data= bytes_Data.decode("utf-8")
    df= proccessing.preprocessing(data)

    st.dataframe(df)'''   

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(uploaded_file.getvalue())
        temp_path = fp.name

        key=st.sidebar.selectbox('Please select the format: ',
                         ('12hr','24hr','custom'))

    df=pd.read_fwf(temp_path)    

    df= processing2.preprocessing(temp_path,key)

    
    dt=sentiment_Analysis.unwanted_data(result=df)
    st.dataframe(dt)
   
    


    usr_lst= df['users'].unique().tolist()
    usr_lst.remove('Group Notification')
    usr_lst.sort()
    usr_lst.insert(0,'Overall')
    selected_usr=st.sidebar.selectbox('Select user',usr_lst)

    if st.sidebar.button("Analyze"):

        no_mesg,word,media_mesg,num_links=functions.stats(selected_usr,df)

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header('Messages in Total')
            st.title(no_mesg)
        with col2:
            st.header('Total words')
            st.title(word)

        with col3:
            st.header('Total media shared')
            st.title(media_mesg)
        with col4:
            st.header("Total links Shared")
            st.title(num_links)


        st.title('Timeline')
        timeline= functions.user_timeline(selected_usr, df)

        fig,ax= plt.subplots()

        ax.plot(timeline['time'],timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title('Daily timeline')
        daily_timeline= functions.daily_timeline(selected_usr,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['date'], daily_timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title('Activity Map')

        col1,col2= st.columns(2)

        with col1:
            st.title('Most Activited Day')
            activate_day= functions.weekly_activity(selected_usr,df)
            fig,ax= plt.subplots()
            ax.bar(activate_day.index,activate_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title('Most Activated Month')
            month_Day= functions.montly_activity(selected_usr,df)
            fig,ax= plt.subplots()
            ax.bar(month_Day.index,month_Day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        st.title('Activity Heatmap')
        activate_heatmap= functions.heatmap(selected_usr,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(activate_heatmap)
        st.pyplot(fig)


        if selected_usr=='Overall':
            st.title('User Activity')
            x,df2=functions.user_activity(df)
            fig,ax=plt.subplots()
            


            col1,col2= st.columns(2)


            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(df2)
        st.title('word cloud')
        wc_df=functions.word_cloud(selected_usr,df)
        fig,ax= plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)

        st.title('Most used words')
        r_df= functions.most_used_words(selected_usr,df)

        fig,ax= plt.subplots()

        ax.bar(r_df[0],r_df[1])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)


        emoj_df= functions.user_emoji(selected_usr, df)

        st.title('Emoji Analysis')

        col1,col2= st.columns(2)


        with col1:
            st.dataframe(emoj_df)
        with col2:
            fig,ax= plt.subplots()
            ax.pie(emoj_df[1], labels=emoj_df[0],autopct='%0.2f')# when using pie chart you only give value and labels are seprately given
            st.pyplot(fig)


       



                



    