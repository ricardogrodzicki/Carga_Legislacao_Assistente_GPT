# Integração com OpenAI Vector Store

## Visão Geral

O `simple_server.py` agora suporta integração com o OpenAI Vector Store, permitindo que a aplicação busque documentos dinâmicos e sempre atualizados sobre regulamentações do setor elétrico brasileiro.

## Configuração

### 1. Obter Credenciais da OpenAI

1. Acesse https://platform.openai.com
2. Crie uma conta ou faça login
3. Vá para "API Keys" e crie uma nova chave
4. Anote sua chave de API (começa com `sk-...`)

### 2. Criar ou Identificar seu Vector Store

O Vector Store deve conter documentos sobre regulamentações do setor elétrico brasileiro. Para criar um:

1. Acesse a interface da OpenAI ou use a API
2. Crie um novo Vector Store
3. Faça upload dos seus documentos de regulamentação
4. Anote o ID do Vector Store (começa com `vs_...`)

### 3. Configurar Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env
nano .env
```

Adicione suas credenciais:

```
OPENAI_API_KEY=sk-sua_chave_aqui
VECTOR_STORE_ID=vs_seu_vector_store_id_aqui
```

### 4. Instalar Dependências

```bash
pip install openai python-dotenv
```

## Funcionamento

### Fluxo de Inicialização

1. O servidor tenta carregar as variáveis de ambiente do arquivo `.env`
2. Se `OPENAI_API_KEY` e `VECTOR_STORE_ID` estiverem configurados:
   - Busca documentos do Vector Store usando a query "energia elétrica"
   - Carrega até 20 documentos do Vector Store
   - Extrai as primeiras 3 linhas significativas de cada documento
3. Se não estiverem configurados ou houver erro:
   - Usa dados de exemplo locais (10 regulamentações de amostra)
   - Funciona normalmente sem necessidade de configuração

### Função de Busca

```python
fetch_documents_from_vector_store(query="energia elétrica", max_results=20)
```

**Parâmetros:**
- `query`: Termo de busca (padrão: "energia elétrica")
- `max_results`: Número máximo de documentos a buscar (padrão: 20)

**Retorno:**
- Lista de textos de documentos se sucesso
- `None` se não configurado ou erro

### API Response

A resposta da API `/api/themes` agora inclui um campo `source`:

```json
{
  "success": true,
  "themes": [...],
  "total_documents": 20,
  "source": "vector_store"  // ou "sample_data"
}
```

## Estrutura dos Documentos no Vector Store

Para melhores resultados, os documentos no Vector Store devem:

1. **Estar em português brasileiro**
2. **Conter texto sobre regulamentações elétricas**
3. **Ter conteúdo suficiente** (pelo menos algumas linhas)
4. **Incluir termos técnicos do setor**, como:
   - Tarifas, distribuição, transmissão
   - Geração, consumidor, qualidade
   - ANEEL, energia elétrica, etc.

### Exemplo de Documento Ideal

```
Resolução ANEEL nº 1000/2024

Estabelece os procedimentos para o reajuste tarifário anual das 
distribuidoras de energia elétrica.

Art. 1º - As distribuidoras deverão aplicar os índices de reajuste 
conforme metodologia estabelecida pela ANEEL.

Art. 2º - O reajuste considerará os custos operacionais, investimentos 
em infraestrutura e qualidade do serviço prestado aos consumidores.
```

## Solução de Problemas

### Servidor usa sample_data mesmo com .env configurado

**Possíveis causas:**
1. Variáveis de ambiente não carregadas
   - Verifique se o arquivo `.env` está no diretório correto
   - Confirme que `python-dotenv` está instalado
   
2. Credenciais inválidas
   - Verifique se a API key é válida
   - Confirme se o Vector Store ID está correto
   
3. Erros de conexão
   - Verifique sua conexão com internet
   - Veja os logs do servidor para mensagens de erro

### Erro "OPENAI_API_KEY or VECTOR_STORE_ID not set"

**Solução:**
1. Verifique se o arquivo `.env` existe
2. Confirme que as variáveis estão no formato correto:
   ```
   OPENAI_API_KEY=sk-...
   VECTOR_STORE_ID=vs_...
   ```
3. Não use aspas ao redor dos valores

### Erro ao buscar documentos do Vector Store

**Possíveis causas:**
1. Vector Store vazio
   - Faça upload de documentos para o Vector Store
   
2. Permissões da API key
   - Confirme que a API key tem permissão para acessar Vector Stores
   
3. Vector Store ID incorreto
   - Verifique o ID na interface da OpenAI

## Monitoramento

O servidor exibe mensagens informativas durante a inicialização:

```bash
# Com Vector Store configurado e funcionando:
Successfully fetched 20 documents from Vector Store
Using 20 documents from OpenAI Vector Store

# Sem Vector Store ou com erro:
Warning: OPENAI_API_KEY or VECTOR_STORE_ID not set in .env file
Using 10 sample documents (Vector Store not available)
```

## Vantagens da Integração

1. **Dados Sempre Atualizados**: Temas refletem a base atual do Vector Store
2. **Escalabilidade**: Suporta grande volume de documentos
3. **Flexibilidade**: Fácil atualização da base de dados
4. **Fallback Seguro**: Funciona mesmo sem configuração
5. **Transparência**: API indica a fonte dos dados

## Limitações

1. **Custos**: Uso da API OpenAI pode gerar custos
2. **Latência**: Primeira requisição pode ser mais lenta
3. **Dependência Externa**: Requer conexão com OpenAI
4. **Quota**: Sujeito a limites de rate da API OpenAI

## Próximos Passos

Para melhorar a integração:

1. Implementar cache de documentos
2. Adicionar busca por query personalizada
3. Suportar múltiplos Vector Stores
4. Implementar paginação de resultados
5. Adicionar filtros por data/tipo de documento
