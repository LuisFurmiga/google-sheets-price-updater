from oauth2client.service_account import ServiceAccountCredentials
import gspread

class GoogleAPISheet:
        
    def setup_google_api(self, sheet_url):
        """
        Configuração do acesso ao Google Sheets
        """
        CREDENTIALS_PATH = "../config/credentials.json"  # Ajuste o caminho correto

        # Inicializar credenciais e autenticação com Google Sheets
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
        client = gspread.authorize(creds)  # type: ignore
        sheet = client.open_by_url(sheet_url).sheet1

        return sheet
