# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 09:46:18 2023

@author: richa
"""

import pandas as pd

import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import webbrowser
from PIL import Image
import zipfile as zp

zpName='Nguyen_FP_Data.zip'
zpfile= zp.ZipFile(zpName,'r').extractall()


st.set_page_config(
        page_title="Country Reference Guide")

with st.sidebar:
    selected = option_menu(
        menu_title='Main Menu',
        options=['Home',"Economy",'Human Development Index','Manufacturing','Military Ependiture','Population'], 
        icons=['house','currency-dollar','mortarboard', 'building' , 'cash-coin', 'people-fill']
        
        )


# MAKE DATA CHARTS AND TABLES
def show_Data(data,cntry1,cntry2,rng1,rng2,yr1,mesr1,mesr2,txt1,txt2):
    
    st.header(txt2)
    df=data
    
    #Choose what countries you want to examine (Defaulted to China and US)
    countries = st.multiselect("Choose Countries", list(df.index),[cntry1, cntry2])
    countryDB=df.T[countries]
    
    #Choose the range of years to examine (Defaulted to Minimum and Maximum)
    yR = st.slider('Please select a Range of Years',rng1, rng2,(rng1, rng2))
    
    #Creates ranged specified data and displays the data
    rCountryDB=countryDB[str(min(yR)):str(max(yR))]
    st.write(mesr1, rCountryDB.T)
        #Download Main Data
    df1=rCountryDB.T.to_csv().encode('utf-8')
    st.download_button(label='Download Dataframe as CSV?',data=df1,file_name=f'{txt2}{countries}{str(min(yR))}-{str(max(yR))}.csv',mime='text/csv')
    

    #Displays Total Percent Change for range
    totPerChange=pd.DataFrame()
    totPerChange[f'{str(min(yR))} - {str(max(yR))}']=rCountryDB.T.apply(lambda row: str((((row.iloc[-1] - row.iloc[0])/row.iloc[0])*100).round(2))+'%', axis=1)
    
    col1, col2 =st.columns(2)
    with col1:
        st.write('Total Percent Change')
        st.dataframe(totPerChange,use_container_width=True)
    with col2:
        #Download DF % Change
        "\n"
        "\n"
        "\n"
        "\n"
        '\n'
        st.download_button(label='Download Data as CSV',data=totPerChange.to_csv().encode('utf-8'),file_name=f'TotPctChange{countries}_{str(min(yR))}-{str(max(yR))}.csv',mime='text/csv')
            
            
    #plots data and interactive map
    plotLine=px.line(rCountryDB, labels={'index':'Years','value':mesr2,'Country':'Countries'}, title=f'Line Chart of {txt2} from {str(min(yR))} to {str(max(yR))}')
    plotScatr=px.scatter(rCountryDB, labels={'index':'Years','value':mesr2,'Country':'Countries'}, title=f'Line Chart of {txt2} from {str(min(yR))} to {str(max(yR))}')
    plotArea=px.area(rCountryDB, labels={'index':'Years','value':mesr2,'Country':'Countries'}, title=f'Area Chart of {txt2} from {str(min(yR))} to {str(max(yR))}')
    
    charts=st.radio('Which Chart do you want to See?',('Line','Scatter','Area'))
    if charts=='Line':
        st.plotly_chart(plotLine)
    if charts=='Scatter':
        st.plotly_chart(plotScatr)
    if charts=='Area':
        st.plotly_chart(plotArea)
    
    
    st.divider()
            
    #Displays percent change
    st.subheader('Annual Percent Change')
    perChange = rCountryDB.T.pct_change(axis='columns')*100
    perChange
    st.download_button(label='Download Data as CSV',data=perChange.to_csv().encode('utf-8'),file_name=f'AnnualPctChange{countries}_{str(min(yR))}-{str(max(yR))}.csv',mime='text/csv')
    
    #Get average % change
    avgPerChange=perChange.mean(axis=1)
    perChangeAvg=pd.DataFrame()
    perChangeAvg['Average Annual Percent Change'] = avgPerChange
    
    col3, col4 =st.columns(2)
    with col3:
        st.write('Average Percent Change')
        st.dataframe(perChangeAvg['Average Annual Percent Change'],use_container_width=True)
    with col4:
        "\n"
        "\n"
        "\n"
        "\n"
        '\n'
        st.download_button(label='Download Data as CSV',data=perChangeAvg.to_csv().encode('utf-8'),file_name=f'AnnualPctChange{countries}_{str(min(yR))}-{str(max(yR))}.csv',mime='text/csv')
   
    #plot % change
    perPlot=px.line(perChange.T,labels={'index':'Years','value':'Percent %','Country':'Countries'}, title='Line Chart of Annual Percent Change')
    st.plotly_chart(perPlot) 
        
    st.divider()
    
    #Moves to data for specific year
    st.subheader(txt1)
    
    #Choose specific year
    ySpec=st.slider('Please Choose a Specific Year',rng1,rng2,(yr1))
    ySpecStr=str(ySpec)
    
    #Makes dataframe based on specified year
    ySpecCntry=countryDB.T[str(ySpec)]
    
    col5,col6=st.columns(2)
    with col5:
        st.write(mesr1)
        st.dataframe(ySpecCntry, use_container_width=True)
    with col6:
        "\n"
        "\n"
        "\n"
        "\n"
        '\n'
        st.download_button(label='Download Data as CSV',data=ySpecCntry.to_csv().encode('utf-8'),file_name=f'Data{countries} {str(ySpec)}.csv',mime='text/csv')
     
        
    #Makes piechart to compare
    fig=px.pie(countryDB.T,values=str(ySpec),names=countries,color=countries,title='Examine Size Makeup at Year '+ySpecStr)
    st.plotly_chart(fig, use_container_width=True)
    bar=px.bar(ySpecCntry,color=countries, labels={'value':mesr2,'Country':'Countries','color':'Countries'},title='The Data at Year '+ySpecStr)
    st.plotly_chart(bar,use_container_width=True )

cna='China'
usa='United States'


#HOME TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------


if selected == 'Home':
    st.balloons()
    image=Image.open('pngwing.com.png')
    st.image(image)
    st.header('Project Description')
    st.markdown("The purpose of this Final Project was to learn how to use Streamlit to make a quick reference guide relating to my applied project on "
                +"**:red[The Developments of the People’s Republic of China,] and the :blue[Need to Reshore American Manufacturing]**. "
                +"This guide will display areas of intrigue relating to a country’s :green[Economic, Human Development, Manufacturing, Military, and Population] data. "
                +"It will display only the data for the given selected countries as well as the data at certain time frames. Links to the online sources of the data "
                +"will be given, as well as the option to download the data. "
                )
    with st.expander('Imported Libraries and Tools Used'):
        
        st.code('''
                
            import pandas as pd \n
            import matplotlib.pyplot as plt \n
            import streamlit as st \n
            import plotly.express as px \n
            from streamlit_option_menu import option_menu \n
            import webbrowser \n
            from PIL import Image
            
            ''', language='python')

      
    


   
#ECONOMIC TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

# Extract Economic Data
econData= pd.read_csv('WEOApr2023all.csv')
econData=econData.drop(labels=['WEO Country Code','ISO','WEO Subject Code','Subject Notes','Country/Series-specific Notes','Estimates Start After'], axis=1)
econData=econData.set_index(['Country'])
econData.iloc[:,3:]=econData.iloc[:,3:].astype(float)

#Get only Data in terms of USD
econDataUSD=econData[econData['Units']=='U.S. dollars']

#Get only GDP in terms of USD
econDataUSDGDP=econDataUSD[econDataUSD['Subject Descriptor']=='Gross domestic product, current prices']
econDataUSDGDP=econDataUSDGDP.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only GDP/capita in terms of USD
econDataUSDGDPCap=econDataUSD[econDataUSD['Subject Descriptor']=='Gross domestic product per capita, current prices']
econDataUSDGDPCap=econDataUSDGDPCap.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only Data in terms of PPP
econDataPPP=econData[econData['Units']=='Purchasing power parity; international dollars']

#Get only GDP in terms of PPP
econDataPPPGDP=econDataPPP[econDataPPP['Subject Descriptor']=='Gross domestic product, current prices']
econDataPPPGDP=econDataPPPGDP.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only GDP/Capita in terms of PPP
econDataPPPGDPCap=econDataPPP[econDataPPP['Subject Descriptor']=='Gross domestic product per capita, current prices']
econDataPPPGDPCap=econDataPPPGDPCap.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)


#Code for Economics Tab

if selected == 'Economy':
    st.title('Economy')
    #Give Tab Description
    st.write("This tab will display the global economic data ranging from 1980 to the projected data in 2028. " +"A country's Gross Domestic Product (GDP), is a measure of how much economic output a country generated, typically measured in US Dollars. " 
             +"A country's GDP per capita measures the economic output of a nation per resident. Purchasing Power Parity (PPP) is a metric that adjusts the US Dollar to more closely match how much a dollar is worth in a given country"
             + "These mutrics are based on items such as a nation's standard of living, currency, and more, taking a 'basket of goods' approach. "
             +"The data past year 2022 are the International Monetary Fund's Projected figures.")

    econDataTb, econLink=st.tabs(['Data','Source'])
    with econDataTb:
       choice=[]
       sel=st.selectbox('Choose what Data you Wish to See',('GDP-USD','GDP-USD per Capita','GDP-PPP','GDP-PPP per Capita'))
       choice.append(sel)
       if choice == ['GDP-USD']:
           USDGDP=show_Data(econDataUSDGDP,cna,usa,1980,2028,2022,'Data Measured in Millions USD (2021 Prices)','Millions USD (2021 Prices)','Compare GDP for a Specific Year',"Country's GDP in USD")
       
       if choice == ['GDP-USD per Capita']:
           USDGDPCap=show_Data(econDataUSDGDPCap,cna,usa,1980,2028,2022,'Data Measured in USD (2021 Prices)','USD (2021 Prices)','Compare GDP/Capita for a Specific Year',"Country's GDP per Capita in USD")
       
       if choice == ['GDP-PPP']:
           PPPGDP=show_Data(econDataPPPGDP,cna,usa,1980,2028,2022,'Data Measured in Purchasing Power Parity; Millions International Dollars', 'Millions International Dollars' , 'Compare GDP-PPP for a Specific Year',"Country's GDP in PPP")
      
       if choice == ['GDP-PPP per Capita']:
           PPPGDPCap=show_Data(econDataPPPGDPCap,cna,usa,1980,2028,2022,'Data Measured in Purchasing Power Parity; International Dollars', 'International Dollars', 'Compare GDP/Capita in PPP for a Specific Year',"Country's GDP per Capita in PPP")
    with econLink:
        st.write("This Data originated from the International Monetary Fund")
        econURL='https://www.imf.org/en/Publications/WEO/weo-database/2023/April/download-entire-database'
        if st.button('International Monetary Fund'):
            webbrowser.open_new_tab(econURL)
 
    


#HUMAN DEVELOPMENT INDEX TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Extract HDI Data
hdiDF=pd.read_csv('HDR21-22_Composite_indices_complete_time_series.csv').set_index('Country')


#Code for HDI tab
if selected == 'Human Development Index':
    st.title('Human Development Index')
    st.write("The Human Development Index (HDI) is a summary measure of the average achievement in key dimensions of human development. "
             + "These achievements include but are not limited to an individual’s life expectancy, education, standard of living and more. "
             +"Generally a higher score means that a country is more developed and ranges from 0 to 1."
             +"This data was retrieved from the United Nations Development Program")
    hdiDataTb, hdiLink=st.tabs(['Data','Source'])
    with hdiDataTb:
        hdiData=show_Data(hdiDF,cna,usa,1990,2021,2021,'Scores','Scores','Compare HDI for a Specific Year',"Country's Human Development Index")

    with hdiLink:
        st.write('This Data originated from the United Nations')
        hdiURL='https://hdr.undp.org/data-center/documentation-and-downloads'
        if st.button('United Nations Development Program'):
            webbrowser.open_new_tab(hdiURL)
        

#MANUFACTURING TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Extract and Clean Manufacturing Data
mfgData=pd.read_csv('API_NV.IND.MANF.CD_DS2_en_csv_v2_5363423.csv')
mfgData=mfgData.rename(columns={"Country Name": "Country"})
mfgData=mfgData.set_index(['Country'])
mfgData=mfgData.drop(labels=['Country Code','Indicator Code','Indicator Name'], axis=1)

    
if selected == 'Manufacturing':
    st.title('Manufacturing')
    st.write("The following data will display the value added by manufacturing per country in 2021 US dollars. "
             + "The following data originated from the World Bank")
    
    mfgDataTb, mfgLink=st.tabs(['Data','Source'])
    with mfgDataTb:
        mfgShow=show_Data(mfgData,cna,usa,1975,2021,2021,'Amount of Output in US Dollars', 'US Dollars' , 'Compare Amount of Output for a Specific Year', "Country's Manufacturing Output")
      
    with mfgLink:
        mfgURL='https://data.worldbank.org/indicator/NV.IND.MANF.CD?end=2021&start=1960&view=chart'
        st.write('This Data originated from the World Bank')
        if st.button('World Bank'):
            webbrowser.open_new_tab(mfgURL)
        
        
    




#MILITARY TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Get annual Military Expenditure Data
milExp=pd.read_csv('milExp.csv').set_index('Country')

#Get MilExp as share of GDP
milExpPer=pd.read_csv('milPercent.csv').set_index('Country')
milExpPer=milExpPer.mul(100)
    
if selected == 'Military Ependiture':
    st.title('Military Ependiture')
    st.write("The following data will display the Military Expenditures of each selected country as well as how much that spending is related to gross domestic product. "
             +"The following data originated from the Stockholm International Peace Research Institute.")
    milTb, milLink=st.tabs(['Data','Source'])
    with milTb:
        st.header('Military Expenditures')
        choice1=[]
        sel1=st.selectbox('Choose what Data you Wish to See',('Annual Military Expenditures','Annual Military Expenditures as a Share of GDP'))
        choice1.append(sel1)
        if choice1 == ['Annual Military Expenditures']:
            milExpData=show_Data(milExp,cna,'United States of America',1949,2022,2021,'Measured in Millions USD (2021 prices)', 'Millions US Dollars (2021 prices)' ,'Compare Military Expenditure in a Specifc Year', 'Annual Military Expenditure')
        if choice1 == ['Annual Military Expenditures as a Share of GDP']:
            milExpPerData=show_Data(milExpPer,cna,'United States of America',1949,2022,2021,'Measured as a Percent Makeup', 'Percentage of GDP' ,'Compare Share of GDP in a Specifc Year', 'Annual Military Expenditure as a Share of GDP')
            
    with milLink:
        milURL='https://milex.sipri.org/sipri'
        st.write('This Data originated from the Stockholm International Peace Research Institute')
        if st.button('Stockholm International Peace Research Institute'):
            webbrowser.open_new_tab(milURL)



#POPULATION TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Ectract population data
popData=pd.read_csv('totpopmf.csv')
popData['Time']=popData['Time'].astype(str)
popData=popData.rename(columns={"Location": "Country"})

#get only total population
totPopData=popData.drop(labels=['PopMale','PopFemale'], axis=1).pivot_table(values='PopTotal', index='Country', columns='Time', aggfunc='first')*1000

#get only male population
mPopData=popData.drop(labels=['PopTotal','PopFemale'], axis=1).pivot_table(values='PopMale', index='Country', columns='Time', aggfunc='first')*1000

#get only female population 
fPopData=popData.drop(labels=['PopTotal','PopMale'], axis=1).pivot_table(values='PopFemale', index='Country', columns='Time', aggfunc='first')*1000

    
if selected == 'Population':
    st.title('Population')
    st.write("The following data will display the Total, Male, and Female Populations for the selected countries within a given time frame. "
             +"The data past year 2022 are the United Nations’ projected figures. "
             +"This data originated from the United Nations Department of Economic And Social Affairs.")
    
    popDataTb,popLink=st.tabs(['Data','Source'])
    with popDataTb:
        choice2=[]
        sel2=st.selectbox('Choose what Data you Wish to See',('Total Population','Male Population','Female Population'))
        choice2.append(sel2)
        if choice2==['Total Population']:
            totPopData=show_Data(totPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,   'Compare Populations', 'Total Populations of Countries')
        if choice2==['Male Population']:
            totPopData=show_Data(mPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,   'Compare Populations', 'Total Male Populations of Countries')
        if choice2==['Female Population']:
            totPopData=show_Data(fPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,  'Compare Populations', 'Total Female Populations of Countries')

    
    with popLink:
        st.write('This Data originated from the United Nations Department of Economic And Social Affairs')
        popURL='https://population.un.org/wpp/Download/Standard/CSV/'
        if st.button('United Nations Department of Economic And Social Affairs'):
            webbrowser.open_new_tab(popURL)
