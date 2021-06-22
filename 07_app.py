
from requests.adapters import Response, ResponseError
from scipy.sparse import data
from sklearn.pipeline import Pipeline
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import urllib, json
import joblib
from geopy.geocoders import Nominatim
import googlemaps
from PIL import Image



cat_features = ['Município','Condições Climáticas']
num_features = ['Latitude', 'Longitude','Mes_sin', 'Mes_cos','dias_semana_sin','horario_sin','horario_cos']

def load_model():
    return joblib.load('Models/classifier_v0.joblib')

def load_encoder():
    return joblib.load('Models/encoder_v0.joblib')

def app():#isolar todos os campos gráficos aqui dentro dessa função app

    st.set_page_config(layout='wide',page_title = "Motorcycle Risk Predictor - SP",page_icon=":vertical_traffic_light:")

    image = Image.open('logo2.png')

    st.image(image,use_column_width=True)
    st.title('Avaliação de risco para motociclistas na grande São Paulo')
    st.sidebar.title('Parâmetros de entrada')



    # inputs sidebar
    input_adress = st.sidebar.text_input("Endereço da localização atual")
    # current=st.sidebar.checkbox('Dia e Horário Atual')
    input_date = st.sidebar.text_input("Data escolhida - Formato DD/MM/YYYY")
    input_time = st.sidebar.text_input("Horario escolhido - Formato HH:MM")

    # definindo 2 colunas
    col1, col2 = st.beta_columns(2)

    #carregando artefatos
    encoder = load_encoder()
    classifier = load_model()

    #do Endereço busca na API -- Lat, Lon, Município ####### Google Maps API ########
    try:
        key='AIzaSyCT6oRvKT3-LH0XDts0GqNAY4M8RrmxJIQ'
        gmaps = googlemaps.Client(key)
        geocode_result = gmaps.geocode(input_adress)
        lat = geocode_result[0].get('geometry').get('viewport').get('southwest').get('lat')
        lon = geocode_result[0].get('geometry').get('viewport').get('southwest').get('lng')
        município = geocode_result[0].get('address_components')[3].get('long_name')
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

        with col1:
            st.map(map_data)
        with col2:
            st.write('Informações:')
            st.write('Latitude:',round(lat,5),'Longitude:',round(lon,5))
            st.write('Município: ',município)
    except:
        pass


    #do horário calcula o horario_sen e horario_cos
    try:
       
        list_h =input_time.split(':') # Cria lista com Hora, Minuto
        hor_flt = float(list_h[0]) + float(list_h[1])/60 # Transforma hora e minuto em um float
        horario_sin=np.sin(2.*np.pi*hor_flt/24.) # Transforma o horário em sin.
        horario_cos=np.cos(2.*np.pi*hor_flt/24.) # Transforma o horário em sin.
        # with col2:
            # st.write('Hora:',int(list_h[0]),':',int(list_h[1]))
        #     st.write('horario_cos:',horario_cos)
    except:
        pass

    #da data calcula o mes_sen e mes_cos
    try:
       
        list_d =input_date.split('/') # Cria lista com dia, mes e ano
        dia = float(list_d[0])
        mes = float(list_d[1])
        ano = float(list_d[2])
        Mes_sin=np.sin(2.*np.pi*mes/12)
        Mes_cos=np.cos(2.*np.pi*mes/12)
    except:
        pass



    #da data calcula o dia_sem_sin e dia_sem_cos
    try:
        date_chosen = datetime.date(int(ano), int(mes),int(dia))
        day_name = datetime.date(int(ano), int(mes),int(dia)).strftime("%A")#retorna o nome do dia em inglês
        if day_name=='Friday':
            day_num=5
        elif day_name=='Thursday':
            day_num=4
        elif day_name=='Wednesday':
            day_num=3
        elif day_name=='Tuesday':
            day_num=2
        elif day_name=='Monday':
            day_num=1
        elif day_name=='Sunday':
            day_num=7
        elif day_name=='Saturday':
            day_num=6
        day_num_norm = day_num/7 #normalizando o dia
        dias_semana_sin=np.sin(2.*np.pi*day_num_norm)
        dias_semana_cos=np.cos(2.*np.pi*day_num_norm)
        
        # with col2:
        #     st.write('Data',date_chosen)
            # st.write('Nome do dia',day_name)
            # st.write('Num dia',day_num)
            # st.write('Num dia NORM',day_num_norm)
            # st.write('dia sem SIN',dias_semana_sin)
            # st.write('dia sem COS',dias_semana_cos)
    except:
        pass



    # da data e horário busca na API a condição climática
    try:
        Weather_but = st.sidebar.button('Calcular Risco')
        key1='B8JYA2DGP8JEMDN3SH4N4XGTT'
        key2='A6USW7ZJVKXS796M85TUD5JB7'
        url_weather = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{},{}/{}?key={}".format(lat,lon,date_chosen,key2)

        def get_API_value():
            response = urllib.request.urlopen(url_weather)
            data = json.loads(response.read())
            condition = data.get('days')[0].get('hours')[int(list_h[0])].get('conditions')
            precip = data.get('days')[0].get('hours')[int(list_h[0])].get('precip')
            return [condition,precip]
        if Weather_but == True:
            cond_precip= get_API_value()
            if cond_precip[0] =='Partially cloudy':
                condition_por = 'NUBLADO'
                # image2 = Image.open('nublado.png')
            elif cond_precip[0] == 'Overcast':
                condition_por = 'NUBLADO'
                # image2 = Image.open('nublado.png')
            elif cond_precip[0] == 'Rain':
                condition_por = 'CHUVA'
                # image2 = Image.open('chuva.png')
            elif cond_precip[0] == 'Clear':
                condition_por = 'BOM'
                # image2 = Image.open('bom.png')
            elif cond_precip[0] == 'Rain, Partially cloudy':
                condition_por = 'CHUVA'
                # image2 = Image.open('chuva.png')
            elif cond_precip[0] == 'Rain, Overcast':
                condition_por = 'CHUVA'
                # image2 = Image.open('chuva.png')    

            with col2:   
                # st.write('Condição do tempo: ',cond_precip[0])
                st.write('Condição do tempo: ',condition_por)                 
    except:
        pass

    #CRIANDO DF COM TODOS INPUTS e calculando proba
    try:
        df = pd.DataFrame({'Município':[município], 'Latitude':[lat], 'Longitude':[lon], 'Condições Climáticas':[condition_por], 'Mes_sin':[Mes_sin],'Mes_cos':[Mes_cos], 'dias_semana_sin':[dias_semana_sin], 'horario_sin':[horario_sin], 'horario_cos':[horario_cos]})
        df.to_csv('predict.csv',index=False)
        df_proc = encoder.transform(df)
        y = classifier.predict_proba(df_proc)
        y=y[0]
        probability = y[1]# classe positiva
        with col2:   
                st.write('Grau de Risco:',probability)

        if probability <0.2:
            output_msg = 'Você está sob RISCO BEM BAIXO, porém mantenha sempre a atenção!'
        elif probability >=0.2 and probability< 0.40:
            output_msg = 'Você está sob RISCO BAIXO, sempre cumpra as leis de trânsito!'
        elif probability >=0.4 and probability< 0.65:
            output_msg = 'Você está sob RISCO MODERADO, sempre cumpra as leis de trânsito!'
        elif probability >=0.65 and probability< 0.85:
            output_msg = 'Você está sob RISCO ALTO, vá devagar e sempre use capacete'
        elif probability >=0.85:
            output_msg = 'Você está sob RISCO MUITO ALTO, preste muita atenção e diminua a velocidade'
    
        with col2: 
                st.subheader(output_msg)
    except:
        pass

    with st.sidebar:
        """
        #### :desktop_computer: [Source code in Github](https://github.com/renatolotto/Projeto-TERA-Data-Science---Acidentes-Motocicletas)
        """
    # (https://github.com/aldencabajar/traffic_flow_counter)

        # """
        # ## Code Generator for Machine Learning
        # [![Renato](https://img.shields.io/github/stars/renatolotto/Projeto-TERA-Data-Science---Acidentes-Motocicletas?label=Github&style=social)](https://github.com/renatolotto/Projeto-TERA-Data-Science---Acidentes-Motocicletas)
        # """
            



    #dar um predict
    #melhorar mapa
    #implementar current 
    # etc...


app()

