from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.crud_routes import crud_bp
from app.database import get_db_connection

app = Flask(__name__)

# 🔹 Registrando as Rotas
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(crud_bp, url_prefix="/")

# 🔹 Teste de conexão com o banco
@app.route("/health")
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "API Rodando e conectada ao banco!"}, 200
    except Exception as e:
        return {"status": "Erro ao conectar ao banco!", "erro": str(e)}, 500

# 🔹 Iniciando a API
if __name__ == "__main__":
    app.run(debug=True)
