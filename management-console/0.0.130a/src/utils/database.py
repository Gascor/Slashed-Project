import pymysql
import logging
from werkzeug.security import generate_password_hash, check_password_hash

def verify_credentials(username, password, db_host, db_user, db_password, db_name):
    connection = None
    try:
        logging.debug(f"Trying to connect to the database at {db_host} as {db_user}")
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        logging.debug(f"User fetched from database: {user}")
        if user and check_password_hash(user['password_hash'], password):
            return True
        return False
    except pymysql.MySQLError as err:
        logging.error(f"Database connection failed: {err}")
        return False
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        return False
    finally:
        if connection and connection.open:
            cursor.close()
            connection.close()

def reset_database(db_host, db_user, db_password):
    connection = None
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        cursor = connection.cursor()

        # Générer le mot de passe haché pour GascorSU
        hashed_password = generate_password_hash('HanaInari78&')

        commands = [
            "DROP DATABASE IF EXISTS slashed_project",
            "CREATE DATABASE slashed_project",
            "USE slashed_project",
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            f"INSERT INTO users (username, password_hash) VALUES ('GascorSU', '{hashed_password}')",
            "CREATE USER IF NOT EXISTS 'GascorSU'@'%' IDENTIFIED BY 'HanaInari78&'",
            "GRANT ALL PRIVILEGES ON *.* TO 'GascorSU'@'%' WITH GRANT OPTION",
            "FLUSH PRIVILEGES"
        ]
        for command in commands:
            cursor.execute(command)
        connection.commit()
        return True
    except pymysql.MySQLError as err:
        logging.error(f"Error resetting database: {err}")
        return False
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        return False
    finally:
        if connection and connection.open:
            cursor.close()
            connection.close()