from geopy.geocoders import Nominatim
# Busca no Nominatim qual é a latitude e longitude do ponto em questão.
    
geolocator = Nominatim(user_agent="Acidente")
location = geolocator.geocode(user_input)

# Desenha pro usuario onde é o ponto em questão até pra ele saber se é o ponto esperado

lat = location.latitude
lon = location.longitude

map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

st.map(map_data) 

st.write('latitude:',lat,'longitude:',lon)