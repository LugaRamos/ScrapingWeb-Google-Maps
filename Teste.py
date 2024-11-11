import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAgRF6ZuK7_EO4KrHlemSlYLD2ilteldx4')

coordenadas = (-25.515148, -48.5224133)  # Use as coordenadas corretas
termo_pesquisa = 'Cafeteria'
raio_perimetro = 5000  # Raio em metros

try:
    places_result = gmaps.places(query=termo_pesquisa, location=coordenadas, radius=raio_perimetro)
    print(places_result)
except googlemaps.exceptions.ApiError as e:
    print(f"Erro na API: {e}")
