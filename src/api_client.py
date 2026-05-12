import requests
import ast
from datetime import datetime
from logger import logger

def get_data():
    api_url = "https://b2b.itresume.ru/api/statistics"

    params = {
    'client': 'Skillfactory',
    'client_key': 'M2MGWS',
    'start': '2023-04-01 12:46:47.860798',
    'end': '2023-04-01 13:46:47.860798'
    }

    res = []

    try:
        r = requests.get(api_url, params=params)

        r.raise_for_status()

        logger.info(f'Данные с API успешно получены, статус: {r.status_code}')
        
        data = r.json()        

        res = validate_data(data)

        logger.info('Данные прошли пре-валидацию')
        
        return res

    except requests.exceptions.HTTPError as err:
        logger.error(f"Ошибка HTTP: {err}")

    except Exception as e:
        logger.error(f"Другая ошибка: {e}")

    return None

def validate_data(incoming_data):
    logger.info('Запуск пре-валидации')
    
    expected_types = {
        'user_id': str,
        'created_at': str,
        'is_correct': (bool, type(None))
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
                    logger.error(f"Ошибка парсинга строки: {params}")
                    params = {}

        if isinstance(params, dict):
            row.update(params)
        else:
            logger.error(f"Неожиданный тип данных в passback_params: {type(params)}")
            continue
        
        is_row_valid = True

        for key, expected_type in expected_types.items():
            val = row.get(key)

            if not isinstance(val, expected_type):
                logger.error(f"Ошибка типа: {key} должен быть {expected_type}, а пришел {type(val)}")
                is_row_valid = False
                break
            
            if key == 'created_at':
                row['created_at'] = datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')

            if key in field_constraints:
                if val not in field_constraints[key]:
                    logger.error(f"Ошибка значения: {key} содержит '{val}', а можно только {field_constraints[key]}")
                    is_row_valid = False
                    break

        if is_row_valid:
            outcome_data.append(row)
    
    return outcome_data

#print(get_data())