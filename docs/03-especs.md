# Especificações do Sistema de Atendimento (SAC)

## 1. Requisitos

### 1.1 Requisitos Funcionais (RF)
* **RF001 - Autenticação:** Sistema de login seguro, cadastro de novos clientes e fluxo de recuperação de senha via token.
* **RF002 - Perfis de Acesso:** Suporte a três perfis distintos:
    * **Cliente:** Abre e acompanha suas próprias solicitações.
    * **Atendente:** Gerencia solicitações atribuídas e fila de atendimento.
    * **Administrador:** Controle total sobre usuários, categorias, configurações e relatórios.
* **RF003 - Abertura de Solicitações:** Cliente preenche título, descrição, seleciona categoria e pode anexar arquivos.
* **RF004 - Atribuição de Chamados:**
    * **Automática:** Baseada na menor carga de trabalho (atendente com menos chamados ativos).
    * **Manual:** Administradores podem reatribuir chamados a qualquer momento.
* **RF005 - SLA por Categoria:** Cada categoria possui um prazo de resolução em horas. O sistema calcula o vencimento automaticamente.
* **RF006 - Linha do Tempo (Timeline):** Visualização cronológica de todas as interações, mensagens, anexos e mudanças de status de um chamado.
* **RF007 - Upload de Anexos:** Suporte a múltiplos arquivos na abertura e durante a interação.
* **RF008 - Reabertura de Chamados:** Clientes podem reabrir chamados encerrados em até 7 dias após o fechamento.
* **RF009 - Avaliação do Atendimento:** Após a resolução, o cliente pode atribuir uma nota (1-5) e um comentário.
* **RF010 - Base de Conhecimento:** Repositório de artigos e FAQ para reduzir a abertura de chamados repetitivos.
* **RF011 - Dashboard do Cliente:** Resumo de chamados ativos, histórico e acesso rápido à abertura.
* **RF012 - Dashboard do Atendente:** Fila de trabalho, chamados aguardando resposta e métricas de SLA pessoal.
* **RF013 - Dashboard Administrativo:** Visão consolidada de volumetria, conformidade de SLA global e distribuição por status.
* **RF014 - Relatórios Avançados:** Filtros dinâmicos para exportação de dados detalhados.
* **RF015 - Gestão de Usuários:** Cadastro, edição, ativação/desativação e troca de perfil de usuários.
* **RF016 - Gestão de Categorias:** Criação e edição de categorias com definição de prazos SLA específicos.
* **RF017 - Gestão de SLA:** Configuração de SLA global de fallback (48h) e monitoramento de chamados vencidos.
* **RF018 - Notificações:** Sistema de alertas internos (na plataforma) e simulado por e-mail para mudanças de status.
* **RF019 - Logs e Auditoria:** Registro de trilha de auditoria para ações críticas (ex: deleção, alteração de permissão).
* **RF020 - Mobile-first:** Interface responsiva projetada prioritariamente para dispositivos móveis.
* **RF021 - Acessibilidade:** Uso de tags semânticas, contrastes adequados e compatibilidade com leitores de tela.
* **RF022 - Exportação de Relatórios:** Geração de arquivos CSV com dados operacionais.

### 1.2 Requisitos Não Funcionais (RNF)
* **RNF001 - Segurança:** Implementação de proteção contra CSRF, XSS e injeção de SQL.
* **RNF002 - Hash de Senha:** Uso de `werkzeug.security` (bcrypt/scrypt) para armazenamento de senhas.
* **RNF003 - Logs de Sistema:** Logs estruturados em nível de aplicação para depuração e segurança.
* **RNF004 - Testabilidade:** Código modular que permite alta cobertura de testes automatizados.
* **RNF005 - Modularidade:** Separação clara entre lógica de negócio (Services) e acesso a dados (Repositories).
* **RNF006 - Padrões REST:** API seguindo princípios RESTful (verbos corretos, códigos de status adequados).
* **RNF007 - Compatibilidade com Flask:** Projeto compatível com a versão 3.0+ do Flask.
* **RNF008 - Banco de Dados:** SQLite para desenvolvimento e testes; compatibilidade com PostgreSQL para produção.
* **RNF009 - Docker:** Containerização completa da aplicação para fácil deployment.
* **RNF010 - Performance:** Tempo de resposta médio das requisições abaixo de 200ms sob carga normal.
* **RNF011 - UX Responsiva:** Uso de frameworks modernos (Bootstrap) para fluidez em qualquer tela.

### 1.3 Regras de Negócio (RN)
* **RN001 - SLA por Categoria:** O prazo de resolução é definido pela categoria selecionada.
* **RN002 - SLA Global:** Caso a categoria não tenha prazo, o padrão é 48 horas úteis.
* **RN003 - Escalonamento:** Chamados que ultrapassam o SLA devem ser marcados visualmente e priorizados na fila administrativa.
* **RN004 - Regras de Reabertura:** Um chamado encerrado pode ser reaberto em 7 dias; após isso, deve-se abrir um novo.
* **RN005 - Regras de Encerramento:** Chamados sem interação do cliente por 5 dias (status "Aguardando Cliente") são encerrados automaticamente.
* **RN006 - Regras de Avaliação:** A avaliação é opcional, mas só pode ser feita uma vez por chamado "Resolvido".
* **RN007 - Permissões por Perfil:** 
    * **Cliente:** Apenas seus próprios dados.
    * **Atendente:** Seus chamados e fila comum.
    * **Admin:** Acesso irrestrito.
* **RN008 - Regras de Anexos:** Limite de 5MB por arquivo; extensões permitidas: PDF, JPG, PNG, DOCX, TXT.
* **RN009 - Regras de Prioridade:** Definida automaticamente pelo SLA (Menor prazo = Maior prioridade), mas ajustável pelo Admin.

## 2. Arquitetura

### 2.1 Estrutura MVC e Camadas
* **Models:** Entidades ORM que definem o esquema do banco de dados.
* **Views:** Blueprints Flask responsáveis pelo roteamento e renderização (HTML/JSON).
* **Controllers:** Lógica de controle de fluxo contida nas rotas das Views.
* **Services:** Onde reside 100% da lógica de negócio (ex: cálculo de SLA, atribuição).
* **Repositories:** Abstração para consultas SQLAlchemy, mantendo os Services limpos.

### 2.2 Padrões de Projeto
* **Repository Pattern:** Desacoplamento do ORM.
* **Service Layer:** Centralização da inteligência do sistema.
* **Dependency Injection (Manual):** Services injetados ou instanciados de forma controlada.

### 2.3 Organização de Pastas
```
/app
  /models       # Entidades SQLAlchemy
  /repositories # Consultas especializadas
  /services     # Lógica de negócio (o "coração" do sistema)
  /views        # Blueprints (auth, admin, solicitacoes, api)
  /templates    # Interface Jinja2
  /static       # Assets (CSS/JS)
  /utils        # Helpers (uploads, validadores)
```

### 2.4 Fluxos do Sistema
1. **Login:** Validação -> Criação de Sessão -> Redirecionamento por Perfil.
2. **Abertura de Chamado:** Seleção Categoria -> Geração Protocolo -> Cálculo SLA -> Atribuição -> Registro Timeline.
3. **SLA:** Monitoramento de tempo -> Alerta de Vencimento -> Escalonamento.
4. **Encerramento:** Mudança Status -> Liberação de Avaliação -> Registro Auditoria.

## 3. Modelos de Dados (ORM)

### Usuario
* `id` (int, PK), `nome` (str), `email` (str, Unique), `senha_hash` (str), `perfil` (enum), `ativo` (bool), `criado_em` (datetime).

### Solicitacao
* `id` (int, PK), `protocolo` (str, Unique), `cliente_id` (FK), `atendente_id` (FK, Nullable), `categoria_id` (FK), `titulo` (str), `descricao` (text), `status` (str), `prioridade` (str), `prazo_sla` (datetime), `criado_em` (datetime), `atualizado_em` (datetime).

### Categoria
* `id` (int, PK), `nome` (str, Unique), `descricao` (str), `prazo_horas` (int).

### Mensagem
* `id` (int, PK), `solicitacao_id` (FK), `usuario_id` (FK), `conteudo` (text), `criado_em` (datetime).

### Anexo
* `id` (int, PK), `mensagem_id` (FK), `caminho` (str), `nome_original` (str), `tipo` (str), `tamanho` (int).

### SLA
* `id` (int, PK), `solicitacao_id` (FK), `vencimento` (datetime), `cumprido` (bool), `resolvido_em` (datetime).

### LogAuditoria
* `id` (int, PK), `usuario_id` (FK, Nullable), `acao` (str), `tabela` (str), `registro_id` (int), `detalhes` (text), `ip` (str), `criado_em` (datetime).

## 4. Endpoints REST

| Método | URL | Descrição | Permissão | Status |
|---|---|---|---|---|
| POST | `/api/auth/register` | Cadastro de usuário | Público | 201 |
| POST | `/api/auth/login` | Login | Público | 200/401 |
| GET | `/api/solicitacoes` | Lista solicitações | Logado | 200 |
| POST | `/api/solicitacoes` | Cria solicitação | Logado | 201 |
| GET | `/api/solicitacoes/<id>` | Detalhes | Autorizado | 200 |
| POST | `/api/solicitacoes/<id>/mensagens` | Envia mensagem | Autorizado | 201 |
| GET | `/admin/dashboard` | Dados do dashboard | Admin | 200 |

## 5. Critérios de Aceite
1. **Login:** Acesso garantido apenas com credenciais válidas e perfil correto.
2. **SLA:** Prazo calculado deve ser `data_criacao + horas_categoria`.
3. **Atribuição:** Novo chamado deve cair para o atendente com menos chamados "Em Aberto".
4. **Mobile:** Layout não deve ter scroll horizontal em telas de 375px.
