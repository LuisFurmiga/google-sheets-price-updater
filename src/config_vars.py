import os
import shutil
from pathlib import Path

# URL da Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/SEU_ID"

DEBUG_PORT = "9222"

# Caso encontre um item sem nome ele vai considerar que a lista acabou? True = Finaliza o programa ou False = Continua lendo até finalizar todas linhas que foram passadas
EMPTY_ITEM_NAME_FINISH_THE_PROGRAM = True

# Caso queira usar um perfil com Cookies e sessão logada, True. Caso contrario, False
OPEN_MY_CHROME_ACCOUNT = False

# A moeda base que estou utilizando e não precisa de conversão caso venha nesse valor
MY_FOREX = "BRL"

def get_chrome_path():
    """
    Retorna o caminho do executável do Google Chrome automaticamente.
    """
    if os.name == "nt":  # Windows
        # Procura em locais comuns
        possible_paths = [
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
            Path(os.getenv("LOCALAPPDATA") + r"\Google\Chrome\Application\chrome.exe")
        ]
        for path in possible_paths:
            if path.exists():
                return str(path)

        # Tenta encontrar pelo registro do Windows
        from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE
        try:
            with OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe") as key:
                path, _ = QueryValueEx(key, "")
            return str(path)
        except Exception:
            pass

    else:  # Linux/macOS
        path = shutil.which("google-chrome") or shutil.which("chrome") or shutil.which("chromium")
        if path:
            return str(path)

        # Verifica caminho no macOS
        mac_path = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if mac_path.exists():
            return str(mac_path)

    return None  # Retorna None se não encontrar o Chrome


def get_chrome_profile_path():
    """
    Retorna o caminho do perfil padrão do Google Chrome automaticamente.
    """
    if os.name == "nt":  # Windows
        return str(Path(os.getenv("LOCALAPPDATA")) / "Google" / "Chrome" / "User Data")
    else:  # Linux/macOS
        linux_path = Path(os.getenv("HOME")) / ".config" / "google-chrome"
        mac_path = Path(os.getenv("HOME")) / "Library" / "Application Support" / "Google" / "Chrome"
        
        return str(linux_path) if linux_path.exists() else str(mac_path)

# Abra o Chrome e na barra de endereço digite: 
# chrome://version/

# Caminho do perfil do Google Chrome
# Pegue o "Caminho de Perfil" e cole aqui embaixo.
# Colar o caminho até \User Data
CHROME_PROFILE_PATH = get_chrome_profile_path()

CHROME_PATH = get_chrome_path()
