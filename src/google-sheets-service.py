from pathlib import Path
import googleapiclient.discovery
from google.oauth2 import service_account

BASE_DIR = Path(__file__).parent.parent

CREDENTIALS_FILE = BASE_DIR / "data" / 'student-code-analytics-495616-2cf9a9519186.json'

def sheets_connect():
    SCOPES = [
        'https://googleapis.com',
        'https://googleapis.com'
    ]
    
    credentials = service_account.Credentials.from_service_account_file(str(CREDENTIALS_FILE), scopes=SCOPES)
    
    service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)

    spreadsheet_body = {
        'properties': {'title': 'Student`s code metrics', 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                'sheetId': 0,
                                'title': 'Metrics',
                                'gridProperties': {'rowCount': 8, 'columnCount': 5}}}]}

    try:
        response = service.spreadsheets().create(body=spreadsheet_body).execute()
        print(f"Успех! ID таблицы: {response.get('spreadsheetId')}")
        return response
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

if __name__ == "__main__":
    sheets_connect()