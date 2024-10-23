import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao
import numpy as np

# Primeira consulta / atualizações se dados
#Consultar os dados
query = "SELECT * FROM tb_carros"

#Carregar os dados e armazenar
df = conexao(query)

#Botão para atualizar
if st.button("Atualizar Dados"):
    df = conexao(query)
    
#Estrutura lateral de filtros 
st.sidebar.header("Selecione um Filtro")
marca = st.sidebar.multiselect("Marca Selecionada", #Nome do seletor 
                               options=df["marca"].unique(), #Opções de cada marca
                               default=df["marca"].unique()
                               )

modelo = st.sidebar.multiselect("Modelo Selecionado", #Nome do seletor 
                               options=df["modelo"].unique(), 
                               default=df["modelo"].unique()
                               )

ano = st.sidebar.multiselect("Ano Selecionado", #Nome do seletor 
                               options=df["ano"].unique(), 
                               default=df["ano"].unique()
                               )

valor = st.sidebar.multiselect("Valor Selecionado", #Nome do seletor 
                               options=df["valor"].unique(), 
                               default=df["valor"].unique()
                               )

cor = st.sidebar.multiselect("Cor Selecionada", #Nome do seletor 
                               options=df["cor"].unique(), 
                               default=df["cor"].unique()
                               )

numero_vendas = st.sidebar.multiselect("Número de Vendas Selecionado", #Nome do seletor 
                               options=df["numero_vendas"].unique(), 
                               default=df["numero_vendas"].unique()
                               )

#Aplicar os filtros selecionados
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas)) 
]

#Exibir valores médios - estatisticas
def Home():
    with st.expander("Valores"): #Cria uma caixa expansável con um título   
        mostrarDados = st.multiselect('Filter:' , df_selecionado, default=[])
     
     #Verifica se o usuário sekecionou colunas para exibir
        if mostrarDados:
        #Exibe os dados filtrados pelas colunas selecionadas
            st.write(df_selecionado[mostrarDados])
         
    if not df_selecionado.empty:
        venda_total = df_selecionado["numero_vendas"].sum()
        venda_media = df_selecionado["numero_vendas"].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()
        
        #Cria 3 colunas para exibir os totais calculados
        total1, total2, total3 = st.columns(3, gap="large")
        
        with total1:
            st.info("Valor Total de Vendas dos Carros", icon='📌')
            st.metric(label="Total", value=f"{venda_total:,.0f}")
            
        with total2:
            st.info("Valor Médio das Vendas", icon='📌')
            st.metric(label="Média", value=f'{venda_media:,.0f}')
            
        with total3:
            st.info("Valor Mediano das Carros", icon='📌')
            st.metric(label="Média", value=f'{venda_media:,.0f}')
    
    else: 
        st.warning("Nenhum dado disponível com os filtros selecionados")
#Insere uma linha divisória para separar as seções         
st.markdown("""---------""")

#GRÁFICOS!!!!!!
def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("Nenhum dado disponível para geerar gráficos")
        #Interrompe a função
        return


#Criação de gráficos
#4 abas --> Graficos de Barras, Graficos de Linhas, Graficos de pizza e Dispersão
    graf1, graf2, graf3, graf4, graf5 = st.tabs(["Gráfico de Barras", "Gráfico de Linhas", "Gráfico de Pizza", "Gráfico de Dspersão","Gráfico de Área"])

    with graf1:
        st.write("Gráfico de Barras") #Título
        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)
        #Agrupa pela marca e conta o número de ocorrências da coluna valor. Depois ordena o resultado de forma decrescente.
        
        fig_valores = px.bar(
            investimento, #Contém os dados sobre valores por marca
            x= investimento.index,
            y="valor",
            orientation="v",
            title="<b>Valores de Carros</b>",
            color_discrete_sequence=["#0083b3"])
            
        #Exibe
        st.plotly_chart(fig_valores, use_contrainer_width=True)
        
        
    with graf2:
        st.write("Gráfico de Linhas")
        dados = df_selecionado.groupby("marca").count()[["valor"]]
        
        fig_valores2 = px.line(dados, 
                                  x=dados.index,
                                  y="valor",
                                  title="<b>Valores por Marca</b>",
                                  color_discrete_sequence=['#0083b8'])
        st.plotly_chart(fig_valores2, use_container_width=True)
        
    with graf3:
        st.write("Gráfico de Pizza")
        dados2 = df_selecionado.groupby("marca").sum()[["valor"]]
        fig_valores3 = px.pie(dados2,
                              values="valor", #Valores que serão representados
                              names=dados2.index, #Título do gráfico de pizza
                              title="<b>Distribuição de Valores por Marca</b>"
                              )
        st.plotly_chart(fig_valores3, use_contrainer_width=True)
        
    with graf4:
        st.write("Gráfico de Dispersão")
        dados3 = df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])
        
        fig_valores4 = px.scatter(dados3,
                                  x="marca",
                                  y="value",
                                  color="variable",
                                  title="<b>Dispersão de Valores por Marca</b>")
        st.plotly_chart(fig_valores4, use_container_width=True)
        
    with graf5:
        dados4 = df_selecionado.groupby("marca").count()[["valor"]]
        fig_valores5 = px.area(dados4, 
                                  x=dados4.index,
                                  y="valor",
                                  title="<b>Valores por Marca</b>",
                                  color_discrete_sequence=['#0083b8'])
        st.area_chart(fig_valores5)
        
        
        
        
        
        
        
        
        
        
        
        
def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    objetivo = 200000
    percentual = round((valorAtual / objetivo * 100))
    
    if percentual > 100:
        st.subheader("Valor Atingidos!!!")
    else:
        st.write(f"Você tem {percentual}% de {objetivo}. Corra atrás filhão!")
        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, text="Alvo %")
            
# MENU LATERAL
def menuLateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="Menu", options=["Home", "Progresso"],
                                  icons=["house", "eye"], menu_icon="cast",
                                  default_index=0)
    if selecionado == "Home":
        st.subheader(f"Página:{selecionado}")
        Home()
        graficos(df_selecionado)
        
    if selecionado == "Progresso":
        st.subheader(f"Página:{selecionado}")
        barraprogresso()
        graficos(df_selecionado)
        
        
#Ajustar o CSS
        
        
menuLateral()