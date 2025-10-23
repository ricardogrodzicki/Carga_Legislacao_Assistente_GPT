# ANEEL Tracker - Guia de Início Rápido

## Início Rápido em 3 Passos

### 1. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 2. Execute o Servidor

```bash
python aneel_server.py
```

### 3. Abra o Navegador

```
http://localhost:5001
```

Pronto! A interface web já estará disponível.

---

## O que é o ANEEL Tracker?

Uma ferramenta completa para acompanhar pautas e atas da ANEEL de forma:

- **Automatizada**: Coleta dados automaticamente do site oficial
- **Organizada**: Agrupa por tipo (pauta/ata) e tema
- **Inteligente**: Classifica processos usando IA
- **Interativa**: Interface web moderna e amigável
- **Completa**: API REST para integração

---

## Principais Recursos

### Dashboard
Visualize estatísticas gerais: documentos, pautas, atas e processos

### Documentos
Navegue por pautas e atas publicadas

### Por Tema
Veja processos agrupados por 10 macrotemas:
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

### Busca
Pesquise processos por número, assunto ou deliberação

### Filtros
Filtre por tipo de documento e tema

### Exportação
Exporte dados em JSON para análise externa

---

## Configuração Opcional

### Habilitar Classificação com IA (OpenAI)

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite `.env` e adicione sua chave:
```env
OPENAI_API_KEY=sk-sua-chave-aqui
```

3. Reinicie o servidor

Com OpenAI ativado, a classificação fica muito mais precisa!

---

## Uso Básico da Interface

1. **Atualizar Dados**: Clique em "Atualizar" para buscar novos documentos
2. **Navegar**: Use as abas para alternar entre visualizações
3. **Pesquisar**: Digite na caixa de busca para encontrar processos
4. **Filtrar**: Use os dropdowns para filtrar por tipo e tema
5. **Exportar**: Clique em "Exportar" para baixar dados

---

## API REST

A ferramenta também fornece uma API completa:

### Listar Documentos
```bash
curl http://localhost:5001/api/documentos?tipo=pauta&limite=10
```

### Ver Processos por Tema
```bash
curl http://localhost:5001/api/temas
```

### Pesquisar
```bash
curl "http://localhost:5001/api/pesquisar?q=tarifa&limite=20"
```

### Atualizar Dados
```bash
curl -X POST http://localhost:5001/api/atualizar \
  -H "Content-Type: application/json" \
  -d '{"paginas": 5}'
```

---

## Estrutura dos Dados

### Documento (Pauta/Ata)
```json
{
  "tipo": "pauta",
  "numero_reuniao": "042",
  "data": "2024-10-15",
  "tipo_reuniao": "Reunião Ordinária",
  "processos": [...]
}
```

### Processo
```json
{
  "numero": "48500.123456/2024-01",
  "assunto": "Reajuste tarifário...",
  "macrotema": "Tarifas e Preços",
  "subtemas": ["Reajuste Tarifário"],
  "descricao_sucinta": "Aprovação do reajuste..."
}
```

---

## Linha de Comando

Use diretamente o módulo:

```bash
python aneel_tracker.py --paginas 10 --output dados.json
```

Isso coleta dados e salva em JSON sem interface web.

---

## Solução de Problemas

### Porta em uso
```bash
PORT=5002 python aneel_server.py
```

### Módulo não encontrado
```bash
pip install -r requirements.txt
```

### Scraping não funciona
- Verifique sua conexão com internet
- O site da ANEEL pode estar indisponível temporariamente

---

## Próximos Passos

1. Explore a **documentação completa**: `ANEEL_TRACKER_README.md`
2. Teste a **API REST** com diferentes filtros
3. Configure **OpenAI** para classificação mais precisa
4. **Integre** com seus sistemas usando a API

---

## Arquivos Principais

- `aneel_tracker.py` - Módulo principal (scraping, processamento, classificação)
- `aneel_server.py` - Servidor web Flask com API
- `templates/aneel_index.html` - Interface web
- `ANEEL_TRACKER_README.md` - Documentação completa
- `test_aneel_tracker.py` - Testes

---

## Tecnologias

- **Python 3.8+**
- **Flask** (servidor web)
- **BeautifulSoup** (scraping)
- **OpenAI API** (classificação IA - opcional)
- **JavaScript** (interface interativa)

---

## Suporte

Consulte a documentação completa em `ANEEL_TRACKER_README.md`

---

Desenvolvido para facilitar o acompanhamento das deliberações da ANEEL!
