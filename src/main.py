from logger import logger
from api_client import APIClientService
from database import DatabaseConnection
from google_sheets_service import GoogleSheetsService
from pathlib import Path
import json
from email_service import EmailService

def main():

    client = APIClientService(
        client='Skillfactory',
        client_key='M2MGWS',
        api_url='https://b2b.itresume.ru/api/statistics'
    )

    data = client.fetch_data(
        start_date='2026-04-25 00:00:00.00',
        end_date='2026-04-26 00:00:00.00'
    )
    
    db = None

    if data:
        try:
            db = DatabaseConnection.get_instance()

            db.post_data(data)

            metrics = calculate_metrics(data)

            uploader = GoogleSheetsService()

            uploader.upload_data(metrics)

            current_dir = Path(__file__).resolve().parent

            email_config_path = current_dir.parent / "data" / "email_config.json"

            with open(email_config_path, "r", encoding="utf-8") as f:
                EMAIL_CONFIG = json.load(f)

            mail_sender = EmailService(**EMAIL_CONFIG)

            url = 'https://docs.google.com/spreadsheets/d/1e-ANzHGEP9uwjbBGUNCXiSRPV-p17ClOm3C0NUlCu6o'

            mail_sender.send_email(
                recipient='liza.rachevskaya@mail.ru',
                body = f'Check the google-sheets table for new info:<br><a href="{url}">{url}</a>',
                subject = 'New metrics counted'
            )

        except Exception as ex:
            logger.error(ex)

        finally:
            if db:
                db.close()

def calculate_metrics(data_list):
    res = {'allAttemptsCount': len(data_list),
           'runAttemptsCount': 0,
           'submitAttemptsCount': 0,
           'successSubmitConversion': 0,
           'uniqueUsersCount': 0
        }
    
    res['runAttemptsCount'] = sum(1 for x in data_list if x.get('attempt_type') == 'run')
    res['submitAttemptsCount'] = len(data_list) - res['runAttemptsCount']

    if res['submitAttemptsCount'] != 0:
        res['successSubmitConversion'] = sum(1 for x in data_list if x.get('attempt_type') == 'submit' and x.get('is_correct') == True)*1.0/res['submitAttemptsCount']

    res['uniqueUsersCount'] = len({x['user_id'] for x in data_list if 'user_id' in x})

    return res

if __name__ == "__main__":
    main()