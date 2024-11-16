import sqlite3
from datetime import datetime

def conectar():
    conn = sqlite3.connect('clima.db')
    cursor = conn.cursor()
    
    # Criação da tabela, se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas_clima (
            id INTEGER PRIMARY KEY,
            cidade TEXT,
            data TEXT,
            hora TEXT,
            temperatura REAL,
            descricao TEXT,
            umidade INTEGER,
            vento REAL
        )
    ''')
    conn.commit()
    return conn, cursor 

def buscar_dados_clima(cidade):
    conn, cursor = conectar()
    agora = datetime.now()
    data = agora.strftime('%Y-%m-%d')
    hora = agora.strftime('%H:%M')

    cursor.execute('''
        SELECT temperatura, descricao, umidade, vento FROM consultas_clima
        WHERE cidade = ? AND data = ? AND hora = ?
    ''', (cidade, data, hora))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# salvar dados climáticos
def salvar_dados_clima(cidade, dados_climaticos):
    conn, cursor = conectar()
    agora = datetime.now()
    data = agora.strftime('%Y-%m-%d')
    hora = agora.strftime('%H:%M')

    temperatura = dados_climaticos['main']['temp']
    descricao = dados_climaticos['weather'][0]['description']
    umidade = dados_climaticos['main']['humidity']
    vento = dados_climaticos['wind']['speed']

    cursor.execute('''
        INSERT INTO consultas_clima (cidade, data, hora, temperatura, descricao, umidade, vento)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (cidade, data, hora, temperatura, descricao, umidade, vento))
    conn.commit()
    conn.close()

# Função para visualizar todos os dados da tabela no terminal, com base no chatgpt, para nao precisar ficar 
# alterando o codigo, para saber onde encontra-se os dados,
# consegui essa função para implementar e ser mais flexivel e facil de verificar no banco de dados
def ver_tabela(cidade=None, data=None):
    conn, cursor = conectar()
    query = ""  
    
    # Adicionando filtro de cidade, se fornecido
    if cidade:
        query += " AND cidade = ?"
    
    # Adicionando filtro de data, se fornecido
    if data:
        query += " AND data = ?"
    
    cursor.execute(query, (cidade, data) if cidade and data else (cidade,) if cidade else (data,))
    
    resultados = cursor.fetchall()
    conn.close()
    
    # Exibindo os dados no terminal
    if resultados:
        for linha in resultados:
            print(linha)
    else:
        print("Nenhum dado encontrado para a consulta especificada.")
