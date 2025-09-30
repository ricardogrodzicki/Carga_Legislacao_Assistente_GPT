# Manual de Uso - Navegador de Regulamentação Elétrica

## Visão Geral

O Navegador de Regulamentação Elétrica é uma ferramenta interativa que permite explorar temas de regulamentação do setor elétrico brasileiro através de uma interface visual intuitiva com nuvens de temas navegáveis.

## Iniciando a Aplicação

### Opção 1: Servidor Simples (Recomendado)

#### Com OpenAI Vector Store (Dados Atualizados)

Se você tem acesso ao Vector Store da OpenAI com regulamentações do setor elétrico:

```bash
# 1. Copie o arquivo de exemplo de variáveis de ambiente
cp .env.example .env

# 2. Edite .env e adicione suas credenciais
# OPENAI_API_KEY=sua_chave_aqui
# VECTOR_STORE_ID=seu_vector_store_id_aqui

# 3. Instale as dependências (se ainda não instalou)
pip install openai python-dotenv

# 4. Inicie o servidor
python3 simple_server.py
```

O servidor buscará automaticamente os documentos mais relevantes sobre "energia elétrica" do Vector Store da OpenAI.

#### Sem Vector Store (Dados de Exemplo)

Para usar apenas dados de exemplo locais:

```bash
python3 simple_server.py
```

O servidor funcionará normalmente com os dados de exemplo integrados, sem necessidade de configuração adicional.

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

### Integração com OpenAI Vector Store

A aplicação agora suporta integração com o Vector Store da OpenAI para buscar documentos dinâmicos e sempre atualizados:

- **Busca Automática**: Na inicialização, busca documentos sobre "energia elétrica"
- **Dados Atualizados**: Apresenta temas baseados na base de dados do assistente OpenAI
- **Fallback Inteligente**: Se o Vector Store não estiver configurado, usa dados de exemplo
- **Status Transparente**: A API indica se está usando dados do Vector Store ou dados de exemplo

#### Configuração do Vector Store

1. Obtenha sua chave de API da OpenAI em https://platform.openai.com
2. Crie ou identifique seu Vector Store ID
3. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   OPENAI_API_KEY=sua_chave_aqui
   VECTOR_STORE_ID=seu_vector_store_id_aqui
   ```

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