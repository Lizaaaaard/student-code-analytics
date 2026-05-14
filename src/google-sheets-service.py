from pathlib import Path
import gspread

BASE_DIR = Path(__file__).parent.parent

CREDENTIALS_FILE = BASE_DIR / "data" / 'creds.json'
TABLE_NAME = "student-code-analytics"


def sheets_connect(data_list):
    gc = gspread.service_account(CREDENTIALS_FILE)

    wks = gc.open(TABLE_NAME).sheet1

    wks.update([[1, 2], [3, 4]], 'A1')

    wks.update_acell('B42', "it's down there somewhere, let me take another look.")

    wks.format('A1:B1', {'textFormat': {'bold': True}})


if __name__ == "__main__":
    sheets_connect()
