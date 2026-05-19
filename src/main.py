from logger import logger
from api_client import get_data
from database import DatabaseConnection
from google_sheets_service import sheets_connect

def main():

    data = get_data()
    db = None

    if data:
        try:
            db = DatabaseConnection.get_instance()

            db.post_data(data)

            metrics = calculate_metrics(data)

            sheets_connect(metrics)

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