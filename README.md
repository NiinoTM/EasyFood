# 🍽️ EasyFood - Sistema de Gestão Alimentícia (SGA)

Um sistema para gerenciamento de alimentos, estoque, fornecedores e refeições, com relatórios nutricionais e financeiros.

---

## 📋 Descrição
Sistema desenvolvido para controle de:
- Cadastro de alimentos com informações nutricionais
- Gerenciamento de fornecedores
- Movimentações de estoque (entradas/saídas)
- Criação de refeições padrão
- Geração de relatórios:
  - Nutricionais (projeções diárias/semanais/mensais)
  - Financeiros (custos por refeição)
  - Análise de estoque

---

## ⚙️ Funcionalidades Principais
1. **Alimentos**
   - Cadastro com detalhes nutricionais (proteínas, carboidratos, etc.)
   - Controle de estoque mínimo/ideal
   - Histórico de edições

2. **Fornecedores**
   - Cadastro por tipo (mercado, padaria, etc.)
   - Vinculação com entradas de estoque

3. **Estoque**
   - Registro de entradas (com custo e fornecedor)
   - Registro de saídas (com motivo)
   - Conversão automática de unidades

4. **Refeições**
   - Composição com múltiplos alimentos
   - Edição flexível de porções

5. **Relatórios**
   - Nutricional: calorias, macros e projeções
   - Financeiro: custos por refeição e projeções
   - Estoque: duração atual e status

---

## 🛠️ Instalação e Uso

1. **Pré-requisitos**
   - Python 3.x instalado
   - Biblioteca `tabulate`:
     ```bash
     pip install tabulate
     ```

2. **Execução**
   ```bash
   # Windows
   encodingUTF8.bat

   # Linux/macOS
   PYTHONUTF8=1 python main.py

   ---

## 🔄 Fluxo Recomendado
1. **Cadastre alimentos** (`1. Alimentos`)  
   - Defina nome, unidade, valores nutricionais e estoque

2. **Adicione fornecedores** (`2. Fornecedores`)  
   - Registre mercado/açougue/padaria com localização

3. **Registre entradas no estoque** (`3. Estoque`)  
   - Relacione alimentos com fornecedores e custos

4. **Crie refeições** (`4. Refeições`)  
   - Combine alimentos em preparos padrão com porções

5. **Gere relatórios** (`5. Relatórios`)  
   - Analise nutrição, custos e status do estoque

---

## 🗄️ Estrutura de Dados
Arquivos JSON salvos em `/data`:
- `foods.json`: Alimentos cadastrados
- `suppliers.json`: Fornecedores
- `stock_entries.json`: Histórico de entradas
- `stock_exits.json`: Histórico de saídas  
- `meals.json`: Refeições padrão

---

## 📦 Módulos Principais
| Arquivo          | Descrição                                  |
|------------------|--------------------------------------------|
| `main.py`        | Menu principal e fluxo do sistema         |
| `alimentos.py`   | Gestão de alimentos e nutrição            |
| `fornecedores.py`| Cadastro de fornecedores                  |
| `estoque.py`     | Controle de entradas/saídas de estoque    |
| `refeicoes.py`   | Criação e edição de refeições             |
| `relatorios.py`  | Geração de relatórios nutricionais/financeiros |

---

## 📌 Notas
- Interface totalmente em Português
- Dados salvos em UTF-8
- Compatível com Windows/Linux/macOS
- Cálculos precisos com conversão automática de unidades (gramas, litros, etc.)

---

## 📄 Licença
Distribuído sob licença MIT. Consulte o arquivo LICENSE para detalhes.
