# Bibliotecas
import streamlit as st
import pandas as pd
# OS é pra mexer com arquivos e pastas do comput
import os
import base64

# Configuração viual da página
st.set_page_config(
    page_title="Filmes da Barbie",
    page_icon="🧚‍♀️",
    layout="wide",
)

# Título
st.title("🎀Universo da Barbie")
st.subheader("Detalhes dos filmes da Barbie junto das trilhas sonoras")# Titulo menor

# Carregar os dados do CSV
df = pd.read_csv('filmes_da_Barbie.csv', sep=",", engine="python") # Esclarece que os arquivo estão separados por virgula e tbm ressolve problema de acento se tiver

# Permite colocar informações no csv com '/', pq na hora de ler ele vai tirar
df.columns = df.columns.str.replace('\t', '') 

# Barra lateral com os filtros
st.sidebar.header("✨Filtros de busca🎬✨")
anos = st.sidebar.slider("Ano de lançamento", int(df["Ano"].min()), int(df["Ano"].max()), (2001, 2017)) # Slider coloca a barra de anos

# Caixa com o generos, todos vêm marcado de inicio
generos = st.sidebar.multiselect("Gênero", options=df["Genero"].unique(), default=df["Genero"].unique()) 

# Filtra a tabela de acordo com os filtros
df_filtrado = df[
    (df["Ano"] >= anos[0]) & # Pega filme com ano igual ou maior ao minimo selecionado
    (df["Ano"] <= anos[1]) & # Menor ou igual ao maximo selecionado
    (df["Genero"].isin(generos)) # Só os gêneros dentro do ano selecionado
]

# Verifica se há dados após o filtro
if df_filtrado.empty: #Vê e o quadro ta vazio
    st.warning("Nenhum filme encontrado com os filtros aplicados.")

# Exibir os dados do filme se não tiver vazio a caixa
else:
    for _, row in df_filtrado.iterrows():
        col1, col2, col3 = st.columns([1, 2, 1])

        # Imagem do filme
        with col1:
            img_path = f"imagens/{row['Imagemfilme'].strip()}" # Caminho do arquivo da imagem

            # Verificar se o arquivo existe
            if os.path.exists(img_path):
                st.image(img_path, caption="Imagem do Filme", # Exibe a imagem com uma legenda
                        
            # Ajeita ela no espaço             
                use_container_width=True)
            
            # Caso a img não seja encontrada
            else:
                st.warning("Imagem não encontrada.")

        # Detalhes e trilha sonora
        with col2:
            st.markdown(f"### 💖 {row['Filme']} ({row['Ano']})")
            st.markdown(f"👑 **Personagem:** {row['Personagem']}")
            st.markdown(f"🎭 **Gênero:** {row['Genero']}")
            st.markdown(f"🎵 **Trilha Sonora:** {row['Trilha']}")

            trilha_path = f"audio/{row['Trilha'].strip()}" # Caminho do arquivo do audio
            if os.path.exists(trilha_path):
                st.audio(trilha_path)
            else:
                st.info("🎧 Trilha sonora não encontrada.")

        # Link pra ver o trailers da Barbie
        with col3:
            trailer_link = row.get("Trailer", "").strip()
            if trailer_link:
                st.markdown(f"📺 [Ver trailer]({trailer_link})")
            else:
                st.info("🎬 Trailer não disponível.")
