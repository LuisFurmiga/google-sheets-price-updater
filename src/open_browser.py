from config_vars import CHROME_PATH, CHROME_PROFILE_PATH, DEBUG_PORT
import os
import subprocess

def open_chrome():
    # Comando para abrir o Chrome no modo depuração
    chrome_cmd = f'"{CHROME_PATH}" --remote-debugging-port={DEBUG_PORT} --headless=new --disable-gpu --user-data-dir="{CHROME_PROFILE_PATH}"'
    # Inicia o Chrome
    chrome_process = subprocess.Popen(
        chrome_cmd, 
        shell=True, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    return chrome_process

# Retorna o processo para poder encerrá-lo depois
def close_chrome(chrome_process):
    print("Encerrando o Chrome iniciado pelo script...")
    chrome_process.terminate()  # Mata o processo iniciado pelo script
    #os.system('taskkill /F /IM chrome.exe /T')
