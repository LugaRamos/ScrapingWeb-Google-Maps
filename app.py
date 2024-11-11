from flask import Flask, render_template, request, send_file
import googlemaps
import folium
import pandas as pd
from io import BytesIO
import os

# Verificar se o diretório 'static' existe, caso contrário, criá-lo
if not os.path.exists('assets'):
    os.makedirs('assets')

app = Flask(__name__, static_folder='assets')

# Inicializar o cliente Google Mapsl
gmaps = googlemaps.Client(key='AIzaSyAgRF6ZuK7_EO4KrHlemSlYLD2ilteldx4')

def obter_resultados(termo_pesquisa, raio_perimetro, coordenadas, max_paginas):
        # Lista para armazenar os resultados
        resultados = []

        # Realizar a pesquisa em várias páginas
        for pagina in range(1, max_paginas + 1):
            # Realizar a pesquisa na página atual
            places_result = gmaps.places(query=termo_pesquisa, location=coordenadas, radius=raio_perimetro, page_token=None if pagina == 1 else places_result['next_page_token'])

            # Iterar sobre os resultados da pesquisa
            for place in places_result['results']:
                # Obter o ID de lugar para obter mais detalhes
                place_id = place['place_id']
                
                # Obter detalhes do lugar usando o ID de lugar
                place_details = gmaps.place(place_id=place_id, fields=['name', 'formatted_address', 'formatted_phone_number', 'opening_hours', 'website', 'url', 'geometry'])
                
                # Extrair as informações
                nome_empresa = place_details['result']['name']
                endereco = place_details['result']['formatted_address']
                telefone = place_details['result'].get('formatted_phone_number', 'N/A')
                horario_funcionamento = place_details['result'].get('opening_hours', {}).get('weekday_text', 'N/A')
                website = place_details['result'].get('website', 'N/A')
                google_maps_url = place_details['result'].get('url', 'N/A')
                latitude = place_details['result']['geometry']['location']['lat']
                longitude = place_details['result']['geometry']['location']['lng']
                
                # Adicionar o resultado à lista
                resultados.append({'Nome': nome_empresa, 'Endereço': endereco, 'Telefone': telefone, 'Horário de Funcionamento': horario_funcionamento, 'Website': website, 'Google Maps URL': google_maps_url, 'Latitude': latitude, 'Longitude': longitude})
            
            # Verificar se há mais páginas de resultados
            if 'next_page_token' not in places_result:
                break
        
        return resultados

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    if request.method == 'POST':
        termo_pesquisa = request.form['termo_pesquisa']
        raio_perimetro = int(request.form['raio_perimetro'])
        coordenadas = {
            'latitude': request.form['latitude'],
            'longitude': request.form['longitude']
        }

        max_paginas = 20
        
        resultados = obter_resultados(termo_pesquisa, raio_perimetro, coordenadas, max_paginas)
        
        if resultados:
            df_resultados = pd.DataFrame(resultados)

            # Criar o arquivo Excel em memória
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_resultados.to_excel(writer, index=False)
            output.seek(0)

            # Salvar o mapa em memória também
            mapa = folium.Map(location=[resultados[0]['Latitude'], resultados[0]['Longitude']], zoom_start=10)
            folium.Circle(
                radius=raio_perimetro,
                location=[resultados[0]['Latitude'], resultados[0]['Longitude']],
                color='blue',
                fill=True,
                fill_color='blue',
                opacity=0.3
            ).add_to(mapa)
            
            for lugar in resultados:
                folium.Marker([lugar['Latitude'], lugar['Longitude']], popup=lugar['Nome']).add_to(mapa)

            mapa.save('assets/mapa.html')

            # Renderizar a página com os resultados e o link para download
            return render_template('index.html', resultados=resultados, download_link=True)
        
        else:
            return 'Nenhum resultado encontrado.'
    
    else:
        return render_template('index.html')

@app.route('/download')
def download_file():
    # Enviar o arquivo Excel gerado em memória
    output = BytesIO()
    df = pd.read_excel('assets/Empresas.xlsx')
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='Empresas.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)