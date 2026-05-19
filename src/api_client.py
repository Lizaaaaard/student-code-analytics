import requests
import ast
from datetime import datetime
from logger import logger

def get_data():
    api_url = "https://b2b.itresume.ru/api/statistics"

    params = {
    'client': 'Skillfactory',
    'client_key': 'M2MGWS',
    'start': '2023-04-25 12:00:47.860798',
    'end': '2023-04-25 18:00:47.860798'
    }

    res = []

    try:
        r = requests.get(api_url, params=params)

        r.raise_for_status()

        logger.info(f'Data from API received successfully, status: {r.status_code}')
        
        data = r.json()        

        res = validate_data(data)

        logger.info('The data has been validated')
        
        return res

    except requests.exceptions.HTTPError as err:
        logger.error(f"Ошибка HTTP: {err}")

    except Exception as e:
        logger.error(f"Другая ошибка: {e}")

    return None

def validate_data(incoming_data):
    logger.info('Launch validation')
    
    expected_types = {
        'user_id': str,
        'created_at': str,
        'is_correct': (bool, type(None)),
        'lis_outcome_service_url': str,
        'lis_result_sourcedid': str,
        'attempt_type': str
    }

    field_constraints = {
    'attempt_type': ['run', 'submit']
    }

    outcome_data = []

    for row in incoming_data:
        if "lti_user_id" in row:
            row["user_id"] = row.pop("lti_user_id")

        params = row.pop("passback_params", None)

        if params:
            if isinstance(params, str):
                try:
                    params = ast.literal_eval(params)
                except (ValueError, SyntaxError):
                    logger.error(f"String parsing error: {params}")
                    params = {}

        if isinstance(params, dict):
            row.update(params)
        else:
            logger.error(f"Unexpected data type in passback_params: {type(params)}")
            continue
        
        is_row_valid = True

        for key, expected_type in expected_types.items():
            val = row.get(key)

            if not isinstance(val, expected_type):
                logger.error(f"Type Error: {key} must be {expected_type}, but received {type(val)}")
                is_row_valid = False
                break
            
            if key == 'created_at':
                row['created_at'] = datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')

            if key in field_constraints:
                if val not in field_constraints[key]:
                    logger.error(f"Value error: {key} contains '{val}', but only {field_constraints[key]} is allowed")
                    is_row_valid = False
                    break

        if is_row_valid:
            outcome_data.append(row)
    
    return outcome_data