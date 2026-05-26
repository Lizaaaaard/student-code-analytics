from pathlib import Path
import gspread
from logger import logger
from gspread.utils import rowcol_to_a1

BASE_DIR = Path(__file__).parent.parent

TABLE_NAME = "student-code-analytics"

class GoogleSheetsService:
    def __init__(self):
        self.table_name = 'student-code-analytics'
        self.credentials_path = BASE_DIR / "data" / "creds.json"
        self.wks = None

    def connect(self):
        if self.wks is None:
            gc = gspread.service_account(self.credentials_path)
            self.wks = gc.open(self.table_name).sheet1

        logger.info(f"Access to Google Sheets table '{self.table_name}'spreadsheet has been obtained")
        return self.wks
    
    def upload_data(self, data_dict):
        if not data_dict:
            logger.warning("Data dictionary is empty. Nothing to upload.")
            return
        
        wks = self.connect()

        values = [list(data_dict.keys()), list(data_dict.values())]

        end_cell = rowcol_to_a1(1, len(data_dict))

        wks.update(values, "A1")

        wks.format(
            f"A1:{end_cell}",
            {
                "textFormat": {
                    "bold": True,
                    "fontSize": 12,
                    "foregroundColor": {
                        "red": 1.0,
                        "green": 1.0,
                        "blue": 1.0,
                    },
                },
                "horizontalAlignment": "CENTER",
                "backgroundColor": {
                    "red": 0.67,
                    "green": 0.67,
                    "blue": 0.67,
                },
            },
        )

        logger.info("The data has been uploaded to a Google Sheets spreadsheet")
