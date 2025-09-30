# Navegador de Regulamentação do Setor Elétrico

Uma ferramenta interativa para exploração de temas em regulamentações do setor elétrico brasileiro através de nuvens de temas navegáveis.

## Características

- 🔍 **Análise Temática**: Extrai e agrupa temas automaticamente de documentos regulamentares
- 🎯 **Navegação Hierárquica**: Permite aprofundamento progressivo nos temas
- ☁️ **Visualização Interativa**: Interface de nuvem de temas com D3.js
- 📤 **Upload de Documentos**: Suporte para análise de documentos personalizados
- 🇧🇷 **Otimizado para Português**: Processamento específico para regulamentação brasileira

## Instalação e Uso

### Opção 1: Servidor Simples (Recomendado)

Usando apenas bibliotecas nativas do Python:

```bash
# Clone o repositório
git clone https://github.com/ricardogrodzicki/Carga_Legislacao_Assistente_GPT.git
cd Carga_Legislacao_Assistente_GPT

# Execute o servidor simples
python3 simple_server.py
```

Acesse http://localhost:8000 no seu navegador.

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

1. **Visualização Inicial**: A página inicial mostra os temas principais encontrados nos dados de exemplo
2. **Navegação**: Clique nas bolhas para explorar subtemas
3. **Breadcrumb**: Use a navegação superior para voltar aos níveis anteriores
4. **Upload**: Use o botão "Carregar Documentos" para analisar seus próprios textos
5. **Detalhes**: Visualize palavras-chave e documentos relacionados a cada tema

## Estrutura do Projeto

```
├── simple_server.py          # Servidor HTTP simples (apenas bibliotecas nativas)
├── app.py                    # Servidor Flask avançado
├── templates/
│   └── index.html            # Interface web principal
├── requirements.txt          # Dependências Python
└── README.md                # Este arquivo
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