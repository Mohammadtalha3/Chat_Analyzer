import streamlit as st
import proccessing,functions

st.sidebar.title("Chat Analyzer")



uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_Data= uploaded_file.getvalue()
    data= bytes_Data.decode("utf-8")
    df= proccessing.preprocessing(data)

    st.dataframe(df)    


    usr_lst= df['users'].unique().tolist()
    usr_lst.remove('Group NOtification')
    usr_lst.sort()
    usr_lst.insert(0,'Overall')
    selected_usr=st.sidebar.selectbox('Select user',usr_lst)

    if st.sidebar.button("Analyze"):

        no_mesg,word=functions.stats(selected_usr,df)

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header('Messages in Total')
            st.title(no_mesg)
        with col2:
            st.header('Total words')
            st.title(word)


    