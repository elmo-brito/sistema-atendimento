# Plano de Testes - Sistema de Atendimento (SAC)

Este documento descreve a estratégia de testes para o Sistema de Atendimento, seguindo a metodologia **TDD (Test-Driven Development) First**. O objetivo é garantir a qualidade, segurança e manutenibilidade do código desde o início do desenvolvimento.

## 1. Estratégia de Testes

A estratégia foca em automação e cobertura de cenários críticos, dividindo-se em:

- **Testes Unitários:** Validação da lógica de negócio isolada na camada de `Services`.
- **Testes de Integração:** Validação da interação entre `Services`, `Repositories` e o banco de dados.
- **Testes de API:** Validação dos endpoints REST (Views) e conformidade com os requisitos de segurança e status HTTP.

### Ferramentas
- **Pytest:** Framework principal de testes.
- **Pytest-Mock:** Para simulação (mocks) de dependências externas (ex: integração com provedores de e-mail).
- **Freezegun:** Para controle preciso de tempo em testes de SLA e prazos de reabertura.
- **Pytest-Flask:** Facilita o teste de aplicações Flask, provendo o objeto `app` e `client`.
- **Factory-Boy:** Criação de dados de teste (fixtures) de forma consistente e escalável.
- **Coverage:** Monitoramento da cobertura de testes.

## 2. Casos de Teste por Funcionalidade

Para cada RF (Requisito Funcional) e RN (Regra de Negócio), define-se um cenário crítico para TDD.

### 2.1 Autenticação e Perfis (RF001, RF002, RN007)
| ID | Cenário | Tipo | Prioridade | Descrição |
|---|---|---|---|---|
| TC001 | Login com credenciais válidas | API | Crítica | Validar se o sistema retorna 200 OK e cria a sessão para um usuário ativo. |
| TC002 | Acesso negado para rota de Admin | API | Alta | Garantir que um usuário com perfil 'Cliente' receba 403 Forbidden ao acessar `/admin/dashboard`. |
| TC003 | Recuperação de senha com token expirado | Unitário | Média | Utilizar `freezegun` para avançar o tempo e validar se o `AuthService` invalida tokens após o prazo de expiração. |

### 2.2 Gestão de Solicitações e Atribuição (RF003, RF004, RN003)
| ID | Cenário | Tipo | Prioridade | Descrição |
|---|---|---|---|---|
| TC004 | Atribuição Automática por menor carga | Integração | Crítica | Ao abrir um chamado, validar se o `SolicitacaoService` o atribui ao atendente com menos chamados ativos. Em caso de empate, validar critério de desempate (ex: ordem alfabética ou ID). |
| TC005 | Abertura de chamado sem categoria | API | Alta | Validar se a API retorna 400 Bad Request ao omitir campos obrigatórios. |

### 2.3 SLA e Regras de Negócio (RF005, RN001, RN002, RN005)
| ID | Cenário | Tipo | Prioridade | Descrição |
|---|---|---|---|---|
| TC006 | Cálculo de SLA por Categoria | Unitário | Crítica | Validar se o `SolicitacaoService` calcula corretamente `data_criacao + horas_categoria`, considerando apenas horas úteis (se aplicável). |
| TC007 | Encerramento automático por inatividade | Unitário | Alta | Usar `freezegun` para avançar 5 dias e validar se chamados "Aguardando Cliente" fecham automaticamente sem nova interação. |
| TC008 | Cálculo de SLA Global (Fallback) | Unitário | Média | Garantir que se a categoria não tiver prazo, o sistema aplique o padrão de 48h. |

### 2.4 Reabertura e Avaliação (RF008, RF009, RN004, RN006)
| ID | Cenário | Tipo | Prioridade | Descrição |
|---|---|---|---|---|
| TC009 | Reabertura de chamado após 7 dias | Unitário | Alta | Validar se o sistema impede a reabertura de um chamado fechado há mais de 7 dias, forçando a criação de um novo. |
| TC010 | Avaliação dupla de chamado | API | Baixa | Garantir que um segundo POST para avaliação de um mesmo chamado retorne erro 400 ou 409. |

### 2.5 Segurança e Anexos (RNF001, RN008)
| ID | Cenário | Tipo | Prioridade | Descrição |
|---|---|---|---|---|
| TC011 | Upload de arquivo proibido | API | Alta | Tentar upload de arquivo `.exe` ou `.sh` e validar se o sistema rejeita com 400 Bad Request. |
| TC012 | Proteção CSRF em formulários | API | Crítica | Validar se requisições POST sem token CSRF são rejeitadas em ambiente de produção/staging. |

## 3. Ambiente de Testes e Isolamento

### Banco de Dados de Teste
Os testes devem utilizar um banco de dados SQLite em memória (`sqlite:///:memory:`) ou um arquivo separado (`test_app.db`) para garantir que os dados de teste não interfiram no ambiente de desenvolvimento.

### Isolamento de Testes
Cada teste deve ser executado dentro de uma transação do SQLAlchemy que é revertida (`rollback`) ao final, garantindo um estado limpo para o próximo teste.

## 4. Execução e CI/CD

### Execução Local
```bash
# Rodar todos os testes com PYTHONPATH configurado
PYTHONPATH=. pytest -v

# Rodar com relatório de cobertura
coverage run -m pytest
coverage report -m --include="app/services/*,app/repositories/*"
```

### Integração Contínua (CI)
Sugere-se a inclusão de um workflow de GitHub Actions que:
1. Instale as dependências.
2. Execute o Linter (Flake8/Black).
3. Execute a suíte de testes.
4. Falhe o build se a cobertura cair abaixo de **90%** nas camadas de Service e Repository.
