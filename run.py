from app import create_app, db
from app.models import Usuario, Solicitacao, Categoria, Mensagem, Anexo, Historico

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Usuario': Usuario,
        'Solicitacao': Solicitacao,
        'Categoria': Categoria,
        'Mensagem': Mensagem,
        'Anexo': Anexo,
        'Historico': Historico
    }

if __name__ == '__main__':
    app.run(debug=True)
