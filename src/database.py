import psycopg2
from psycopg2.extras import execute_values
from logger import logger

HOST = 'localhost'
PORT = 5432
DATABASE = 'student-code-analytics'
USER = 'postgres'
PASSWORD = 'postgres'

class DatabaseConnection:
    __instance = None

    @staticmethod
    def get_instance():
        if not DatabaseConnection.__instance:
            DatabaseConnection()
        return DatabaseConnection.__instance

    def __init__(self):
        if DatabaseConnection.__instance:
            logger.error("Подключение уже установлено")
        else:
            self.connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
            self.cursor = self.connection.cursor()
            DatabaseConnection.__instance = self
            logger.info('Соединение с БД установлено')

    def save(self):
        self.connection.commit()
        logger.info('Запрос в БД успешно сохранен')

    def close(self):
        self.cursor.close()
        self.connection.close()
        logger.info('Соединение с БД закрыто')

    def post_data(self, data_list):       
        columns = ['oauth_consumer_key', 'user_id', 'attempt_type', 'is_correct', 'lis_outcome_service_url', 'created_at', 'lis_result_sourcedid']

        query = f"INSERT INTO data ({', '.join(columns)}) VALUES %s"

        values = [[item[column] for column in columns] for item in data_list]

        try:
            execute_values(self.cursor, query, values)

            self.save()

        except Exception as ex:
            self.connection.rollback()
            logger.error(f"Ошибка при сохранении записи в БД: {ex}")
            raise ex