from pathlib import Path
import gspread
from logger import logger
from gspread.utils import rowcol_to_a1

BASE_DIR = Path(__file__).parent.parent

CREDENTIALS_FILE = BASE_DIR / "data" / 'creds.json'
TABLE_NAME = "student-code-analytics"


def sheets_connect(data_dict):
    header = [key for key in data_dict.keys()]

    end_cell = rowcol_to_a1(1, len(data_dict.keys())) 

    gc = gspread.service_account(CREDENTIALS_FILE)

    wks = gc.open(TABLE_NAME).sheet1

    logger.info('Access to Google Sheets spreadsheet has been obtained')

    values = [
        list(data_dict.keys()),
        list(data_dict.values())
    ]

    wks.update(values, "A1")

    wks.format(f'A1:{end_cell}', {'textFormat': {
                          "bold": True,
                          "fontSize": 12,
                          "foregroundColor": {
                            "red": 1.0,
                            "green": 1.0,
                            "blue": 1.0
                            }},
                        "horizontalAlignment": "CENTER",
                        "backgroundColor": {
                          "red": 172,
                          "green": 172,
                          "blue": 172
                        }
    })
    
    logger.info('The data has been uploaded to a Google Sheets spreadsheet')
