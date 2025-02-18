# README - Trabalho de Pesquisa Operacional

## Universidade Federal de São João del-Rei
**Departamento de Ciência da Computação**  
Disciplina: Pesquisa Operacional  
Professor: Guilherme de Castro Pena  
Data de Entrega: 17/02/2025  

### Descrição
Este repositório contém a implementação dos modelos de **Programação Linear Inteira (PLI)** para os problemas clássicos estudados na disciplina de Pesquisa Operacional. Os modelos foram desenvolvidos utilizando o **IBM CPLEX** com a linguagem **Python** e resolvem os seguintes problemas:

1. **Problema do Caminho Mínimo (PCM)** - `pcm.py`
2. **Problema da Designação (PD)** - `pd.py`
3. **Problema de Fluxo de Custo Mínimo (PFCM)** - `pfcm.py`
4. **Problema de Fluxo Máximo (PFM)** - `pfm.py`
5. **Problema do Transporte (PT)** - `pt.py`

Cada problema foi modelado de acordo com as instruções do trabalho, utilizando variáveis inteiras ou binárias conforme especificado.

---

## 1. Problemas Modelados

### 1.1. Problema do Caminho Mínimo (PCM)
- **Arquivo:** `pcm.py`
- **Descrição:** Resolve o problema de encontrar o caminho mínimo entre um vértice de origem e um de destino em um grafo ponderado.
- **Variáveis:** Binárias
- **Entrada:** Um arquivo `in.txt` contendo:
  - Primeira linha: `N M` (número de vértices e arestas)
  - Linhas seguintes: `A B C` (aresta entre os vértices A e B com custo C)
- **Saída:** Caminho mínimo encontrado e custo total.

### 1.2. Problema da Designação (PD)
- **Arquivo:** `pd.py`
- **Descrição:** Resolve o problema de atribuir tarefas a trabalhadores minimizando o custo total.
- **Variáveis:** Binárias
- **Entrada:** Um arquivo `in.txt` contendo:
  - Primeira linha: `N` (tamanho da matriz de custos, deve ser quadrada)
  - Próximas `N` linhas: Matriz de custos
- **Saída:** Atribuição ótima de tarefas a trabalhadores e custo total mínimo.

### 1.3. Problema de Fluxo de Custo Mínimo (PFCM)
- **Arquivo:** `pfcm.py`
- **Descrição:** Resolve o problema de encontrar o fluxo de menor custo em uma rede com restrições de capacidade.
- **Variáveis:** Inteiras
- **Entrada:** Um arquivo `in.txt` contendo:
  - Primeira linha: `N M` (número de vértices e arestas)
  - Linhas seguintes: `A B C` (aresta entre os vértices A e B com capacidade C)
- **Saída:** Fluxo ótimo com menor custo.

### 1.4. Problema de Fluxo Máximo (PFM)
- **Arquivo:** `pfm.py`
- **Descrição:** Resolve o problema de encontrar o maior fluxo possível entre um nó fonte e um nó destino em uma rede.
- **Variáveis:** Inteiras
- **Entrada:** Um arquivo `in.txt` contendo:
  - Primeira linha: `N M` (número de vértices e arestas)
  - Linhas seguintes: `A B C` (aresta entre os vértices A e B com capacidade C)
- **Saída:** Fluxo máximo encontrado e caminho correspondente.

### 1.5. Problema do Transporte (PT)
- **Arquivo:** `pt.py`
- **Descrição:** Resolve o problema de transporte, minimizando os custos de envio entre fornecedores e destinos.
- **Variáveis:** Inteiras
- **Entrada:** Um arquivo `in.txt` contendo:
  - Primeira linha: `S D` (número de fornecedores e destinos)
  - Próximas `S` linhas: Oferta de cada fornecedor
  - Próximas `D` linhas: Demanda de cada destino
  - Próximas `S` linhas: Matriz de custos
- **Saída:** Quantidades enviadas de cada fornecedor para cada destino e custo total mínimo.

---

## 2. Requisitos de Execução
- **Python 3.7+**
- **IBM CPLEX (docplex)**
- **Bibliotecas:** `pandas`, `psutil`, `os`, `time`

Para instalar as dependências, execute:
```bash
pip install docplex pandas psutil
```

---

## 3. Como Executar
Cada script pode ser executado diretamente pelo terminal da seguinte forma:
```bash
python nome_do_arquivo.py
```
**Exemplo:**
```bash
python pcm.py
```
Certifique-se de que um arquivo `in.txt` correspondente ao problema está no mesmo diretório do script.

---

## 4. Estrutura do Repositório
```
|-- tp_po/
    |-- src
        |-- pcm.py        # Problema do Caminho Mínimo
        |-- pd.py         # Problema da Designação
        |-- pfcm.py       # Problema de Fluxo de Custo Mínimo
        |-- pfm.py        # Problema de Fluxo Máximo
        |-- pt.py         # Problema do Transporte
        |-- in.txt        # Arquivo de entrada (exemplo para cada problema)
    |-- README.md     # Este arquivo
```

---

**Autores:**
- Gabriel Souza de Oliveira 
- Lucas Mendonça Sacchi

**Observação:** Este projeto foi desenvolvido para fins acadêmicos na disciplina de Pesquisa Operacional da UFSJ.
