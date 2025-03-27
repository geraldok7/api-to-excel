# Estágio de construção
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --user -r requirements.txt

# Estágio final
FROM python:3.9-slim

WORKDIR /app

# Copia apenas o necessário do estágio de construção
COPY --from=builder /root/.local /root/.local
COPY . .

# Garante que os scripts do usuário estarão no PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Porta padrão do Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]