from logger import logger
from api_client import get_data
from database import DatabaseConnection

def main():

    data = get_data()

    db = None

    if data:
        try:
            db = DatabaseConnection.get_instance()

            db.post_data(data)

        except Exception as ex:
            logger.error(ex)

        finally:
            if db:
                db.close()


if __name__ == "__main__":
    main()