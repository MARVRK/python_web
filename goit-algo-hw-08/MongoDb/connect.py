from mongoengine import connect, connection, ConnectionFailure
import configparser


def connect_to_database():
    try:
        connection.disconnect()
        config = configparser.ConfigParser()
        config.read('config.ini')

        mongo_user = config.get('DB', 'user')
        mongodb_pass = config.get('DB', 'pass')
        db_name = config.get('DB', 'db_name')
        domain = config.get('DB', 'domain')

        # Adjusted connection string with your MongoDB Atlas credentials and database name
        connect(
            host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority",
            ssl=True
        )
    except ConnectionFailure:
        pass