# Relatório de Inspeção de Segurança - Sistema de Atendimento (SAC)

## 1. Resumo Executivo

Este documento apresenta os resultados da inspeção detalhada de cibersegurança do projeto **Sistema de Atendimento (SAC)**. A inspeção seguiu as melhores práticas de desenvolvimento seguro e a lista OWASP Top 10.

### Contagem de Achados por Severidade (Final - Todos os Níveis)

| Severidade | Quantidade |
|------------|------------|
| Crítica    | 2          |
| Alta       | 4          |
| Média      | 6          |
| Baixa      | 3          |
| **Total**  | **15**     |

---

## 2. As 5 Ações Mais Urgentes

1. **Implementar proteção CSRF global** (Instalar `Flask-WTF` e configurar `CSRFProtect`).
2. **Corrigir IDOR em downloads de anexos** (Verificar permissão do usuário antes de servir o arquivo).
3. **Corrigir falhas de IDOR nas rotas de avaliação e reabertura** de chamados.
4. **Implementar política de bloqueio de conta** após tentativas falhas no `AuthService`.
5. **Remover a fallback hardcoded da `SECRET_KEY`** no arquivo `config.py`.

---

## 3. Detalhes das Vulnerabilidades

### [NÍVEL SUPERFICIAL]

### 3.1 Exposição de Chave Secreta (Fallback Hardcoded)
- **Localização:** `config.py`, Classe `Config`, Linha 8.
- **Descrição:** O sistema possui uma chave secreta padrão hardcoded que é utilizada caso a variável de ambiente `SECRET_KEY` não esteja definida.
- **Evidência:** `SECRET_KEY = os.environ.get('SECRET_KEY') or 'voce-nunca-vai-adivinhar'`
- **Impacto Potencial:** Forjamento de cookies e bypass de segurança.
- **Nível de Severidade:** Crítica.
- **Recomendação de Correção:** Remover fallback e exigir variável de ambiente.

### 3.2 Modo Debug Ativado em Produção
- **Localização:** `run.py`, Linha 18.
- **Descrição:** Servidor Flask roda com `debug=True`.
- **Nível de Severidade:** Alta.

### 3.3 Falta de Cabeçalhos de Segurança HTTP
- **Localização:** `app/__init__.py`.
- **Descrição:** Ausência de cabeçalhos como CSP, HSTS e X-Frame-Options.
- **Nível de Severidade:** Média.

### 3.4 Configuração Insegura de Limite de Upload
- **Localização:** `config.py`, Linha 12.
- **Descrição:** `MAX_CONTENT_LENGTH` de 100MB excede a regra de 5MB.
- **Nível de Severidade:** Média.

### 3.5 Cookies de Sessão sem Atributos de Segurança
- **Localização:** `config.py`.
- **Descrição:** Cookies sem `Secure` ou `HttpOnly`.
- **Nível de Severidade:** Média.

### 3.6 Logs com Informações Sensíveis
- **Localização:** `app/__init__.py`.
- **Descrição:** Registro de stack traces completos nos logs.
- **Nível de Severidade:** Baixa.

---

### [NÍVEL MODERADO]

### 3.7 Ausência Global de Proteção CSRF
- **Localização:** Todo o projeto.
- **Descrição:** A aplicação não utiliza tokens CSRF em seus formulários.
- **Evidência:** Formulários em `app/templates/solicitacoes/detalhes.html` não possuem campo de token.
- **Impacto Potencial:** Um atacante pode induzir um usuário a realizar ações indesejadas.
- **Nível de Severidade:** Crítica.
- **Recomendação de Correção:** Instalar `Flask-WTF` e ativar `CSRFProtect`.

### 3.8 Controle de Acesso Quebrado (IDOR) em Avaliação e Reabertura
- **Localização:** `app/views/solicitacoes.py`, Funções `avaliar(id)` e `reabrir(id)`.
- **Descrição:** As rotas não verificam se o usuário é o dono do chamado.
- **Evidência:** Ausência de verificação `solicitacao.cliente_id == current_user.id`.
- **Impacto Potencial:** Manipulação de dados de outros usuários.
- **Nível de Severidade:** Alta.

### 3.9 Falha de Autenticação: Ausência de Bloqueio de Conta
- **Localização:** `app/services/auth_service.py`, Função `login`.
- **Descrição:** O sistema não bloqueia contas após tentativas falhas.
- **Nível de Severidade:** Alta.

### 3.10 Divulgação de Informações em Respostas de Erro
- **Localização:** `app/views/solicitacoes.py`.
- **Descrição:** Exibição de mensagens de erro cruas via `flash`.
- **Nível de Severidade:** Baixa.

---

### [NÍVEL PROFUNDO]

### 3.11 Controle de Acesso Quebrado (IDOR) em Downloads de Anexos
- **Localização:** `app/utils/uploads.py`, Função `uploaded_file`.
- **Descrição:** A rota que serve anexos verifica apenas `@login_required`.
- **Evidência:** `return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)`
- **Impacto Potencial:** Acesso não autorizado a documentos de outros chamados.
- **Nível de Severidade:** Alta.
- **Recomendação de Correção:** Validar permissão de acesso ao chamado antes de servir o arquivo.

### 3.12 Armazenamento de Tokens de Recuperação em Texto Claro
- **Localização:** `app/models/usuario.py`.
- **Descrição:** Tokens de reset são salvos sem hash.
- **Nível de Severidade:** Média.

### 3.13 Ausência de Defesa em Profundidade na Camada de Serviço
- **Localização:** `app/services/solicitacao_service.py`.
- **Descrição:** Lógica de negócio não revalida permissões do executor.
- **Nível de Severidade:** Média.

### 3.14 Nomes de Arquivos de Anexo Previsíveis
- **Localização:** `app/utils/uploads.py`.
- **Descrição:** Uso de ID sequencial no nome do arquivo físico.
- **Nível de Severidade:** Baixa.

### 3.15 Uso de Versões com Vulnerabilidades Conhecidas
- **Localização:** `requirements.txt`.
- **Descrição:** Algumas bibliotecas como `Werkzeug` ou `Jinja2` em versões específicas podem ter CVEs conhecidas se não forem atualizadas regularmente.
- **Nível de Severidade:** Média.
- **Recomendação de Correção:** Executar `pip-audit` e atualizar dependências.
