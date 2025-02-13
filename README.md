# Google Sheets Price Updater

Este script automatiza a coleta de preços do **mercado Steam** e atualiza os valores em uma **planilha do Google Sheets**, incluindo a conversão de moeda via API.

---

## 📌 **Pré-requisitos**
Antes de executar o script, instale os seguintes pacotes:

### 🔹 **1. Instalar as dependências**
Rode o comando abaixo para instalar todas as bibliotecas necessárias:
```sh
python requirements.py
```
Caso queira instalar manualmente:
```sh
pip install selenium webdriver-manager gspread oauth2client requests
```

---

## ⚙️ **Configuração**
### 🔹 **1. Configurar o Google Sheets**
1. **Criar um projeto no Google Cloud**:  
   - [Google Cloud Console](https://console.cloud.google.com/)
   - Crie um novo projeto (Exemplo: `Steam Price Updater`)

2. **Ativar APIs do Google Sheets e Google Drive**:
   - Ativar [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)
   - Ativar [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)

3. **Criar credenciais da Conta de Serviço**:
   - Vá para [Credenciais do Google](https://console.cloud.google.com/apis/credentials)
   - Crie uma **nova Conta de Serviço** → Gere uma chave **JSON** → Baixe, renomeie como `credentials.json` e cole dentro da pasta `config`.
   - Caso tenha dúvida a respeito de como deve ser a estrutura das pastas do projeto, siga para o tópico [Estrutura do Projeto](--estrutura-do-projeto-)

4. **Compartilhar a planilha**:
   - Abra a **planilha do Google Sheets**
   - Compartilhe com o e-mail presente em `credentials.json`.


### 🔹 **2. Configurar o `config_vars.py`**
No arquivo `config_vars.py`, ajuste:
```py

SHEET_URL = "https://docs.google.com/spreadsheets/d/SEU_ID"

```

---

## 📄  Estrutura do Projeto 

```
📁 google-sheets-price-updater/
│── config/
│   └── credentials.json
│── src/
│   ├── config_vars.py
│   ├── main.py
│   ├── open_browser.py
│   └── scraper.py
└── requirements.py
```

## 🚀 **Como rodar o script**

### 🔹 **1. Rodar o script principal**
```sh
python main.py
```
Isso irá buscar os preços e atualizar sua planilha automaticamente. ✅

---

## 🔧 **Possíveis problemas e soluções**

### 🚨 **1. `WebDriverException: chromedriver.exe unexpectedly exited`**
**Solução:**
```sh
pip uninstall webdriver-manager
pip install webdriver-manager
```

### 🚨 **2. `ModuleNotFoundError: No module named 'gspread'`**
**Solução:**
```sh
pip install gspread oauth2client
```

### 🚨 **3. O Chrome abre, mas não acessa os preços**
**Solução:**
- Certifique-se de que **Steam está acessível** no seu navegador.
- Teste abrir manualmente: [https://steamcommunity.com/market/](https://steamcommunity.com/market/)

---
