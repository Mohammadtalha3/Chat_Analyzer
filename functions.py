def stats(selected_usr,df):
    if selected_usr != "overall":
        df2=df[df['users']== selected_usr]

    num_message=df.shape[0]

    word=[]

    for wrd in df2['messages']:
        word.extend(wrd.split())
    return num_message, len(word)