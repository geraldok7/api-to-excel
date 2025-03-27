import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from urllib.parse import urlparse

st.set_page_config(page_title="Universal API to Excel", page_icon="📊")

def fetch_data_from_api(api_url, auth_type=None, credentials=None):
    """Coleta dados de uma API com tratamento para diferentes formatos"""
    try:
        # Configura a autenticação
        params = {}
        headers = {}
        auth = None

        if auth_type == 'basic':
            auth = (credentials['username'], credentials['password'])
        elif auth_type == 'bearer':
            headers['Authorization'] = f"Bearer {credentials['token']}"
        elif auth_type == 'api_key':
            params[credentials['key_name']] = credentials['key_value']

        # Faz a requisição
        response = requests.get(api_url, auth=auth, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Verifica se é uma API paginada (como SWAPI)
        if isinstance(data, dict) and 'results' in data:
            return handle_paginated_data(api_url, data, auth, headers, params)
        
        return data
    
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a API: {e}")
        return None

def handle_paginated_data(base_url, first_page, auth, headers, params):
    """Lida com APIs paginadas"""
    all_data = first_page['results']
    next_url = first_page.get('next')
    
    while next_url:
        try:
            response = requests.get(next_url, auth=auth, headers=headers, params=params)
            response.raise_for_status()
            page_data = response.json()
            all_data.extend(page_data.get('results', []))
            next_url = page_data.get('next')
        except requests.exceptions.RequestException:
            break
    
    return all_data

def normalize_data(api_data):
    """Normaliza diferentes formatos de resposta para um DataFrame"""
    if not api_data:
        return None
    
    # Se for um dicionário único, converte para lista
    if isinstance(api_data, dict):
        # Verifica se é um endpoint que retorna um único item (como /people/1/)
        if not any(key.isdigit() for key in api_data.keys()):  # Não parece ser um item em lista
            api_data = [api_data]
    
    # Se ainda não for uma lista, força conversão
    if not isinstance(api_data, list):
        api_data = [api_data]
    
    return api_data

def transform_to_dataframe(api_data):
    """Transforma os dados normalizados em DataFrame"""
    normalized_data = normalize_data(api_data)
    if not normalized_data:
        return None
    
    try:
        df = pd.json_normalize(normalized_data)
        df['data_coleta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return df
    except Exception as e:
        st.error(f"Erro ao transformar dados: {e}")
        return None

def export_to_excel(df, output_file):
    """Exporta o DataFrame para Excel"""
    if df is not None and not df.empty:
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Dados_API')
                
                # Ajusta largura das colunas
                for column in df:
                    col_width = max(df[column].astype(str).map(len).max(), len(column)) + 2
                    col_idx = df.columns.get_loc(column)
                    writer.sheets['Dados_API'].column_dimensions[chr(65 + col_idx)].width = col_width
            
            return True
        except Exception as e:
            st.error(f"Erro ao exportar Excel: {e}")
            return False
    else:
        st.warning("Nenhum dado válido para exportar")
        return False

# Interface Streamlit
st.title("📊 Universal API to Excel Converter")

with st.expander("🔧 Configurações", expanded=True):
    api_url = st.text_input(
        "URL da API",
        value="https://jsonplaceholder.typicode.com/posts",
        help="Insira a URL completa do endpoint"
    )
    
    auth_type = st.radio(
        "Tipo de autenticação",
        options=["Nenhuma", "Basic Auth", "Bearer Token", "API Key"],
        horizontal=True
    )
    
    credentials = {}
    if auth_type == "Basic Auth":
        col1, col2 = st.columns(2)
        credentials['username'] = col1.text_input("Usuário")
        credentials['password'] = col2.text_input("Senha", type="password")
    elif auth_type == "Bearer Token":
        credentials['token'] = st.text_input("Token", type="password")
    elif auth_type == "API Key":
        col1, col2 = st.columns(2)
        credentials['key_name'] = col1.text_input("Nome do parâmetro", value="api_key")
        credentials['key_value'] = col2.text_input("Valor da chave", type="password")

if st.button("Coletar e Exportar", type="primary"):
    if not api_url:
        st.warning("Por favor, insira a URL da API")
        st.stop()
    
    # Mapeia a seleção para valores internos
    auth_mapping = {
        "Nenhuma": None,
        "Basic Auth": "basic",
        "Bearer Token": "bearer",
        "API Key": "api_key"
    }
    
    with st.spinner("Coletando dados..."):
        api_data = fetch_data_from_api(
            api_url,
            auth_type=auth_mapping[auth_type],
            credentials=credentials if auth_type != "Nenhuma" else None
        )
    
    if api_data:
        with st.spinner("Processando dados..."):
            df = transform_to_dataframe(api_data)
            
            if df is not None:
                st.success(f"✅ Dados coletados com sucesso! {len(df)} registros")
                
                # Mostra prévia
                st.subheader("Prévia dos Dados")
                st.dataframe(df.head(), use_container_width=True)
                
                # Exporta para Excel
                excel_file = "dados_api.xlsx"
                if export_to_excel(df, excel_file):
                    with open(excel_file, "rb") as f:
                        st.download_button(
                            "⬇️ Baixar Excel",
                            f,
                            file_name=excel_file,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

# Exemplos de APIs
with st.expander("🔍 Exemplos de APIs para testar"):
    st.markdown("""
    **APIs públicas para teste:**
    - 🌐 [JSONPlaceholder](https://jsonplaceholder.typicode.com/posts) (dados fictícios)
    - ⭐ [SWAPI (Star Wars)](https://swapi.dev/api/people/) (paginada)
    - 🐕 [Dog API](https://dog.ceo/api/breeds/image/random) (retorno único)
    - 🏛️ [Brasil API](https://brasilapi.com.br/api/cep/v2/01001000) (retorno único)
    - 📰 [NewsAPI](https://newsapi.org/v2/top-headlines?country=us) (requer chave)
    """)

st.markdown("---")
st.caption("Desenvolvido por Geraldok7 com Python e Streamlit | Dúvidas? Consulte o [GitHub](https://github.com/geraldok7/api-to-excel)")