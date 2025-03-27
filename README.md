# Aplicacao Streamlit que busca dados de qualquer API REST (com suporte a autenticacao) e exporta para Excel.

Demo: https://api-to-excel.streamlit.app/

## 🚀 Funcionalidades
- Suporta **qualquer API REST** (respostas JSON)
- Manipula:
  - Objetos unicos (`/endpoint/1`)
  - Arrays de objetos (`/endpoint`)
  - Respostas paginadas (`/endpoint?page=1`)
- Metodos de autenticacao:
  - 🔑 Autenticacao Basica
  - 🧩 Token Bearer
  - 🔐 Chave API
- Normalizacao automatica de dados
- Exportacao limpa para Excel com colunas formatadas

## 🛠️ Instalacao

### Metodo Local
1. Clone o repositorio:
   ```bash
   git clone https://github.com/geraldok7/api-to-excel.git
   cd api-to-excel
   ```
2. Instale as dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicacao:
   ```bash
   streamlit run app.py
   ```

### Metodo Docker (Recomendado)
1. Construa a imagem:
   ```bash
   docker build -t api-to-excel .
   ```
2. Execute o container:
   ```bash
   docker run -p 8501:8501 api-to-excel
   ```
3. Acesse no navegador:
   ```
   http://localhost:8501
   ```

## 🐳 Configuracao Docker Avancada
Para producao, utilize docker-compose:

1. Crie um arquivo .env (opcional):
   ```
   API_USER=seu_usuario
   API_PASS=sua_senha
   ```
2. Execute:
   ```bash
   docker-compose up -d --build
   ```

## 🧑‍💻 Uso
1. Insira a URL do endpoint da API
2. Selecione o tipo de autenticacao (se necessario)
3. Clique em "Coletar e Exportar"
4. Visualize os dados e baixe o arquivo Excel

## 🧪 APIs Testadas

| API             | URL de Exemplo                                       | Tipo         |
|---------------|-------------------------------------------------|-------------|
| JSONPlaceholder | https://jsonplaceholder.typicode.com/posts    | Array       |
| SWAPI          | https://swapi.dev/api/people/                  | Paginada    |
| Dog API       | https://dog.ceo/api/breeds/image/random        | Objeto Unico |
| BrasilAPI     | https://brasilapi.com.br/api/cep/v2/01001000   | Objeto Unico |
| IBGE          | https://servicodados.ibge.gov.br/api/v1/localidades/estados | Array       |

## 🤝 Contribuindo
1. Faca um fork do projeto
2. Crie sua branch de funcionalidade (`git checkout -b feature/FuncionalidadeIncrivel`)
3. Faca o commit das suas alteracoes (`git commit -m 'Adicionar funcionalidade incrivel'`)
4. Faca o push para a branch (`git push origin feature/FuncionalidadeIncrivel`)
5. Abra um Pull Request

## 📝 Licenca
Distribuido sob a Licenca MIT. Veja LICENSE para mais informacoes.

## 📧 Contato
Geraldo - geraldoaugustodf@gmail.com

Link do Projeto: [https://github.com/geraldok7/api-to-excel]
