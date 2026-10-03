import os
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string

# Carrega as variáveis de ambiente declaradas no arquivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'onixbase-default-dev-secret-key')

# Configuração de conexão obtida com segurança via variáveis de ambiente
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'wrross'),
    'passwd': os.getenv('DB_PASS', 'pedrelina123'),
    'db': os.getenv('DB_NAME', 'meu_site_db'),
    'charset': 'utf8mb4'
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OnixBase - Online</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 1.5rem;
        }
        .card {
            background: #1e293b;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
            text-align: center;
            max-width: 480px;
            width: 100%;
            border: 1px solid #334155;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 0.75rem;
            color: #38bdf8;
        }
        p {
            color: #94a3b8;
            font-size: 1rem;
            margin-bottom: 1rem;
            line-height: 1.5;
        }
        .status-badge {
            display: inline-block;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.95rem;
        }
        .status-ok {
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        .status-error {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>OnixBase</h1>
        <p>Servidor Nginx + Gunicorn rodando com sucesso!</p>
        <p>
            Status do Banco de Dados: 
            <span class="status-badge {{ 'status-ok' if status == 'Conectado' else 'status-error' }}">
                {{ status }}
            </span>
        </p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    status = "Erro na conexão"
    try:
        conn = MySQLdb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        cursor.close()
        conn.close()
        status = "Conectado"
    except Exception as e:
        status = f"Erro: {str(e)}"
    
    return render_template_string(HTML_TEMPLATE, status=status)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "project": "OnixBase"})

if __name__ == '__main__':
    # Roda localmente na porta 8000 para testes no seu PC
    app.run(host='127.0.0.1', port=8000, debug=True)