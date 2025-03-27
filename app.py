import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Coletor de API para Excel", page_icon="📊")

# Funções principais
def fetch_data_from_api(api_url, auth_type=None, credentials=None):
    """Coleta dados de uma API usando método GET com autenticação"""
    try:
        if auth_type == 'basic':
            response = requests.get(
                api_url,
                auth=(credentials['username'], credentials['password'])
            )
        elif auth_type == 'bearer':
            headers = {'Authorization': f"Bearer {credentials['token']}"}
            response = requests.get(api_url, headers=headers)
        elif auth_type == 'api_key':
            params = {credentials['key_name']: credentials['key_value']}
            response = requests.get(api_url, params=params)
        else:
            response = requests.get(api_url)
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a API: {e}")
        return None

def transform_to_dataframe(api_data):
    """Transforma os dados da API em um DataFrame estruturado"""
    if not api_data:
        return None
    
    df = pd.DataFrame(api_data)
    df['data_coleta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return df

# Interface Streamlit
st.title("📊 Coletor de API para Excel")

with st.expander("🔧 Configurações", expanded=True):
    api_url = st.text_input(
        "URL da API",
        value="https://jsonplaceholder.typicode.com/posts",
        help="Insira a URL completa do endpoint da API"
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

# Botão para executar a coleta
if st.button("Coletar Dados e Exportar para Excel", type="primary"):
    if not api_url:
        st.warning("Por favor, insira a URL da API")
        st.stop()
    
    if auth_type != "Nenhuma" and not all(credentials.values()):
        st.warning("Por favor, preencha todas as credenciais de autenticação")
        st.stop()
    
    with st.spinner("Coletando dados da API..."):
        # Mapeia a seleção do usuário para os valores internos
        auth_mapping = {
            "Nenhuma": None,
            "Basic Auth": "basic",
            "Bearer Token": "bearer",
            "API Key": "api_key"
        }
        
        api_data = fetch_data_from_api(
            api_url,
            auth_type=auth_mapping[auth_type],
            credentials=credentials
        )
    
    if api_data:
        st.success(f"✅ Dados coletados com sucesso! Total de registros: {len(api_data)}")
        
        with st.spinner("Processando dados..."):
            df = transform_to_dataframe(api_data)
            
            # Mostra uma prévia dos dados
            st.subheader("Prévia dos Dados")
            st.dataframe(df.head(), use_container_width=True)
            
            # Cria o arquivo Excel em memória
            excel_file = pd.ExcelWriter("dados_api.xlsx", engine='openpyxl')
            df.to_excel(excel_file, index=False, sheet_name='Dados_API')
            excel_file.close()
            
            # Disponibiliza para download
            with open("dados_api.xlsx", "rb") as file:
                st.download_button(
                    label="⬇️ Baixar Arquivo Excel",
                    data=file,
                    file_name="dados_api.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.error("Falha ao coletar dados da API. Verifique as credenciais e tente novamente.")

# Rodapé
st.markdown("---")
st.caption("Desenvolvido com Python, Streamlit e ❤️")