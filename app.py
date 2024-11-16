from flask import Flask, render_template, request
import requests
from banco import buscar_dados_clima, salvar_dados_clima
import plotly.graph_objects as go

app = Flask(__name__, static_folder='static')

API_KEY = '089de9028290ec6f829240e0133046fe'

def obter_dados_climaticos(cidade):
    dados_salvos = buscar_dados_clima(cidade)
    if dados_salvos:
        temperatura, descricao, umidade, vento = dados_salvos
        fig = gerar_mapa(temperatura, umidade, vento, cidade)
        return {
            'cidade': cidade,
            'temperatura': temperatura,
            'descricao': descricao,
            'umidade': umidade,
            'vento': vento,
            'grafico': fig.to_html(full_html=False)
        }

    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        salvar_dados_clima(cidade, dados)
        temperatura = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        umidade = dados['main']['humidity']
        vento = dados['wind']['speed']
        fig = gerar_mapa(temperatura, umidade, vento, cidade, dados['coord'])
        
        return {
            'cidade': cidade,
            'temperatura': temperatura,
            'descricao': descricao,
            'umidade': umidade,
            'vento': vento,
            'grafico': fig.to_html(full_html=False)
        }
    else:
        return None

def gerar_mapa(temperatura, umidade, vento, cidade, coordenadas=None):
    if coordenadas:
        lat, lon = coordenadas['lat'], coordenadas['lon']
    else:
        lat, lon = -15.0, -47.0  # Coordenadas padrão para o Brasil

    fig = go.Figure(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers+text',
        marker=go.scattermapbox.Marker(size=14, color='blue'),
        text=[f"Temp: {temperatura} °C, Umidade: {umidade}%, Vento: {vento} m/s"],
        textposition="top right"
    ))

    fig.update_layout(
        mapbox=dict(
            accesstoken="YOUR_MAPBOX_ACCESS_TOKEN",  # Use uma chave de acesso do Mapbox
            style="open-street-map",
            center=dict(lat=lat, lon=lon),
            zoom=5
        ),
        showlegend=False,
        title=f"Clima em {cidade}"
    )
    return fig

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/previsao', methods=['POST'])
def previsao():
    cidade = request.form['cidade']
    dados = obter_dados_climaticos(cidade)
    
    if dados:
        clima = {
            'cidade': cidade,
            'temperatura': dados['temperatura'],
            'descricao': dados['descricao'],
            'umidade': dados['umidade'],
            'vento': dados['vento']
        }
        return render_template('previsao.html', clima=clima, div_graph=dados['grafico'])
    else:
        erro = "Não foi possível obter os dados climáticos. Verifique o nome da cidade."
        return render_template('index.html', erro=erro)

if __name__ == '__main__':
    app.run(debug=True)
