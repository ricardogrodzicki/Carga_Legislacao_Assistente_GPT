# Ferramentas para o Setor Elétrico Brasileiro

Conjunto de ferramentas interativas para análise e consultoria no setor elétrico brasileiro.

## Ferramentas Disponíveis

### 1. Navegador de Regulamentação do Setor Elétrico
Uma ferramenta interativa para exploração de temas em regulamentações do setor elétrico brasileiro através de nuvens de temas navegáveis.

### 2. Análise de Localização para Plantas Industriais (NOVO!)
Ferramenta profissional para consultores de energia analisarem e recomendarem a melhor localização no Brasil para instalação de plantas industriais eletrointensivas. Inclui análise comparativa de custos (OPEX/CAPEX), prazos, incentivos fiscais e scores ponderáveis.

## Características

- 🔍 **Análise Temática**: Extrai e agrupa temas automaticamente de documentos regulamentares
- 🎯 **Navegação Hierárquica**: Permite aprofundamento progressivo nos temas
- ☁️ **Visualização Interativa**: Interface de nuvem de temas com D3.js
- 📤 **Upload de Documentos**: Suporte para análise de documentos personalizados
- 🤖 **Integração OpenAI**: Busca dinâmica de documentos via Vector Store da OpenAI
- 🔄 **Dados Sempre Atualizados**: Temas baseados na base do assistente OpenAI
- 🇧🇷 **Otimizado para Português**: Processamento específico para regulamentação brasileira

## Instalação e Uso

### Opção 1: Servidor Simples (Recomendado)

Usando apenas bibliotecas nativas do Python ou com integração OpenAI:

```bash
# Clone o repositório
git clone https://github.com/ricardogrodzicki/Carga_Legislacao_Assistente_GPT.git
cd Carga_Legislacao_Assistente_GPT

# Para usar com OpenAI Vector Store (opcional):
# 1. Copie o arquivo de exemplo
cp .env.example .env

# 2. Edite .env e adicione suas credenciais OpenAI
# 3. Instale as dependências
pip install openai python-dotenv

# Execute o servidor simples (funciona com ou sem OpenAI)
python3 simple_server.py
```

Acesse http://localhost:8000 no seu navegador.

**Nota**: O servidor funciona sem configuração adicional usando dados de exemplo. Configure o `.env` para usar dados dinâmicos do Vector Store da OpenAI.

### Opção 2: Servidor Flask (Avançado)

Se você tiver as dependências instaladas:

```bash
# Instale as dependências
pip install -r requirements.txt

# Execute o servidor Flask
python3 app.py
```

Acesse http://localhost:5000 no seu navegador.

## Como Usar

### Navegador de Regulamentação
1. **Visualização Inicial**: A página inicial mostra os temas principais encontrados nos dados de exemplo
2. **Navegação**: Clique nas bolhas para explorar subtemas
3. **Breadcrumb**: Use a navegação superior para voltar aos níveis anteriores
4. **Upload**: Use o botão "Carregar Documentos" para analisar seus próprios textos
5. **Detalhes**: Visualize palavras-chave e documentos relacionados a cada tema

### Análise de Localização Industrial
1. **Acesso**: Na página inicial, clique em "Análise de Localização Industrial" ou acesse `http://localhost:8000/industrial-location`
2. **Entrada de Dados**: Preencha os campos com informações da planta industrial (carga, tipo, orçamento, etc.)
3. **Ajuste de Pesos**: Personalize a importância de cada critério (custo, prazo, incentivos, etc.)
4. **Análise**: Clique em "Realizar Análise" para obter recomendações
5. **Resultados**: Visualize Top 3 regiões, tabelas comparativas e gráficos interativos
6. **Exportação**: Salve cenários ou exporte dados em CSV para Excel

Para mais detalhes, consulte o [Guia Completo de Uso da Ferramenta de Localização](INDUSTRIAL_LOCATION_GUIDE.md).

## Estrutura do Projeto

```
├── simple_server.py                  # Servidor HTTP simples (apenas bibliotecas nativas)
├── app.py                            # Servidor Flask avançado
├── templates/
│   ├── index.html                    # Interface web principal - Navegador de Regulamentação
│   ├── index_local.html              # Versão local do navegador
│   └── industrial_location.html      # Ferramenta de Análise de Localização Industrial
├── requirements.txt                  # Dependências Python
├── README.md                         # Este arquivo
├── INDUSTRIAL_LOCATION_GUIDE.md      # Guia completo da ferramenta de localização
├── USAGE.md                          # Guia de uso detalhado
└── VECTOR_STORE.md                   # Documentação sobre Vector Store
```

## Funcionalidades

### Análise Temática
- Extração automática de temas baseada em palavras-chave do setor elétrico
- Categorização por: tarifas, distribuição, transmissão, geração, consumidor, etc.
- Suporte para documentos personalizados

### Interface Interativa
- Visualização em nuvem de bolhas redimensionáveis
- Cores distintas para cada tema
- Navegação hierárquica com breadcrumbs
- Estatísticas em tempo real

### Processamento de Texto
- Remoção de stopwords em português
- Limpeza e normalização de texto
- Identificação de termos específicos do setor elétrico

## Exemplo de Dados

A aplicação inclui dados de exemplo com regulamentações sobre:
- Tarifas e reajustes de energia elétrica
- Qualidade do fornecimento
- Geração distribuída solar
- Segurança em instalações elétricas
- Concessões de transmissão
- Fiscalização e penalidades
- Direitos do consumidor
- Energia renovável
- Medição inteligente
- Aspectos ambientais

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.