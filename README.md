
# Aplicação Streamlit que busca dados de qualquer API REST (com suporte a autenticação) e exporta para Excel.

![Demo](https://api-to-excel.streamlit.app/)

## 🚀 Funcionalidades
- Suporta **qualquer API REST** (respostas JSON)
- Manipula:
  - Objetos únicos (`/endpoint/1`)
  - Arrays de objetos (`/endpoint`)
  - Respostas paginadas (`/endpoint?page=1`)
- Métodos de autenticação:
  - 🔑 Autenticação Básica
  - 🪙 Token Bearer
  - 🔐 Chave API
- Normalização automática de dados
- Exportação limpa para Excel com colunas formatadas

## 🛠️ Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/yourusername/api-to-excel.git
   cd api-to-excel
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

## 🧑‍💻 Uso
1. Insira a URL do endpoint da API
2. Selecione o tipo de autenticação (se necessário)
3. Clique em "Coletar e Exportar"
4. Visualize os dados e baixe o arquivo Excel

## 🧪 APIs Testadas
| API | URL de Exemplo | Tipo |
|-----|----------------|------|
| JSONPlaceholder | `https://jsonplaceholder.typicode.com/posts` | Array |
| SWAPI | `https://swapi.dev/api/people/` | Paginada |
| Dog API | `https://dog.ceo/api/breeds/image/random` | Objeto Único |
| BrasilAPI | `https://brasilapi.com.br/api/cep/v2/01001000` | Objeto Único |

## 🤝 Contribuindo
1. Faça um fork do projeto
2. Crie sua branch de funcionalidade (`git checkout -b feature/FuncionalidadeIncrível`)
3. Faça o commit das suas alterações (`git commit -m 'Adicionar funcionalidade incrível'`)
4. Faça o push para a branch (`git push origin feature/FuncionalidadeIncrível`)
5. Abra um Pull Request

## 📜 Licença
Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.

## 📧 Contato
Geraldo - geraldoaugustodf@gmail.com

Link do Projeto: [https://github.com/geraldok7/api-to-excel]
