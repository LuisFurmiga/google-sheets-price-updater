from config_vars import EMPTY_ITEM_NAME_FINISH_THE_PROGRAM, MY_FOREX, OPEN_MY_CHROME_ACCOUNT, SHEET_URL
from google_api import GoogleAPISheet
from open_browser import open_chrome, close_chrome
from scraper import ItemScraper
import requests
import time

def get_exchange_rate(from_currency, to_currency=MY_FOREX):
    """
    Obtém a taxa de câmbio da API AwesomeAPI.
    Exemplo: get_exchange_rate("USD") retorna a taxa de USD para MY_FOREX(BRL).
    """
    url = f"https://economia.awesomeapi.com.br/json/last/{from_currency}-{to_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        key = f"{from_currency}{to_currency}"
        if key in data:
            return float(data[key]["low"])  # Retorna o valor mais baixo do dia
    return None  # Retorna None se houver erro

def update_spreadsheet():
    """
    Atualiza a planilha com os preços atualizados dos itens e converte os valores para BRL.
    """
    
    sheet = GoogleAPISheet().setup_google_api(SHEET_URL)
    data = sheet.get_all_records()

    # Inicializa o WebDriver apenas uma vez para otimização
    selectors = {"price": "span.normal_price"}
    scraper = ItemScraper("https://steamcommunity.com/market/search?q=", selectors)

    # Forex Symbol: USD = Dólar; BRL = Real; CAD = Canadian Dollar; JPY = Japanese Yen
    prev_forex_symbol = None

    exchange_rate = 1

    for i, row in enumerate(data, start=2):  # Começa na linha 2 (pula o cabeçalho)
        item_name = row['Item']

        if not item_name:
            if EMPTY_ITEM_NAME_FINISH_THE_PROGRAM:
                print(f"Finalizando leitura. Acabaram se os itens!")
                break
            else:
                print(f"Pulando linha {i}: Nome do item está vazio")
                continue

        actual_price, forex_symbol = scraper.get_item_price(item_name)

        # Se não houver moeda ou preço, pula o item
        if not forex_symbol or not actual_price:
            print(f"Pulando '{item_name}'. Nenhum item encontrado")
            continue

        # Obtém a taxa de câmbio na primeira rodada ou caso tenha mudado de moeda
        if prev_forex_symbol != forex_symbol and forex_symbol != MY_FOREX:
            exchange_rate = get_exchange_rate(forex_symbol)
            prev_forex_symbol = forex_symbol 

        MIN_SALE_PRICE = 0.01
        # Pula o item caso não cumpra o valor mínimo de venda da Steam que é de 1 centavo de Dólar, ou 1 cent
        if float(actual_price) <= round(MIN_SALE_PRICE * exchange_rate, 2):
            print(f"Pulando '{item_name}'. Nenhum item a venda!")
            continue

        if forex_symbol == MY_FOREX:
            actual_price = str(actual_price).replace(".", ",")
            sheet.update_cell(i, 3, actual_price)  # Atualiza a coluna com novo valor
            print(f"'{item_name}': {actual_price} {forex_symbol}")
        elif exchange_rate:
            brl_price = round(float(actual_price) * exchange_rate, 2)  # Converte para MY_FOREX
            sheet.update_cell(i, 3, brl_price)  # Atualiza a coluna com novo valor calculado
            print(f"'{item_name}' convertido: {actual_price} {forex_symbol} → {brl_price} {MY_FOREX}")
        else:
            sheet.update_cell(i, 3, "Erro na cotação")
            print(f"Erro ao obter cotação para '{forex_symbol}'")
        time.sleep(1)

    scraper.close_driver()  # Encerra o WebDriver após a execução

if __name__ == "__main__":
    if OPEN_MY_CHROME_ACCOUNT:
        chrome_process = open_chrome()
    update_spreadsheet()
    if OPEN_MY_CHROME_ACCOUNT:
        close_chrome(chrome_process)
