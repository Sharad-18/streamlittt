import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
df=pd.read_csv('startup_cleaned.csv')


st.set_page_config(layout='wide',page_title='Startup Analysis')

df['date']=pd.to_datetime(df['date'], errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def overall_analysis():
    st.title('OverAll Analysis')
    
    # total invested amount
    total=round(df['amount'].sum())
    
    
    # max funding
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    
    # average funding
    avg_funding=total=round(df.groupby('startup')['amount'].sum().mean())
    
    # num of startup
    num_startup=df['startup'].nunique()
    
    
    col1,col2,col3,col4=st.columns(4)
    
    with col1:
        st.metric('Total',str(total),' CR')
    
    with col2:
        st.metric('Max',str(max_funding),' CR')
        
    with col3:
        st.metric('Avg',str(avg_funding),' CR')
        
    with col4:
        st.metric('Funded Startups',str(num_startup),' CR')
        
    st.header('MOM on Graph')
    
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        tempdf=df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        tempdf=df.groupby(['year','month'])['amount'].count().reset_index()
        
    tempdf['x_axis']=tempdf['month'].astype('str') + '-' + tempdf['year'].astype('str')
    fig5,ax5=plt.subplots()
    ax5.plot(tempdf['x_axis'],tempdf['amount'])
    st.pyplot(fig5)
    
    # invested in sectors
    
    st.subheader('Amount Invested Sectors')
    selected_option1=st.selectbox('Select Type1',['Total Amount','Count'])
    if selected_option1=='Total Amount':
        gen_sector=df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
    else:
        gen_sector=df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(10)
    st.dataframe(gen_sector)
    
    
    fig6,ax6=plt.subplots()
    ax6.pie(gen_sector,labels=gen_sector.index,autopct="%0.01F%%")
    st.pyplot(fig6)
    colu1,colu2=st.columns(2)
    # type of funding
    with colu1:
        st.subheader('Types of Funding')
        type_fund=df.groupby('type')['amount'].sum()
        type_fund2=df['type'].nunique()
        st.text(type_fund2)
        st.dataframe(type_fund)
    
    # city wise funding
    with colu2:
        st.subheader('City Wise Funding')
        city_fund=df.groupby('city')['amount'].sum()
        city_fund2=df['city'].nunique()
        st.text(city_fund2)
        st.dataframe(city_fund)
    
    # top Startups on the basis of investing
    colum1,colum2=st.columns(2)
    with colum1:
        st.subheader('Top 10 Startups On The Basis Of Investors')
        top_startups=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(10)
        st.dataframe(top_startups)
    with colum2:
        st.subheader('Top 10 Startups On The Basis Of Year')
        top_startups1=df.groupby(['startup','year'])['amount'].max().sort_values(ascending=False).head(10)
        st.dataframe(top_startups1)
    column1,column2=st.columns(2)
    with column1:
        st.subheader('Top 10 Investors')
        top_investors=df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)
        st.dataframe(top_investors)
        
# load company data

def company_data(company):
    st.title(company)
    # Type of industry
    industry=df.groupby('startup')['vertical'].sum()[company]
    st.subheader('Type of Industry')
    st.text(industry)
    
    # subindustry
    sub_industry=df.groupby('startup')['subvertical'].sum()[company]
    st.subheader('SubType of Industry')
    st.text(sub_industry)
    
    # location
    location=df.groupby('startup')['city'].sum()[company]
    st.subheader('Location')
    st.text(location)
    
    # funding Round
    type_of_funding=df.groupby('startup')['type'].sum()[company]
    st.subheader('Funding Round')
    st.text(type_of_funding)

def invester_detail(investor):
    st.title(investor)
    
    

    # recent investment
    recent_df=df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'type', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(recent_df)

    # biggest investment
    col1,col2=st.columns(2)
    with col1:    
        big_investment=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        
        st.subheader('Big Investment')
        st.dataframe(big_investment)
        fig,ax=plt.subplots()
        ax.bar(big_investment.index,big_investment.values)
        st.pyplot(fig)
    # general investment
    with col2:
        gen_invest=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested in')
        st.dataframe(gen_invest)
        fig1,ax1=plt.subplots()
        ax1.pie(gen_invest,labels=gen_invest.index,autopct="%0.01F%%")
        st.pyplot(fig1)
    col3,col4=st.columns(2)
    with col3:
        round_invest=df[df['investors'].str.contains(investor)].groupby('type')['amount'].sum()
        st.subheader('Rounds')
        st.dataframe(round_invest)
        fig2,ax2=plt.subplots()
        ax2.pie(round_invest,labels=round_invest.index,autopct="%0.01F%%")
        st.pyplot(fig2)
    
    with col4:
        city_invest=df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Invested In City')
        st.dataframe(city_invest)
        fig3,ax3=plt.subplots()
        ax3.pie(city_invest,labels=city_invest.index,autopct="%0.01F%%")
        st.pyplot(fig3)
        
    df['year']=df['date'].dt.year
    year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YOY Investment')
    st.dataframe(year_series)
    fig4,ax4=plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)    

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select one',['Overall analysis','Startup','Investor'])

if option == 'Overall analysis':
    overall_analysis()
        
        
elif option=='Startup':
    selected_comapany=st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btnl= st.sidebar.button('Find Startup Details')
    if btnl:
        company_data(selected_comapany)
    
    
else:
    selected_investor=st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    st.title('Investor Analysis')
    if btn2:
        invester_detail(selected_investor)
