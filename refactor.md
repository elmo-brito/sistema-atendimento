# Relatório de Refatoração e Otimização - SAC Premium

Este documento detalha as mudanças realizadas para alinhar o sistema estritamente às especificações do arquivo `docs/03-especs.md` e otimizar a arquitetura para desempenho e manutenibilidade.

## 1. Simplificação e Alinhamento do Modelo de Dados
Foi realizada uma "limpeza" profunda no banco de dados para remover abstrações desnecessárias que não constavam na especificação original.

- **Remoção de RBAC Complexo**: As tabelas `Papel` (Roles) e `Permissao` foram removidas. O controle de acesso agora é baseado no campo `perfil` (`cliente`, `atendente`, `admin`) no modelo `Usuario`, reduzindo o número de joins em consultas de autenticação.
- **Pruning de Modelos**: Tabelas como `Subcategoria`, `ConfiguracaoGlobal` e `RegraAutomacao` foram eliminadas por não estarem previstas no escopo simplificado.
- **Novas Entidades**: Implementação dos modelos `Avaliacao` (RF009) e `Artigo` (RF010) para suporte à Base de Conhecimento e Feedback do Cliente.

## 2. Otimização de Consultas e Camada de Repositório
As consultas ao banco de dados foram otimizadas para garantir escalabilidade.

- **Atribuição Inteligente (MTTA)**: A lógica `get_least_busy_atendente` no `UsuarioRepository` foi otimizada usando uma **subquery** que conta chamados ativos diretamente no banco, evitando o carregamento de todos os usuários na memória do Python para processamento.
- **Busca Global**: Centralização da lógica de filtro e busca no `SolicitacaoRepository`, permitindo filtragem combinada (status, prioridade, categoria) em uma única query.
- **Timeline Performance**: Uso de `cascade="all, delete-orphan"` e carregamento `lazy='dynamic'` para gerenciar grandes volumes de mensagens e anexos sem comprometer o tempo de resposta da página de detalhes.

## 3. Modularização da Lógica de Negócio (Services)
A lógica foi movida das Views para Services especializados, facilitando o TDD e a reutilização.

- **`AuthService`**: Centraliza registro, login (com verificação de status `ativo`) e fluxo de recuperação de senha.
- **`SolicitacaoService`**: Gere o ciclo de vida completo do chamado, incluindo a regra de **reabertura em 7 dias** (RN004) e **encerramento automático** (RN005).
- **`ReportService`**: Implementação de métricas calculadas como **MTTR** (Mean Time To Resolve) e **MTTA** (Mean Time To Assign), com exportação eficiente para CSV.

## 4. Melhorias na Interface e UX
- **Mobile-First**: Refatoração completa dos templates Jinja2 usando Tailwind CSS para garantir ausência de scroll horizontal em telas de 375px (RF021).
- **Feedback Visual**: Implementação de badges de status e prioridade consistentes em todo o sistema.
- **Redução de Dependências de Frontend**: Migração de lógicas complexas para Alpine.js, mantendo o frontend leve e reativo.

## 5. Estabilização e Testes
- **Suite de Testes Atualizada**: Todos os 15 testes automatizados foram refatorados para validar o novo sistema de perfis e regras de SLA.
- **Cobertura**: Foco em 100% de cobertura nos métodos críticos de `SolicitacaoService` (Cálculo de SLA e Atribuição).

---
*Relatório gerado em 18 de Maio de 2026.*
