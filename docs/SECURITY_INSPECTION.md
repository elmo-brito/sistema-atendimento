# Relatório de Inspeção de Segurança - Sistema de Atendimento (SAC)

## 1. Resumo Executivo

Este documento apresenta os resultados da inspeção detalhada de cibersegurança do projeto **Sistema de Atendimento (SAC)**. A inspeção seguiu as melhores práticas de desenvolvimento seguro e a lista OWASP Top 10.

### Contagem de Achados por Severidade (Nível Superficial)

| Severidade | Quantidade |
|------------|------------|
| Crítica    | 1          |
| Alta       | 1          |
| Média      | 3          |
| Baixa      | 1          |
| **Total**  | **6**      |

---

## 2. As 5 Ações Mais Urgentes

1. **Remover a fallback hardcoded da `SECRET_KEY`** no arquivo `config.py`.
2. **Desativar o modo Debug** no `run.py` para ambientes de produção.
3. **Implementar cabeçalhos de segurança HTTP** (HSTS, CSP, X-Frame-Options).
4. **Configurar cookies de sessão seguros** (`Secure`, `HttpOnly`, `SameSite`).
5. **Reduzir o `MAX_CONTENT_LENGTH`** para alinhar com a regra de negócio de 5MB.

---

## 3. Detalhes das Vulnerabilidades (Nível Superficial)

### 3.1 Exposição de Chave Secreta (Fallback Hardcoded)
- **Localização:** `config.py`, Classe `Config`, Linha 8.
- **Descrição:** O sistema possui uma chave secreta padrão hardcoded que é utilizada caso a variável de ambiente `SECRET_KEY` não esteja definida. Isso compromete a integridade das sessões e tokens JWT.
- **Evidência:** 
  ```python
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'voce-nunca-vai-adivinhar'
  ```
- **Impacto Potencial:** Um atacante que conheça a chave padrão pode forjar cookies de sessão, sequestrar contas de usuários (inclusive administradores) e contornar proteções CSRF.
- **Nível de Severidade:** Crítica.
- **Recomendação de Correção:** Remova o fallback. O sistema deve falhar ao iniciar se a `SECRET_KEY` não for fornecida via variável de ambiente.
- **Referências:** OWASP A02:2021 – Security Misconfiguration; CWE-798.

### 3.2 Modo Debug Ativado em Produção
- **Localização:** `run.py`, Linha 18.
- **Descrição:** O servidor Flask está configurado para rodar em modo `debug=True`.
- **Evidência:** 
  ```python
  if __name__ == '__main__':
      app.run(debug=True)
  ```
- **Impacto Potencial:** O modo debug expõe um console interativo e detalhes da stack trace em caso de erro, permitindo execução remota de código (RCE) se acessado por um atacante.
- **Nível de Severidade:** Alta.
- **Recomendação de Correção:** Altere para `debug=False` ou utilize variáveis de ambiente para controlar o estado do debug.
- **Referências:** OWASP A02:2021 – Security Misconfiguration; CWE-489.

### 3.3 Falta de Cabeçalhos de Segurança HTTP
- **Localização:** `app/__init__.py`, Função `create_app`.
- **Descrição:** A aplicação não configura explicitamente cabeçalhos de segurança fundamentais como Content-Security-Policy (CSP), Strict-Transport-Security (HSTS), X-Content-Type-Options e X-Frame-Options.
- **Evidência:** Ausência de middleware ou extensões como `Flask-Talisman`.
- **Impacto Potencial:** Vulnerabilidade a ataques de Cross-Site Scripting (XSS), Clickjacking e Man-in-the-Middle.
- **Nível de Severidade:** Média.
- **Recomendação de Correção:** Instalar e configurar `Flask-Talisman` para adicionar automaticamente os cabeçalhos de segurança recomendados.
- **Referências:** OWASP A05:2021 – Security Misconfiguration; CWE-693.

### 3.4 Configuração Insegura de Limite de Upload
- **Localização:** `config.py`, Linha 12.
- **Descrição:** O `MAX_CONTENT_LENGTH` está configurado para 100MB, enquanto a regra de negócio (RN008) especifica um limite de 5MB.
- **Evidência:** 
  ```python
  MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
  ```
- **Impacto Potencial:** Ataques de Negação de Serviço (DoS) por exaustão de armazenamento ou memória ao processar arquivos excessivamente grandes.
- **Nível de Severidade:** Média.
- **Recomendação de Correção:** Reduzir o valor para `5 * 1024 * 1024` (5MB).
- **Referências:** OWASP A02:2021 – Security Misconfiguration; CWE-400.

### 3.5 Cookies de Sessão sem Atributos de Segurança
- **Localização:** `app/__init__.py`.
- **Descrição:** Os cookies de sessão do Flask não estão configurados com os atributos `Secure`, `HttpOnly` e `SameSite`.
- **Evidência:** Ausência de configurações como `SESSION_COOKIE_SECURE` no `config.py`.
- **Impacto Potencial:** Roubo de sessão via scripts maliciosos (XSS) ou interceptação de tráfego (Sniffing).
- **Nível de Severidade:** Média.
- **Recomendação de Correção:** Adicionar `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True` e `SESSION_COOKIE_SAMESITE='Lax'` à configuração.
- **Referências:** OWASP A07:2021 – Identification and Authentication Failures; CWE-614.

### 3.6 Logs com Informações Sensíveis (Verbose Logging)
- **Localização:** `app/__init__.py`, Linha 55.
- **Descrição:** O handler de erro 500 registra o traceback completo no log do sistema.
- **Evidência:** 
  ```python
  app.logger.error(traceback.format_exc())
  ```
- **Impacto Potencial:** Vazamento de estrutura de diretórios, nomes de variáveis e possivelmente fragmentos de dados sensíveis em caso de erro, facilitando o reconhecimento por parte de um atacante que ganhe acesso aos logs.
- **Nível de Severidade:** Baixa.
- **Recomendação de Correção:** Registrar apenas a mensagem de erro e um ID de correlação, mantendo o traceback em um sistema de log interno/seguro não acessível a todos os operadores.
- **Referências:** OWASP A09:2021 – Security Logging and Alerting Failures; CWE-209.
