import pandas as pd
import streamlit as st
import plotly.express as px

# reading clean csv file with relative path
df = pd.read_csv('vehicles_us_clean.csv')
df.info()


st.header(':red[**Find Your dream Car Today**]')    # :color[] introduced 1.16.0, divider introduced 1.21.0
st.image('https://www.automoblog.net/wp-content/uploads/2023/07/kids-dream-cars-ai-automoblog.net-1-10-1024x1024.png')


st.sidebar.write('''**Enter Your Preferences Below-**  
                 You will see the table changes according to your preferences''')
color =st.sidebar.selectbox('Choose Your Color', df[df['paint_color'] != 'unknown'].paint_color.unique(), index=1)
condition = st.sidebar.radio("In What Condition?",df.condition.unique())
#price_def = (int(df.price.describe()['25%']), int(df.price.describe()['75%']))
budget = st.sidebar.slider('Choose Your Budget', int(df.price.min()), int(df.price.max()), (int(df.price.min()), int(df.price.max())))
actual_budget=list(range(budget[0],budget[1]+1))
Antique = st.sidebar.checkbox('Antique cars only')

column_names = {'price':'Price', 'model_year':'Model Year', 'model':'Model', 'condition':'Condition', 'cylinders':'Cylinders', 'fuel':'Fuel',
       'odometer':'Odometer', 'transmission':'Transmission', 'type':'Type', 'paint_color':'Paint Color', 'is_4wd':'Is 4WD ',
       'date_posted':'Date Posted', 'days_listed':'Days Listed'}

if Antique:
    filtered_data = df[df['model_year'] <= 1994]
    filtered_data = filtered_data[filtered_data['paint_color'] == color]
    filtered_data = filtered_data[filtered_data['condition'] == condition]
    filtered_data = filtered_data[filtered_data['price'].isin(actual_budget)]                      
else:
    filtered_data = df[df['paint_color'] == color]
    filtered_data = filtered_data[filtered_data['condition'] == condition]
    filtered_data = filtered_data[filtered_data['price'].isin(actual_budget)]  
    
st.dataframe(filtered_data)

fig1 = px.scatter(filtered_data, x='model_year', y='price', color='condition', title='Price by Model Year and Car Condition', 
                  labels={'price':'Price in $', 'condition':'Condition', 'model_year':'Model Year'}) 

fig2 = px.histogram(filtered_data, x="type", title='Distribution of Car Type', color_discrete_sequence=['indianred'], 
                    labels={'type':'Car Type'}).update_xaxes(categoryorder='total descending')
fig2.update_layout(yaxis_title_text = 'Number of Cars')
fig2.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Number of Cars")))
## changed to type because condition didnt made sense with the filter

#fig3_labels = filtered_data['fuel'].value_counts().index
#fig3_values = filtered_data['fuel'].value_counts().values
#fig3 = px.pie(data_frame=filtered_data, names=fig3_labels, values=fig3_values, title='A lot of GAZ fueled cars! We don\'t forget the DIESEL lovers', color_discrete_sequence=px.colors.sequential.Rainbow)


st.subheader(':red[**Some Additional Info to Make Your Decision Easier**]')
st.write('**Number of Cars by Fuel Type**')
count_fuel = filtered_data['fuel'].value_counts()
cols = st.columns(len(count_fuel))
counter = 0
for i, v in count_fuel.items():
    cols[counter].metric(label=i, value=v)
    counter += 1
st.plotly_chart(fig1)
st.plotly_chart(fig2)
#st.plotly_chart(fig3)

