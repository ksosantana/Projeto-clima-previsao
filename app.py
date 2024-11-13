from flask import Flask, render_template, request
import requests
from banco import buscar_dados_clima, salvar_dados_clima  # Importa as funções do banco
import plotly.graph_objects as go  # Importa a biblioteca Plotly para gerar gráficos

app = Flask(__name__, static_folder='static')

# Sua chave de API 
API_KEY = '089de9028290ec6f829240e0133046fe'

def obter_dados_climaticos(cidade):
    # Verificar se já temos dados para a cidade no banco
    dados_salvos = buscar_dados_clima(cidade)
    if dados_salvos:
        temperatura, descricao, umidade, vento = dados_salvos
        # Gerar o gráfico com os dados salvos no banco
        fig = gerar_grafico(temperatura, umidade, vento)
        return {
            'cidade': cidade,
            'temperatura': temperatura,
            'descricao': descricao,
            'umidade': umidade,
            'vento': vento,
            'grafico': fig.to_html(full_html=False)  
        }

    # Se não houver dados no banco, faz a requisição para a API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        # Salva os dados no banco
        salvar_dados_clima(cidade, dados)
        temperatura = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        umidade = dados['main']['humidity']
        vento = dados['wind']['speed']
        
        # Gerar o gráfico com os dados da API
        fig = gerar_grafico(temperatura, umidade, vento)
        
        return {
            'cidade': cidade,
            'temperatura': temperatura,
            'descricao': descricao,
            'umidade': umidade,
            'vento': vento,
            'grafico': fig.to_html(full_html=False)  # Passando o gráfico gerado para o template
        }
    else:
        return None

def gerar_grafico(temperatura, umidade, vento):
    # Gerando gráficos circulares (pizza)
    fig = go.Figure(data=[go.Pie(labels=['Temperatura', 'Umidade', 'Vento'],
                                 values=[temperatura, umidade, vento],
                                 hole=0.3)])  # hole=0.3 cria um gráfico de pizza com buraco no meio
    fig.update_layout(title='Clima Atual', title_x=0.5)
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
