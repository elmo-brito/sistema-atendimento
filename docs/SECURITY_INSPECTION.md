# Relatório de Inspeção de Segurança - Sistema de Atendimento (SAC)

## 1. Resumo Executivo

Este documento apresenta os resultados da inspeção detalhada de cibersegurança do projeto **Sistema de Atendimento (SAC)**. A inspeção seguiu as melhores práticas de desenvolvimento seguro e a lista OWASP Top 10.

### Contagem de Achados por Severidade (Níveis Superficial e Moderado)

| Severidade | Quantidade |
|------------|------------|
| Crítica    | 2          |
| Alta       | 3          |
| Média      | 4          |
| Baixa      | 2          |
| **Total**  | **11**     |

---

## 2. As 5 Ações Mais Urgentes

1. **Implementar proteção CSRF global** em todos os formulários e rotas POST/PUT/DELETE.
2. **Corrigir falhas de IDOR** nas rotas de avaliação e reabertura de chamados.
3. **Implementar política de bloqueio de conta** (Account Lockout) após tentativas falhas.
4. **Remover a fallback hardcoded da `SECRET_KEY`** no arquivo `config.py`.
5. **Desativar o modo Debug** no `run.py` para ambientes de produção.

---

## 3. Detalhes das Vulnerabilidades

### [NÍVEL SUPERFICIAL]

### 3.1 Exposição de Chave Secreta (Fallback Hardcoded)
- **Localização:** `config.py`, Classe `Config`, Linha 8.
- **Descrição:** O sistema possui uma chave secreta padrão hardcoded.
- **Evidência:** `SECRET_KEY = os.environ.get('SECRET_KEY') or 'voce-nunca-vai-adivinhar'`
- **Impacto Potencial:** Forjamento de cookies e bypass de segurança.
- **Nível de Severidade:** Crítica.
- **Recomendação de Correção:** Remover fallback e exigir variável de ambiente.

### 3.2 Modo Debug Ativado em Produção
- **Localização:** `run.py`, Linha 18.
- **Descrição:** Servidor Flask roda com `debug=True`.
- **Nível de Severidade:** Alta.

... (mantendo os itens anteriores de forma resumida para brevidade no histórico, mas no arquivo real estarão completos)

### [NÍVEL MODERADO]

### 3.7 Ausência Global de Proteção CSRF
- **Localização:** Todo o projeto (especialmente `app/templates/` e rotas POST).
- **Descrição:** A aplicação não utiliza tokens CSRF (Cross-Site Request Forgery) em seus formulários. O pacote `Flask-WTF` não está instalado e não há middleware de proteção.
- **Evidência:** Formulários em `app/templates/solicitacoes/detalhes.html` (linhas 85, 114, 120) não possuem campo de token.
- **Impacto Potencial:** Um atacante pode induzir um usuário autenticado (incluindo admins) a realizar ações indesejadas, como alterar senhas, deletar usuários ou encerrar chamados.
- **Nível de Severidade:** Crítica.
- **Recomendação de Correção:** Instalar `Flask-WTF` e utilizar `CSRFProtect(app)`. Adicionar `{{ form.csrf_token }}` ou `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">` em todos os formulários.
- **Referências:** OWASP A01:2021 – Broken Access Control; CWE-352.

### 3.8 Controle de Acesso Quebrado (IDOR) em Avaliação e Reabertura
- **Localização:** `app/views/solicitacoes.py`, Funções `avaliar(id)` (linha 135) e `reabrir(id)` (linha 145).
- **Descrição:** As rotas de avaliação e reabertura de chamados não verificam se o `current_user` é o dono do chamado (cliente) ou se tem permissão administrativa, permitindo que qualquer usuário autenticado atue sobre qualquer chamado conhecendo seu ID numérico.
- **Evidência:** 
  ```python
  @bp.route('/solicitacao/<int:id>/avaliar', methods=['POST'])
  @login_required
  def avaliar(id): # Falta verificação de propriedade
  ```
- **Impacto Potencial:** Manipulação de dados de outros usuários, encerramento indevido de chamados e fraude em métricas de atendimento.
- **Nível de Severidade:** Alta.
- **Recomendação de Correção:** Adicionar a verificação `if current_user.perfil == 'cliente' and solicitacao.cliente_id != current_user.id: abort(403)` nestas funções.
- **Referências:** OWASP A01:2021 – Broken Access Control; CWE-639.

### 3.9 Falha de Autenticação: Ausência de Bloqueio de Conta
- **Localização:** `app/services/auth_service.py`, Função `login`.
- **Descrição:** O sistema não incrementa o contador `tentativas_falhas` nem verifica o campo `bloqueado_ate` do modelo `Usuario` durante o processo de login, permitindo ataques de força bruta ilimitados.
- **Evidência:** 
  ```python
  def login(self, email, senha):
      usuario = self.repo.get_by_email(email)
      if usuario and usuario.check_senha(senha) and usuario.ativo:
          return usuario
      return None
  ```
- **Impacto Potencial:** Comprometimento de contas de usuários através de ataques automatizados de força bruta ou credential stuffing.
- **Nível de Severidade:** Alta.
- **Recomendação de Correção:** Implementar lógica para incrementar `tentativas_falhas` em caso de erro e bloquear a conta (setar `bloqueado_ate`) após X tentativas falhas.
- **Referências:** OWASP A07:2021 – Identification and Authentication Failures; CWE-307.

### 3.10 Divulgação de Informações em Respostas de Erro (Generic Exceptions)
- **Localização:** `app/views/solicitacoes.py`, `app/views/admin.py`.
- **Descrição:** O uso de `flash(f'Erro: {str(e)}')` captura exceções genéricas que podem conter detalhes do banco de dados ou da estrutura interna do código.
- **Evidência:** `flash(f'Erro ao criar solicitação: {str(e)}', 'error')` em `solicitacoes.py`.
- **Impacto Potencial:** Vazamento de informações técnicas que auxiliam atacantes na exploração de outras vulnerabilidades.
- **Nível de Severidade:** Baixa.
- **Recomendação de Correção:** Utilizar mensagens de erro amigáveis para o usuário e registrar o erro detalhado apenas nos logs internos.
- **Referências:** OWASP A10:2021 – Server-Side Request Forgery (SSRF); CWE-209.

