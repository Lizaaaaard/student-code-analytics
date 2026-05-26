import requests
import ast
from datetime import datetime
from logger import logger

class DataValidator:
    EXPECTED_TYPES = {
        'user_id': str,
        'created_at': str,
        'is_correct': (bool, type(None)),
        'lis_outcome_service_url': str,
        'lis_result_sourcedid': str,
        'attempt_type': str
    }

    FIELD_CONSTRAINTS = {"attempt_type": ["run", "submit"]}

    @classmethod
    def validate_data(cls, row):
 
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
                return None

            for key, expected_type in cls.EXPECTED_TYPES.items():
                val = row.get(key)

                if not isinstance(val, expected_type):
                    logger.error(f"Type Error: {key} must be {expected_type}, but received {type(val)}")
                    return None
                
                if key == 'created_at':
                    try:
                        row['created_at'] = datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError as ex:
                         logger.error(f"Date format error in {key}: {ex}")
                         return None

                if key in cls.FIELD_CONSTRAINTS:
                    if val not in cls.FIELD_CONSTRAINTS[key]:
                        logger.error(f"Value error: {key} contains '{val}', but only {cls.FIELD_CONSTRAINTS[key]} is allowed")
                        return None

        return row

class APIClientService:
    def __init__(self, client, client_key, api_url):
        self.client = client
        self.client_key = client_key
        self.api_url = api_url

        
    def fetch_data(self, start_date, end_date):
        params = {
        'client': self.client,
        'client_key': self.client_key,
        'start': start_date,
        'end': end_date
        }

        try:
            r = requests.get(self.api_url, params=params)

            r.raise_for_status()

            logger.info(f'Data from API received successfully, status: {r.status_code}')
                 
            return self.process_data(r.json())        

        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error: {err}")

        except Exception as e:
            logger.error(f"Other error: {e}")

        return None
    
    def process_data(self, incoming_data):
        logger.info('Launch validation')

        res = []

        for row in incoming_data:
            validated_row = DataValidator.validate_data(row)

            if validated_row is not None:
                res.append(validated_row)

        logger.info('The data has been validated')
        return res


