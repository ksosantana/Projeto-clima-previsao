import sqlite3
from datetime import datetime

def conectar():
    conn = sqlite3.connect('clima.db')
    cursor = conn.cursor()
# criação de tabela. 
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

#Para salvar dados climáticos.

def salvar_dados_clima(cidade, dados_climaticos):
    conn, cursor = conectar()
    agora = datetime.now()
    data = agora.strftime('%Y-%m-%d')
    hora = agora.strftime('%H:%M')

    cursor.execute('''
        SELECT dados_climaticos FROM consultas_clima
        WHERE cidade = ? AND data = ? AND hora = ?
    ''', (cidade, data, hora))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

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

# Função para visualizar todos os dados da tabela
def ver_tabela():
    conn, cursor = conectar()
    cursor.execute("SELECT * FROM consultas_clima")
    resultados = cursor.fetchall()
    conn.close()
    
    # Exibindo os dados no terminal
    for linha in resultados:
        print(linha)

# Exemplo de chamada para visualizar os dados da tabela
ver_tabela()