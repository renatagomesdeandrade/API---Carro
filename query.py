# Conexão com o banco de dados e enviar os dados para a dash

#CONEXÃO  
import mysql.connector 
import pandas as pd

def conexao(query):
    conn = mysql.connector.connect(
        host = "127.0.0.1",
        port = "3306",
        user = "root",
        password = "senai@134",
        db = "bd_carro"
    )
    
    
    #Executa a consulta SQL e armazena o resultadoem um DataFrame
    dataframe = pd.read_sql(query, conn)

    conn.close()
    return dataframe    