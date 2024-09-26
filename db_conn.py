import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Função de conexão ao banco de dados
def get_connection():
    conn = psycopg2.connect(
        host="192.168.0.3",
        port="5432",
        database="cloudbooster_db",
        user="ipja",
        password="37192541aaSS@"
    )
    
    # Definir o schema
    conn.cursor().execute('SET search_path TO ipja;')
    return conn

# Função para buscar dados
def fetch_data():
    conn = get_connection()
    cur = conn.cursor()
    
    # Consulta na tabela main_avaliacao
    cur.execute("SELECT * FROM main_avaliacao;")
    rows = cur.fetchall()
    
    # Obter os nomes das colunas
    colnames = [desc[0] for desc in cur.description]
    
    cur.close()
    conn.close()
    
    # Retornar os dados como um DataFrame
    return pd.DataFrame(rows, columns=colnames)