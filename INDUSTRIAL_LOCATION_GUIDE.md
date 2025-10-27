# Guia da Ferramenta de Análise de Localização Industrial

## Visão Geral

Ferramenta interativa desenvolvida para consultores de energia analisarem e recomendarem a melhor localização no Brasil para instalação de plantas industriais eletrointensivas.

## Acesso à Ferramenta

Para acessar a ferramenta:

1. Inicie o servidor:
```bash
python3 simple_server.py
```

2. Acesse no navegador:
   - URL principal: `http://localhost:8000/`
   - Clique no botão "Análise de Localização Industrial"
   - **OU** acesse diretamente: `http://localhost:8000/industrial-location`

## Funcionalidades

### 1. Entrada de Dados do Cliente

A ferramenta permite inserir os seguintes dados da planta industrial:

- **Carga Média (MW)**: Potência média demandada pela planta
- **Carga de Pico (MW)**: Potência máxima demandada
- **Fator de Carga (%)**: Percentual de utilização da carga (0-100%)
- **Sazonalidade**: Indica se há variação sazonal no consumo
- **Tipo de Indústria**:
  - Data Center
  - Combustível de Aviação (Metanol)
  - Hidrogênio Verde
  - Siderúrgica
  - Outro
- **Criticidade**: Tolerância a interrupções (Alta/Média/Baixa)
- **Orçamento CAPEX (R$)**: Valor disponível para investimento inicial
- **Timeline (meses)**: Prazo desejado para início de operação
- **Restrições de Localização**: Campo opcional para especificar preferências geográficas

### 2. Base de Dados Regionais

A ferramenta analisa 5 regiões do Brasil:

#### Região Sul (RS, SC, PR)
- TUSD: 85 R$/MWh
- TUST: 45 R$/MWh
- Energia mercado livre: 220 R$/MWh
- Custo de conexão: 450.000 R$/MW
- Prazo de conexão: 18 meses
- Incentivo ICMS: 12%
- Energia renovável: 65%

#### Região Sudeste (SP, RJ, MG, ES)
- TUSD: 120 R$/MWh
- TUST: 65 R$/MWh
- Energia mercado livre: 260 R$/MWh
- Custo de conexão: 650.000 R$/MW
- Prazo de conexão: 24 meses
- Incentivo ICMS: 5%
- Energia renovável: 45%

#### Região Nordeste (BA, CE, PE, RN)
- TUSD: 95 R$/MWh
- TUST: 50 R$/MWh
- Energia mercado livre: 200 R$/MWh
- Custo de conexão: 380.000 R$/MW
- Prazo de conexão: 20 meses
- Incentivo ICMS: 75%
- Energia renovável: 80%

#### Região Centro-Oeste (GO, MT, MS, DF)
- TUSD: 100 R$/MWh
- TUST: 55 R$/MWh
- Energia mercado livre: 230 R$/MWh
- Custo de conexão: 420.000 R$/MW
- Prazo de conexão: 22 meses
- Incentivo ICMS: 30%
- Energia renovável: 55%

#### Região Norte (PA, AM)
- TUSD: 110 R$/MWh
- TUST: 70 R$/MWh
- Energia mercado livre: 240 R$/MWh
- Custo de conexão: 550.000 R$/MW
- Prazo de conexão: 30 meses
- Incentivo ICMS: 50%
- Energia renovável: 90%

### 3. Ajuste de Pesos dos Critérios

Personalize a importância de cada critério usando sliders:

- **Custo** (padrão: 40%): Impacto dos custos operacionais e de investimento
- **Prazo de Conexão** (padrão: 20%): Importância do tempo de implementação
- **Confiabilidade** (padrão: 15%): Disponibilidade de pontos de conexão
- **Incentivos Fiscais** (padrão: 10%): Benefícios de redução de ICMS
- **Infraestrutura** (padrão: 10%): Qualidade da infraestrutura regional
- **Energia Renovável** (padrão: 5%): Disponibilidade de energia limpa

O total dos pesos deve somar 100% para melhor análise.

### 4. Cálculos Realizados

#### OPEX Anual (Custos Operacionais)
- Custo de energia: Carga × 8760 horas × Fator de Carga × Preço da energia
- TUSD: Demanda contratada × TUSD × 12 meses
- TUST: Demanda contratada × TUST × 12 meses
- Encargos: 15% sobre o custo de energia
- **Total OPEX**: Soma de todos os custos operacionais

#### CAPEX (Custos de Investimento)
- Conexão à rede: Demanda × Custo de conexão por MW
- Infraestrutura elétrica: 50% adicional sobre custo de conexão
- **Total CAPEX**: Soma dos investimentos

#### Indicadores Financeiros
- **Custo primeiro ano**: OPEX + CAPEX
- **Custo médio (R$/MWh)**: (OPEX × 10 anos + CAPEX) / Energia consumida em 10 anos
- **Payback simples**: CAPEX / Economia anual com incentivos

#### Score Total (0-100)
Calculado com base nos pesos definidos:
- Score de Custo: Comparação relativa entre regiões
- Score de Prazo: Baseado no tempo de conexão
- Score de Confiabilidade: Disponibilidade de conexão (Alta=100, Média=60, Baixa=30)
- Score de Incentivos: Percentual de redução de ICMS
- Score de Infraestrutura: Qualidade (Boa=100, Regular=60, Precária=30)
- Score de Renovável: Percentual de energia limpa disponível

### 5. Visualizações e Resultados

#### Top 3 Regiões Recomendadas
- Destaque visual para a melhor opção com badge #1
- Cards coloridos com informações principais
- Vantagens específicas de cada região
- Alertas sobre riscos identificados

#### Tabela Comparativa
- Ranking completo das 5 regiões
- Comparação lado a lado de todos os indicadores
- Destaque em verde para a melhor opção
- Valores formatados em milhões de reais

#### Gráfico de Barras - Custos Totais
- Comparação visual de OPEX e CAPEX por região
- Valores em milhões de reais
- Cores distintas para cada tipo de custo

#### Gráfico Radar - Análise Multidimensional
- Comparação do Top 3 em 6 dimensões
- Visualização simultânea de todos os critérios
- Cores específicas para cada região

#### Gráfico de Dispersão - Custo vs Prazo
- Análise da relação entre custo operacional e prazo de conexão
- Identificação visual de trade-offs
- Cores específicas por região

### 6. Funcionalidades Avançadas

#### Salvar Cenários
- Permite salvar múltiplas análises com nomes personalizados
- Útil para comparar diferentes configurações de planta
- Lista de cenários salvos com timestamp

#### Exportar para CSV
- Gera arquivo com todos os dados da análise
- Formato compatível com Excel
- Inclui todos os indicadores calculados

#### Análise de Sensibilidade
- Mostra como variações de ±20% na carga afetam os resultados
- Útil para avaliar robustez da recomendação
- Apresenta 5 pontos de variação (-20%, -10%, 0%, +10%, +20%)

## Casos de Uso

### Exemplo 1: Data Center de Grande Porte

**Entrada:**
- Carga Média: 100 MW
- Carga de Pico: 120 MW
- Fator de Carga: 95%
- Tipo: Data Center
- Criticidade: Alta

**Resultado Esperado:**
- Regiões com alta confiabilidade terão score maior
- Prazo de conexão será fator importante
- Regiões com baixo risco de congestionamento preferidas

### Exemplo 2: Planta de Hidrogênio Verde

**Entrada:**
- Carga Média: 200 MW
- Carga de Pico: 250 MW
- Fator de Carga: 85%
- Tipo: Hidrogênio Verde
- Criticidade: Média

**Resultado Esperado:**
- Alto peso para energia renovável
- Regiões Nordeste e Norte com vantagem
- Incentivos fiscais terão impacto significativo

### Exemplo 3: Produção de SAF (Combustível de Aviação)

**Entrada:**
- Carga Média: 150 MW
- Carga de Pico: 180 MW
- Fator de Carga: 90%
- Tipo: Combustível de Aviação (Metanol)
- Criticidade: Alta

**Resultado Esperado:**
- Balance entre custo e confiabilidade
- Infraestrutura logística importante
- Proximidade a aeroportos (considerar restrições)

## Recomendações de Uso

### Para Consultores

1. **Preparação da Reunião**
   - Colete dados do cliente antecipadamente
   - Prepare 2-3 cenários (conservador, base, otimista)
   - Ajuste pesos conforme prioridades do cliente

2. **Durante a Apresentação**
   - Mostre primeiro o Top 3 recomendações
   - Use o gráfico radar para explicar trade-offs
   - Destaque vantagens específicas de cada região

3. **Análise Técnica**
   - Revise a tabela comparativa detalhada
   - Discuta alertas e riscos identificados
   - Apresente análise de sensibilidade

4. **Documentação**
   - Salve o cenário para referência futura
   - Exporte CSV para anexar à proposta
   - Anote observações específicas do cliente

### Considerações Importantes

- **Valores São Estimativas**: Os dados regionais são baseados em médias de mercado. Sempre valide com dados específicos do projeto.
- **Incentivos Fiscais**: Variam por estado e podem mudar. Confirme benefícios atuais com órgãos competentes.
- **Conexão à Rede**: Prazos dependem da disponibilidade específica do ponto de conexão.
- **Custos de Terreno**: Variam significativamente dentro de cada região.
- **Infraestrutura Logística**: Considere necessidades específicas da indústria.

## Limitações e Próximos Passos

### Limitações Atuais
- Dados regionais agregados (não específicos por estado)
- Não considera custos logísticos detalhados
- Não inclui análise de risco político/regulatório
- Não considera disponibilidade de mão de obra

### Melhorias Futuras Sugeridas
- Integração com APIs de tarifas em tempo real
- Mapa interativo do Brasil com visualização geográfica
- Análise de risco mais detalhada
- Comparação com casos similares instalados
- Simulação de Monte Carlo para incertezas
- Integração com dados de transmissão da ONS

## Suporte Técnico

### Requisitos do Sistema
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Conexão à internet (para CDNs de React, Tailwind, Recharts)
- Python 3.7+ no servidor

### Resolução de Problemas

**Gráficos não aparecem:**
- Verifique conexão à internet
- Tente recarregar a página (Ctrl+F5)

**Cálculos parecem incorretos:**
- Revise os dados de entrada
- Verifique se os pesos somam próximo a 100%
- Confira o fator de carga (0-100%)

**Página não carrega:**
- Verifique se o servidor está rodando
- Confirme que não há outro processo na porta 8000
- Veja logs do servidor no terminal

## Informações Técnicas

### Tecnologias Utilizadas
- **Frontend**: React 18 (via CDN)
- **Estilização**: Tailwind CSS
- **Gráficos**: Recharts
- **Backend**: Python 3 com servidor HTTP nativo
- **Formato**: SPA (Single Page Application)

### Estrutura de Arquivos
```
templates/
  └── industrial_location.html    # Aplicação completa standalone
simple_server.py                  # Servidor com rota /industrial-location
```

### Personalização
Para customizar dados regionais, edite o objeto `REGIONAL_DATA` no arquivo `industrial_location.html` (linha ~35).

## Conclusão

Esta ferramenta foi desenvolvida para facilitar análises rápidas e fundamentadas de localização para plantas industriais eletrointensivas no Brasil. Ela oferece uma visão abrangente dos custos, prazos e trade-offs envolvidos, permitindo decisões mais informadas e apresentações profissionais para clientes.

Para dúvidas ou sugestões de melhoria, consulte a documentação técnica do projeto ou entre em contato com a equipe de desenvolvimento.
