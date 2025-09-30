# Manual de Uso - Navegador de Regulamentação Elétrica

## Visão Geral

O Navegador de Regulamentação Elétrica é uma ferramenta interativa que permite explorar temas de regulamentação do setor elétrico brasileiro através de uma interface visual intuitiva com nuvens de temas navegáveis.

## Iniciando a Aplicação

### Opção 1: Servidor Simples (Recomendado)
```bash
python3 simple_server.py
```
Acesse: http://localhost:8000

### Opção 2: Servidor Flask (se dependências instaladas)
```bash
python3 app.py
```
Acesse: http://localhost:5000

## Interface Principal

### 1. Painel de Estatísticas
- **Documentos**: Número total de documentos analisados
- **Temas**: Quantidade de temas identificados
- **Nível**: Nível atual de navegação hierárquica

### 2. Nuvem de Temas
- Cada tema é representado por uma "bolha" colorida
- O tamanho da bolha indica a quantidade de documentos relacionados
- Cores diferentes ajudam a distinguir entre temas
- Clique em uma bolha para explorar subtemas

### 3. Navegação Hierárquica
- **Breadcrumb**: Mostra o caminho de navegação atual
- **Botão Início**: Retorna ao nível principal
- **Links do Breadcrumb**: Permite voltar a níveis específicos

### 4. Detalhes do Tema
- **Palavras-chave**: Termos mais relevantes do tema
- **Documentos**: Exemplos de regulamentações relacionadas
- **Contagem**: Número de documentos por tema

## Funcionalidades

### Exploração de Temas
1. **Visualização Inicial**: A página mostra os temas principais extraídos dos dados
2. **Drill-down**: Clique em qualquer tema para ver subtemas
3. **Navegação**: Use o breadcrumb para voltar aos níveis anteriores
4. **Detalhes**: Veja palavras-chave e documentos de exemplo

### Upload de Documentos Personalizados
1. Clique no botão **"📤 Carregar Documentos"**
2. Cole seus textos de regulamentação na área de texto
3. Separe documentos diferentes por linha
4. Clique em **"⚙️ Processar Documentos"**
5. A aplicação analisará seus documentos e criará novos temas

### Tipos de Temas Identificados

A aplicação reconhece automaticamente os seguintes tipos de regulamentação:

- **Tarifas e Preços**: Regulamentações sobre custos e tarifação
- **Distribuição de Energia**: Normas para distribuidoras
- **Transmissão de Energia**: Regulamentações de transmissão
- **Geração de Energia**: Normas para geradoras
- **Direitos do Consumidor**: Proteção ao consumidor
- **Qualidade do Serviço**: Indicadores e padrões
- **Segurança Elétrica**: Normas de segurança
- **Aspectos Ambientais**: Regulamentações ambientais
- **Energia Renovável**: Incentivos e normas para energia limpa
- **Energia Solar**: Específico para fotovoltaica
- **Energia Eólica**: Regulamentações eólicas
- **Fiscalização**: Penalidades e multas

## Exemplos de Uso

### Cenário 1: Exploração de Dados Padrão
1. Acesse a aplicação
2. Visualize os 8 temas principais dos dados de exemplo
3. Clique em "Geração de Energia" para ver subtemas
4. Explore as palavras-chave e documentos relacionados

### Cenário 2: Análise de Documentos Personalizados
1. Clique em "Carregar Documentos"
2. Cole regulamentações específicas do seu interesse
3. Processe os documentos
4. Explore os novos temas identificados

### Cenário 3: Navegação Hierárquica
1. Inicie na visualização principal
2. Navegue para um tema específico
3. Use o breadcrumb para voltar
4. Explore diferentes caminhos de navegação

## Dicas de Uso

### Para Melhores Resultados
- **Textos Longos**: Use textos com pelo menos 50 caracteres por documento
- **Separação Clara**: Coloque cada documento em uma linha separada
- **Termos Específicos**: Inclua terminologia técnica do setor elétrico
- **Contexto**: Mantenha contexto relevante nos documentos

### Navegação Eficiente
- Use o breadcrumb para navegação rápida
- Observe as estatísticas para entender a distribuição de temas
- Explore palavras-chave para entender melhor cada tema
- Use a função de upload para análises específicas

## Limitações

- A análise é baseada em palavras-chave em português
- Funciona melhor com documentos do setor elétrico brasileiro
- Temas muito pequenos podem ser agrupados como "Regulamentação Geral"
- A interface requer JavaScript habilitado

## Solução de Problemas

### Servidor não inicia
- Verifique se a porta não está em uso
- Use uma porta diferente modificando o código
- Confirme que Python 3 está instalado

### Temas não aparecem
- Verifique se os documentos têm conteúdo suficiente
- Confirme que o texto está em português
- Tente documentos com terminologia do setor elétrico

### Upload não funciona
- Verifique a conexão com o servidor
- Confirme que há texto na área de upload
- Tente documentos mais longos e específicos

## Perguntas Frequentes (FAQ)

### O que acontece depois de clicar em "Processar Documentos"?

Quando você clica em "⚙️ Processar Documentos":

1. **Processamento Imediato**: O sistema começa a analisar seus documentos instantaneamente
2. **Indicador Visual**: Um indicador de carregamento aparece mostrando que o processamento está em andamento
3. **Análise Automática**: A aplicação identifica temas e palavras-chave automaticamente
4. **Atualização da Interface**: Após alguns segundos, os novos temas aparecem na tela principal
5. **Confirmação**: Uma mensagem de sucesso é exibida quando o processamento está completo

**Não é necessário esperar ou fazer nada além de clicar no botão!** O sistema faz tudo automaticamente.

### Quanto tempo demora o processamento?

- **Documentos pequenos** (1-5 documentos): 1-2 segundos
- **Documentos médios** (6-20 documentos): 2-5 segundos
- **Documentos grandes** (mais de 20): 5-10 segundos

Durante esse tempo, você verá um indicador de progresso com a mensagem "⚙️ Processando seus documentos...".

### Posso usar a aplicação enquanto processa?

Sim! O modal de upload fica bloqueado durante o processamento, mas assim que terminar:
- O modal fecha automaticamente
- Os novos temas aparecem na tela principal
- Você pode começar a explorar imediatamente

### Os temas anteriores são perdidos ao carregar novos documentos?

Sim, ao processar novos documentos, a visualização é substituída pelos novos temas. Se você quiser manter os temas anteriores, anote-os ou faça uma captura de tela antes de carregar novos documentos.