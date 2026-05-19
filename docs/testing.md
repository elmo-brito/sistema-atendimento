# Plano de Testes e Estratégia de Validação

## 1. Testes Unitários

### 1.1 Modelos (ORM)
- **Cenário:** Validação de campos obrigatórios e únicos em `Usuario`.
- **Pré-condições:** Banco de dados de teste (SQLite em memória).
- **Passos:** Tentar criar um `Usuario` sem `email` ou com `email` duplicado.
- **Resultado esperado:** Levantamento de exceção `IntegrityError` ou erro de validação de modelo.

### 1.2 Regras de Negócio (SLA)
- **Cenário:** Cálculo de SLA para categoria específica e fallback global.
- **Pré-condições:** Categorias cadastradas com prazos de 24h e outra sem prazo.
- **Passos:** Criar solicitações em ambas as categorias e verificar o campo `prazo_sla`.
- **Resultado esperado:** 
    - Cat 24h: `criado_em + 24h`.
    - Sem prazo: `criado_em + 48h` (fallback global).

## 2. Testes de Integração

### 2.1 Fluxo de Atribuição Automática
- **Cenário:** Verificação da lógica de menor carga de trabalho.
- **Pré-condições:** Dois atendentes: Atendente A (1 chamado ativo), Atendente B (0 chamados ativos).
- **Passos:** Criar uma nova solicitação.
- **Resultado esperado:** A solicitação deve ser automaticamente atribuída ao Atendente B.

### 2.2 Reabertura de Chamado
- **Cenário:** Reabertura dentro do prazo de 7 dias e tentativa fora do prazo.
- **Pré-condições:** Solicitação encerrada com `atualizado_em` há 6 dias e outra há 8 dias.
- **Passos:** Tentar reabrir ambas.
- **Resultado esperado:** Sucesso para o de 6 dias; erro de "Prazo expirado" para o de 8 dias.

## 3. Testes de API (REST)

### 3.1 Autenticação via API
- **Cenário:** Login e obtenção de token/sessão.
- **Endpoint:** `POST /api/auth/login`.
- **Passos:** Enviar credenciais válidas e inválidas via JSON.
- **Resultado esperado:** 200 OK com dados do usuário (sucesso) ou 401 Unauthorized (falha).

### 3.2 Criação de Solicitação via API
- **Endpoint:** `POST /api/solicitacoes`.
- **Passos:** Enviar payload JSON com `categoria_id`, `titulo` e `descricao`.
- **Resultado esperado:** 201 Created e retorno do objeto com o protocolo gerado.

## 4. Testes de Permissão (RBAC)

### 4.1 Isolamento de Dados do Cliente
- **Cenário:** Cliente tentando acessar detalhes de um chamado que não é seu.
- **Passos:** Logar como Cliente A e tentar acessar `/solicitacao/<ID_DO_CLIENTE_B>`.
- **Resultado esperado:** Redirecionamento para index ou 403 Forbidden.

### 4.2 Acesso Administrativo
- **Cenário:** Cliente tentando acessar o painel administrativo.
- **Passos:** Tentar acessar `/admin/dashboard` com perfil `cliente`.
- **Resultado esperado:** Bloqueio de acesso (403 ou redirecionamento com erro).

### 4.3 Integridade do Acesso Admin
- **Cenário:** Verificação de que o administrador pode acessar todas as áreas administrativas.
- **Passos:** Logar como Administrador e acessar `/admin/usuarios`, `/admin/categorias` e `/admin/dashboard`.
- **Resultado esperado:** Acesso concedido (200 OK) e visualização correta dos dados.

## 5. Testes de Anexos

### 5.1 Validação de Extensão e Tamanho
- **Cenário:** Upload de arquivo `.exe` ou arquivo maior que 5MB.
- **Passos:** Tentar anexar os arquivos mencionados na abertura de chamado.
- **Resultado esperado:** Mensagem de erro "Extensão não permitida" ou "Arquivo muito grande".

## 6. Testes de Relatórios

### 6.1 Geração de CSV
- **Cenário:** Administrador exportando dados de volumetria.
- **Endpoint:** `GET /reports/export/volumetria`.
- **Resultado esperado:** Download de um arquivo `.csv` contendo as colunas Protocolo, Status e SLA.

## 7. Testes de Autenticação

### 7.1 Recuperação de Senha
- **Cenário:** Fluxo completo de recuperação.
- **Passos:** Solicitar recuperação -> Gerar Token -> Resetar senha -> Logar com nova senha.
- **Resultado esperado:** Sucesso em todas as etapas; token deve ser invalidado após o uso.

## 8. Testes de Regressão
- **Cenário:** Verificação pós-refatoração do Service de Atendimento.
- **Passos:** Executar toda a suíte de testes após alterações no `SolicitacaoService`.
- **Resultado esperado:** Zero falhas nos testes existentes.

## 9. Testes de Carga (Mínimos)
- **Cenário:** Simulação de múltiplos acessos simultâneos.
- **Passos:** 10 requisições simultâneas de criação de chamado.
- **Resultado esperado:** Tempo de resposta médio abaixo de 500ms e consistência nos protocolos gerados.
