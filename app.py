import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Survey Results')
st.header('Survey Results 2023')
st.subheader('Please Notify Your Sensitivity in Day Scale')

### --- LOAD DATAFRAME
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='F:G',
                                header=3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
System-Elements = df['System-Elements'].unique().tolist()
times = df['Age'].unique().tolist()

Time_selection = st.slider('Time:',
                        min_value= min(Times),
                        max_value= max(Times),
                        value=(min(Times),max(Times)))

System-Elements_selection = st.multiselect('System-Elements:',
                                    System-Elements,
                                    default=System-Elements)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Time'].between(*Time_selection)) & (df['System-Elements'].isin(System-Elements_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Humidity']).count()[['Time']]
df_grouped = df_grouped.rename(columns={'Time': 'Temperature'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Humidity',
                   y='Temperature',
                   text='Temperature',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('images/survey.jpg')
col1.image(image,
        caption='Designed by slidesgo / Freepik',
        use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Priorities',
                values='Participants',
                names='System-Elementss')

st.plotly_chart(pie_chart)
