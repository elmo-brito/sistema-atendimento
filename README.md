# Sistema de Atendimento (SAC)

Projeto de gestão de chamados desenvolvido em Python com Flask, seguindo arquitetura modular (MVC + Services + Repositories).

## Tecnologias
- **Python 3.10+**
- **Flask 3.0**: Framework web
- **SQLAlchemy**: ORM para persistência
- **Flask-Migrate**: Controle de versões de banco de dados
- **Flask-Login**: Gestão de autenticação e sessões
- **SQLite**: Banco de dados para desenvolvimento
- **Pytest**: Suíte de testes automatizados

## Estrutura do Projeto
- `app/models/`: Entidades do banco de dados.
- `app/repositories/`: Camada de acesso a dados (consultas).
- `app/services/`: Lógica de negócio e regras de SLA.
- `app/views/`: Controladores e rotas (Blueprints).
- `app/templates/`: Interface do usuário (Jinja2).
- `docs/`: Documentação de requisitos e testes.
- `tests/`: Casos de teste automatizados.

## Instalação e Execução

1. **Ambiente Virtual**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Banco de Dados**:
   ```bash
   export FLASK_APP=run.py
   flask db upgrade
   ```

4. **Executar**:
   ```bash
   python3 run.py
   ```
   Acesse: `http://127.0.0.1:5000`

## Funcionalidades Principais
- Autenticação com perfis (Cliente, Atendente, Admin).
- Abertura de chamados com protocolo único.
- Cálculo automático de SLA por categoria.
- Atribuição inteligente (atendente com menor carga).
- Histórico e linha do tempo de interações.
- Upload de anexos.
- Reabertura de chamados em até 7 dias.
- Dashboards específicos por perfil.
- Relatórios em CSV.
- Base de Conhecimento (FAQ).

## Testes
Para rodar a suíte de testes:
```bash
pytest
```

## Comandos Úteis
- Criar migração: `flask db migrate -m "descrição"`
- Aplicar migração: `flask db upgrade`
- Shell interativo: `flask shell`
