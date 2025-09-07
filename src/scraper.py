import re
import tempfile
from config_vars import CHROME_PROFILE_PATH, DEBUG_PORT, MY_FOREX, OPEN_MY_CHROME_ACCOUNT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ItemScraper:
    def __init__(self, url, selectors):
        """
        Inicializa o WebDriver e configura os seletores para busca.
        """
        self.url = url
        self.selectors = selectors
        self.driver = self._setup_driver()

    def _setup_driver(self) -> WebDriver:
        """
        Configura o WebDriver para uso com o Chrome.
        """
        options = webdriver.ChromeOptions()
        service = Service(
                ChromeDriverManager().install(),
                log_path="NUL"  # <- Caso queira bloquear Logs no Linux use "/dev/null"
            )
        if not OPEN_MY_CHROME_ACCOUNT:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--log-level=3")
            options.add_argument("user-agent=Mozilla/5.0")
            # Criar diretório temporário para o perfil
            #temp_profile_dir = tempfile.mkdtemp()
            #options.add_argument(f"--user-data-dir={temp_profile_dir}")
        else:
            options.debugger_address = f"127.0.0.1:{DEBUG_PORT}"

        return webdriver.Chrome(service=service, options=options)

    def get_item_price(self, item_name):
        """
        Busca o preço do item no mercado da Steam.
        """
        try:
            formatted_name = item_name.replace(' ', '+')
            url = f"{self.url}{formatted_name}"

            self.driver.get(url)
            print(f" Acessando: {url}")

            # Aguarda até que os resultados sejam carregados
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.market_listing_row"))
                )
            except:
                print(f" Nenhum resultado encontrado para '{item_name}'")
                return None, None

            # Agora tenta pegar o preço
            selector = self.selectors.get("price", "span.normal_price")

            try:
                element_price = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                price_text = element_price.text.strip()
            except:
                print(f" Elemento de preço não encontrado para '{item_name}'. Verificando HTML...")
                print(self.driver.page_source[:1000])  # Mostra parte do HTML para depuração
                return None, None
            
            # Expressão regular para capturar apenas o valor numérico e a moeda
            regex = r"(R\$)?\s?(\d+[\.,]\d{2})\s?([A-Z]{3})?"
            price_match = re.search(regex, price_text)

            if price_match:
                brl_symbol = price_match.group(1)  # Captura "R$" se houver
                value = price_match.group(2)  # Captura o valor numérico
                forex = price_match.group(3)  # Captura a moeda Forex (USD, EUR, etc.)

                # Se "R$" for encontrado, assume "BRL" como moeda
                if brl_symbol:
                    forex = MY_FOREX

                if forex == MY_FOREX:
                    value = value.replace(",", ".")

                return value, forex
            else:
                print(f" Formato inesperado para '{item_name}': {price_text}")
                return None, None

        except Exception as e:
            print(f" Erro ao obter o preço de '{item_name}': {e}")
            return None, None

    def close_driver(self):
        """
        Fecha o navegador controlado pelo Selenium.
        """
        self.driver.quit()
