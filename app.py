import pandas as pd
import streamlit as st
import plotly.express as px

# reading clean csv file with relative path
df = pd.read_csv('vehicles_us_clean.csv')
df.info()


st.header(':red[Find Your dream Car Today]')
st.image('https://www.automoblog.net/wp-content/uploads/2023/07/kids-dream-cars-ai-automoblog.net-1-10-1024x1024.png')


st.sidebar.write('''Enter Your Preferences  
                 You will see tha table change to find the best cars for you''')
color =st.sidebar.selectbox('Choose Your Color', df.paint_color.unique(), index=1)
condition = st.sidebar.radio("In What Condition?",df.condition.unique())
price_def = (int(df.price.describe()['25%']), int(df.price.describe()['75%']))
year = st.sidebar.slider('Choose Your Budget', int(df.price.min()), int(df.price.max()), (price_def))
Antique = st.sidebar.checkbox('Antique cars only')


if Antique:
    df_ant = df[df['model_year'] <= 1994]
    st.dataframe(df_ant[(df_ant['paint_color'] == color) & (df_ant['condition'] == condition)])
else:
    st.dataframe(df[(df['paint_color'] == color) & (df['condition'] == condition)])

    ##.style.format(subset=['model_year'], formatter="{:.2f}")


fig1 = px.scatter(df, x='model_year', y='price', color='condition', title='Price by Model Year and Car Condition')
fig2 = px.histogram(df, x="condition", title='Soo many EXCELLENT cars!', color_discrete_sequence=['indianred']).update_xaxes(categoryorder='total descending')
fig3_labels = df['fuel'].value_counts().index
fig3_values = df['fuel'].value_counts().values
fig3 = px.pie(data_frame=df, names=fig3_labels, values=fig3_values, title='A lot of GAZ fueled cars! We don\'t forget the DIESEL lovers', color_discrete_sequence=px.colors.sequential.Rainbow)

with st.expander('Some Additional Info for Car Experts Like You'): 
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
