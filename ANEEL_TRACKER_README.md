# ANEEL Tracker - Acompanhamento de Pautas e Atas

## Visão Geral

O ANEEL Tracker é uma ferramenta avançada para acompanhamento automatizado das pautas e atas publicadas pela ANEEL (Agência Nacional de Energia Elétrica). A ferramenta coleta, processa, classifica e apresenta as informações de forma organizada, interativa e amigável.

## Funcionalidades Principais

### 1. Coleta Automatizada
- Scraping do site oficial da ANEEL
- Extração de pautas e atas de reuniões e circuitos deliberativos
- Atualização periódica dos dados

### 2. Processamento Inteligente
- Extração automática de números de processos
- Identificação de assuntos e deliberações
- Análise de contexto usando técnicas de NLP

### 3. Classificação por IA
- **Macrotemas**: Classificação em 10 categorias principais
  - Tarifas e Preços
  - Distribuição de Energia
  - Transmissão de Energia
  - Geração de Energia
  - Direitos do Consumidor
  - Fiscalização e Regulação
  - Aspectos Econômico-Financeiros
  - Aspectos Ambientais
  - Comercialização de Energia
  - Outros Assuntos

- **Subtemas**: Categorização detalhada dentro de cada macrotema
- **Descrição Sucinta**: Resumo objetivo de cada processo (máx. 100 caracteres)
- **Integração OpenAI**: Usa GPT-4 para classificação inteligente (opcional)

### 4. Interface Interativa
- Dashboard com estatísticas em tempo real
- Visualização por documentos (pautas/atas)
- Visualização por temas (macrotemas)
- Lista completa de processos
- Busca avançada
- Filtros por tipo, tema e período
- Design responsivo para mobile e desktop

### 5. Exportação de Dados
- Exportação para JSON
- API REST completa para integração

## Instalação

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório** (se ainda não fez)
```bash
git clone https://github.com/ricardogrodzicki/Carga_Legislacao_Assistente_GPT.git
cd Carga_Legislacao_Assistente_GPT
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure variáveis de ambiente** (opcional, para classificação com IA)

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da OpenAI:
```
OPENAI_API_KEY=sk-...
```

**Nota**: A ferramenta funciona sem a API da OpenAI, usando classificação baseada em palavras-chave.

4. **Execute o servidor**
```bash
python aneel_server.py
```

5. **Acesse a interface**

Abra seu navegador em: `http://localhost:5001`

## Uso

### Interface Web

#### Dashboard Principal
- Visualize estatísticas gerais (documentos, pautas, atas, processos)
- Navegue entre diferentes visualizações usando as abas

#### Aba "Documentos"
- Veja todos os documentos coletados
- Cartões coloridos para pautas (azul) e atas (verde)
- Clique em um cartão para ver detalhes

#### Aba "Por Tema"
- Visualização de processos agrupados por macrotema
- Cartões coloridos indicando quantidade de processos
- Clique em um tema para filtrar processos

#### Aba "Todos os Processos"
- Lista completa de processos
- Informações detalhadas: número, assunto, tema, subtemas
- Descrição sucinta e deliberação (quando disponível)

#### Pesquisa
- Use a caixa de pesquisa para encontrar processos
- Pesquisa em tempo real
- Busca em número, assunto e deliberação

#### Filtros
- **Tipo**: Filtrar por pauta ou ata
- **Tema**: Filtrar por macrotema específico
- Combinação de filtros

#### Atualização
- Clique no botão "Atualizar" para buscar novos dados
- Processo pode levar alguns minutos
- Dados são salvos em cache

#### Exportação
- Clique em "Exportar" para baixar dados em JSON
- Arquivo contém todos os documentos e processos

### API REST

A ferramenta fornece uma API completa para integração:

#### GET /api/status
Retorna status do sistema e estatísticas gerais.

```json
{
  "success": true,
  "status": "online",
  "dados_carregados": true,
  "estatisticas": {
    "total_documentos": 50,
    "total_pautas": 25,
    "total_atas": 25,
    "total_processos": 150
  }
}
```

#### GET /api/documentos
Lista documentos com filtros opcionais.

Query parameters:
- `tipo`: 'pauta' ou 'ata'
- `data_inicio`: YYYY-MM-DD
- `data_fim`: YYYY-MM-DD
- `limite`: número de documentos (padrão: 50)

```bash
curl "http://localhost:5001/api/documentos?tipo=pauta&limite=10"
```

#### GET /api/documento/{tipo}/{numero}
Detalhes de um documento específico.

```bash
curl "http://localhost:5001/api/documento/pauta/123"
```

#### GET /api/temas
Processos agrupados por tema.

Query parameters:
- `macrotema`: filtrar por macrotema específico

```bash
curl "http://localhost:5001/api/temas?macrotema=Tarifas%20e%20Preços"
```

#### GET /api/processos
Lista de processos com filtros.

Query parameters:
- `macrotema`: filtrar por macrotema
- `subtema`: filtrar por subtema
- `tipo_documento`: 'pauta' ou 'ata'
- `limite`: número de processos (padrão: 100)

```bash
curl "http://localhost:5001/api/processos?macrotema=Distribuição%20de%20Energia&limite=20"
```

#### GET /api/pesquisar
Pesquisa em processos.

Query parameters:
- `q`: termo de pesquisa (obrigatório)
- `campo`: 'numero', 'assunto', 'deliberacao', 'descricao_sucinta'
- `limite`: número de resultados (padrão: 50)

```bash
curl "http://localhost:5001/api/pesquisar?q=tarifa&limite=10"
```

#### POST /api/atualizar
Atualiza dados do tracker.

```bash
curl -X POST http://localhost:5001/api/atualizar \
  -H "Content-Type: application/json" \
  -d '{"paginas": 5}'
```

#### GET /api/relatorio
Gera relatório consolidado.

Query parameters:
- `data_inicio`: YYYY-MM-DD
- `data_fim`: YYYY-MM-DD
- `macrotema`: filtrar por macrotema

```bash
curl "http://localhost:5001/api/relatorio?data_inicio=2024-01-01&data_fim=2024-12-31"
```

#### GET /api/exportar/{formato}
Exporta dados (formatos: json, csv).

```bash
curl "http://localhost:5001/api/exportar/json" -O
```

### Uso em Linha de Comando

Você também pode usar o módulo diretamente:

```bash
python aneel_tracker.py --paginas 10 --output dados_aneel.json
```

Parâmetros:
- `--paginas`: número de páginas para coletar (padrão: 5)
- `--output`: arquivo de saída JSON (padrão: aneel_data.json)

## Estrutura do Projeto

```
Carga_Legislacao_Assistente_GPT/
├── aneel_tracker.py          # Módulo principal (scraping, processamento, classificação)
├── aneel_server.py            # Servidor web Flask com API REST
├── templates/
│   └── aneel_index.html      # Interface web interativa
├── requirements.txt           # Dependências Python
├── ANEEL_TRACKER_README.md   # Esta documentação
└── .env.example              # Exemplo de variáveis de ambiente
```

## Arquitetura

### Componentes Principais

#### 1. ANEELScraper
Responsável por coletar dados do site da ANEEL.
- Faz requisições HTTP para o site oficial
- Extrai informações de notícias sobre pautas e atas
- Identifica tipo de documento e metadados

#### 2. ProcessadorDocumentos
Processa documentos e extrai processos.
- Usa regex para identificar números de processos
- Extrai contexto ao redor dos processos
- Identifica assunto e deliberação

#### 3. ClassificadorProcessos
Classifica processos por tema usando IA ou keywords.
- **Modo OpenAI**: Usa GPT-4 para classificação inteligente
- **Modo Keywords**: Classificação baseada em palavras-chave
- Gera descrição sucinta
- Atribui macrotema e subtemas

#### 4. ANEELTracker
Classe principal que coordena tudo.
- Gerencia coleta, processamento e classificação
- Fornece métodos de consulta e filtro
- Exporta dados em JSON

#### 5. Servidor Web (Flask)
API REST e interface web.
- Endpoints RESTful para acesso programático
- Interface HTML/CSS/JS interativa
- Atualização em tempo real

## Macrotemas e Classificação

### Lista Completa de Macrotemas

1. **Tarifas e Preços**
   - Reajuste Tarifário, Revisão Tarifária, Bandeiras Tarifárias, Estrutura Tarifária, Subsídios

2. **Distribuição de Energia**
   - Qualidade do Serviço, Expansão da Rede, Concessão, Perdas Técnicas, Medição

3. **Transmissão de Energia**
   - Concessão, RAP, Reforços, Instalações, Operação

4. **Geração de Energia**
   - Geração Distribuída, Energia Renovável, Térmica, Hidrelétrica, Autorização

5. **Direitos do Consumidor**
   - Atendimento, Faturamento, Religação, Compensação, Ressarcimento

6. **Fiscalização e Regulação**
   - Penalidades, Processos Sancionadores, Compliance, Indicadores, Auditoria

7. **Aspectos Econômico-Financeiros**
   - Base de Remuneração, WACC, Investimentos, Custos Operacionais, Receitas

8. **Aspectos Ambientais**
   - Licenciamento, Compensação Ambiental, Impactos, Recuperação, Estudos

9. **Comercialização de Energia**
   - Mercado Livre, Mercado Regulado, Contratos, Leilões, CCEE

10. **Outros Assuntos**
    - Administrativo, Recursos Humanos, Tecnologia, Pesquisa, Diversos

## Exemplo de Dados

### Estrutura de um Documento

```json
{
  "tipo": "pauta",
  "data": "2024-10-15T00:00:00",
  "numero_reuniao": "042",
  "tipo_reuniao": "Reunião Ordinária",
  "url": "https://www2.aneel.gov.br/...",
  "data_publicacao": "2024-10-11T00:00:00",
  "processos": [
    {
      "numero": "48500.123456/2024-01",
      "assunto": "Reajuste tarifário da distribuidora XYZ...",
      "deliberacao": null,
      "macrotema": "Tarifas e Preços",
      "subtemas": ["Reajuste Tarifário"],
      "descricao_sucinta": "Aprovação do reajuste tarifário anual da distribuidora XYZ"
    }
  ]
}
```

### Estrutura de um Processo

```json
{
  "numero": "48500.123456/2024-01",
  "assunto": "Processo de reajuste tarifário da distribuidora XYZ para o período 2024-2025",
  "deliberacao": "Aprovado por unanimidade",
  "macrotema": "Tarifas e Preços",
  "subtemas": ["Reajuste Tarifário", "Estrutura Tarifária"],
  "descricao_sucinta": "Aprovação do reajuste tarifário anual da distribuidora XYZ"
}
```

## Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# OpenAI API (opcional)
OPENAI_API_KEY=sk-...

# Configurações do servidor
PORT=5001
DEBUG=True

# Configurações de coleta
PAGINAS_PADRAO=5
```

### Personalização

#### Adicionar Novos Macrotemas

Edite `aneel_tracker.py`, na classe `ClassificadorProcessos`:

```python
self.MACROTEMAS = {
    'seu_tema': {
        'nome': 'Nome do Seu Tema',
        'keywords': ['palavra1', 'palavra2'],
        'subtemas': ['Subtema 1', 'Subtema 2']
    },
    # ... outros temas
}
```

#### Ajustar Processamento

Modifique os métodos da classe `ProcessadorDocumentos`:
- `extrair_processos_do_texto()`: lógica de extração
- `_identificar_assunto()`: identificação de assunto
- `_identificar_deliberacao()`: identificação de deliberação

## Troubleshooting

### Erro: "Módulo não encontrado"
```bash
pip install -r requirements.txt
```

### Erro: "Porta já em uso"
Mude a porta no arquivo `.env` ou ao executar:
```bash
PORT=5002 python aneel_server.py
```

### Scraping não funciona
- Verifique sua conexão com a internet
- O site da ANEEL pode estar temporariamente indisponível
- Verifique se não há firewall bloqueando

### Classificação com OpenAI não funciona
- Verifique se `OPENAI_API_KEY` está configurada no `.env`
- Confirme que a chave é válida
- A ferramenta funciona sem OpenAI (usa keywords)

### Performance lenta
- Reduza o número de páginas: `--paginas 2`
- Use o cache: os dados são salvos em `aneel_data.json`
- Classificação com OpenAI é mais lenta (mas mais precisa)

## Limitações Conhecidas

1. **Dependência do Site**: A ferramenta depende da estrutura atual do site da ANEEL
2. **PDFs**: Atualmente simula extração de PDFs (implementação completa requer PyPDF2)
3. **Rate Limiting**: Muitas requisições podem ser bloqueadas
4. **Classificação**: Sem OpenAI, a classificação é baseada em keywords (menos precisa)

## Melhorias Futuras

- [ ] Extração real de PDFs usando PyPDF2/pdfplumber
- [ ] Agendamento automático de atualizações
- [ ] Notificações de novos documentos
- [ ] Análise de tendências e relatórios avançados
- [ ] Exportação para Excel/CSV
- [ ] Integração com sistemas externos
- [ ] Comparação entre pautas e atas
- [ ] Histórico de deliberações

## Suporte

Para dúvidas ou problemas:
1. Verifique esta documentação
2. Consulte os logs do servidor
3. Abra uma issue no GitHub

## Licença

Este projeto está sob licença MIT.

## Contribuições

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Envie um Pull Request

## Autor

Desenvolvido como parte do projeto Carga_Legislacao_Assistente_GPT.

---

**Última atualização**: Outubro 2024
