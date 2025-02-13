import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = [
    "gspread",              # Acesso ao Google Sheets
    "oauth2client",         # Autenticação OAuth 2.0 para Google Sheets
    "requests",             # Para chamadas HTTP (conversão de moeda)
    "selenium",             # Automação de navegador
    "webdriver-manager"    # Gerencia automaticamente ChromeDriver e GeckoDriver
]

# Instalar pacotes Python
for package in required_packages:
    install(package)

print("Todos os pacotes necessários foram instalados com sucesso!")
