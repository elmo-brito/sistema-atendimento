# Relatório de Refatoração e Otimização

## Alterações Realizadas

### 1. Centralização da Lógica de Tempo (UTC)
- Criado utilitário `app/utils/datetime_utils.py` com a função `utc_now()`.
- Refatorado `app/services/solicitacao_service.py` para utilizar `utc_now()`, eliminando chamadas repetitivas e verbosas a `datetime.now(timezone.utc).replace(tzinfo=None)`.
- Garante consistência em todo o sistema para cálculos de SLA e registros de data.

### 2. Implementação de Cache
- Adicionado `Flask-Caching` ao projeto.
- Implementado cache no `CategoriaRepository` para as funções `get_all` e `get_by_id`.
- Reduz o número de consultas ao banco de dados para dados que mudam raramente (Categorias), melhorando o tempo de resposta das telas de abertura e listagem de chamados.

### 3. Preparação para Processamento em Segundo Plano
- Adicionado `Flask-Executor` para permitir a execução de tarefas assíncronas no futuro.
- A infraestrutura está pronta para mover notificações e processamentos pesados para threads separadas sem bloquear a requisição do usuário.

### 4. Modularização e Limpeza
- Atualizado `requirements.txt` com as novas dependências.
- Atualizado `app/__init__.py` para inicializar as novas extensões.

## Impacto na Performance
- Redução de latência em rotas que consultam categorias repetidamente.
- Código mais limpo e fácil de manter (DRY - Don't Repeat Yourself).
- Preparado para escalabilidade com suporte a jobs em background.
