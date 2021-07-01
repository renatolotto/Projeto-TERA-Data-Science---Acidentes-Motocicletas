import streamlit as st
import pandas as pd
import numpy as np
import datetime
import urllib, json
import joblib
import googlemaps
from PIL import Image
from datetime import datetime



cat_features = ['Município','Condições Climáticas']
num_features = ['Latitude', 'Longitude','Mes_sin', 'Mes_cos','dias_semana_sin','horario_sin','horario_cos']

def load_model():
    return joblib.load('Models/classifier_v0.joblib')

def load_encoder():
    return joblib.load('Models/encoder_v0.joblib')

def app():#isolar todos os campos gráficos aqui dentro dessa função app

    st.set_page_config(layout='wide',page_title = "Motorcycle Risk Predictor - SP",page_icon=":vertical_traffic_light:")

    image = Image.open('images/logo3.png')

    st.image(image)#,use_column_width=True
    st.title('Avaliação de risco para motociclistas na grande São Paulo')
    # st.markdown('descrição do app')
    st.sidebar.title('Parâmetros de entrada')



    # inputs sidebar
    input_adress = st.sidebar.text_input("Endereço da localização atual")
    current=st.sidebar.checkbox('Dia e Horário Atual')
    if current == False:
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
        city = geocode_result[0].get('address_components')[3].get('long_name')
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

        with col1:
            st.map(map_data)
        with col2:
            st.write('Informações:')
            st.write('Latitude:',round(lat,5),'Longitude:',round(lon,5))
            st.write('Município: ',city)

    except:
        pass

    #do horário calcula o horario_sen e horario_cos   
    try:
        if current == False:
            list_h =input_time.split(':') # Cria lista com Hora, Minuto
        else:
            list_h = datetime.now().strftime("%H:%M").split(':')
        hor_flt = float(list_h[0]) + float(list_h[1])/60 # Transforma hora e minuto em um float
        horario_sin=np.sin(2.*np.pi*hor_flt/24.) # Transforma o horário em sin.
        horario_cos=np.cos(2.*np.pi*hor_flt/24.) # Transforma o horário em sin.

    except:
        pass

    #da data calcula o mes_sen e mes_cos
    try:
        if current == False:
            list_d =input_date.split('/') # Cria lista com dia, mes e ano
        else:
            list_d = datetime.now().strftime("%d/%m/%Y").split('/')
        dia = float(list_d[0])
        mes = float(list_d[1])
        ano = float(list_d[2])
        Mes_sin=np.sin(2.*np.pi*mes/12)
        Mes_cos=np.cos(2.*np.pi*mes/12)
    except:
        pass



    #da data calcula o dia_sem_sin e dia_sem_cos
    try:
        if current == False:
            date_chosen = datetime.strptime(input_date, '%d/%m/%Y')
            date_chosen = date_chosen.date()
            day_name = date_chosen.strftime("%A")
        else:
            date_chosen = datetime.today()
            date_chosen = date_chosen.date()
            day_name = datetime.today().strftime("%A")#retorna o nome do dia em inglês
        # date_chosen = datetime.date(ano, mes,dia)
        # day_name = datetime.date(int(ano), int(mes),int(dia)).strftime("%A")#retorna o nome do dia em inglês
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
        
        with col2:
            st.write('Data escolhida:',date_chosen)
            st.write('Hora:',int(list_h[0]),':',int(list_h[1]))
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
        df = pd.DataFrame({'Município':[city], 'Latitude':[lat], 'Longitude':[lon], 'Condições Climáticas':[condition_por], 'Mes_sin':[Mes_sin],'Mes_cos':[Mes_cos], 'dias_semana_sin':[dias_semana_sin], 'horario_sin':[horario_sin], 'horario_cos':[horario_cos]})
        df.to_csv('predict.csv',index=False)
        df_proc = encoder.transform(df)
        y = classifier.predict_proba(df_proc)
        y=y[0]
        probability = y[1]# classe positiva
        with col2:   
            st.write('Grau de Risco:',probability)

        if probability <0.2:
            output_msg = 'Você está sob RISCO BEM BAIXO, porém mantenha sempre a atenção!'
        elif probability >=0.2 and probability< 0.40 and horario_cos > 0 : #noite
            output_msg = 'Você está sob RISCO BAIXO, lembre-se de ligar as luzes'
        elif probability >=0.2 and probability< 0.40 and horario_cos < 0  : #dia
            output_msg = 'Mesmo com um RISCO BAIXO, lembre-se de usar capacete e dar a seta'
        elif probability >=0.4 and probability< 0.65:
            output_msg = 'Você está sob RISCO MODERADO, sempre cumpra as leis de trânsito!'
        elif probability >=0.65 and probability< 0.85 and condition_por != 'CHUVA':
            output_msg = 'Você está sob RISCO ALTO, todo cuidado é pouco, vá devagar e sempre use capacete'
        elif probability >=0.65 and probability< 0.85 and condition_por == 'CHUVA':
            output_msg = 'Você está sob RISCO ALTO e com a pista molhada redobre o cuidado'
        elif probability >=0.85 and condition_por != 'CHUVA':
            output_msg = 'Você está sob RISCO MUITO ALTO, preste muita atenção e diminua a velocidade'
        elif probability >=0.85 and condition_por == 'CHUVA':
            output_msg = 'Você está sob RISCO MUITO ALTO, mantenha a distância e diminua a velocidade'
    
        with col2: 
                st.subheader(output_msg)
    except:
        pass

    with st.sidebar:
        """
        #### :desktop_computer: [Source code in Github](https://github.com/renatolotto/Projeto-TERA-Data-Science---Acidentes-Motocicletas)
        """
        # """
        # ##### Source code: [![Renato](https://img.shields.io/github/stars/renatolotto/Projeto-TERA-Data-Science---Acidentes-Motocicletas?style=social)](https://github.com/renatolotto/Projeto-TERA-Data-Science---Acidentes-Motocicletas)
        # """
app()

