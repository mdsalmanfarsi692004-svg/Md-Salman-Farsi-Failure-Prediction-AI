import psycopg2

# CHANGE ONLY THE PASSWORD BELOW
DB_CONFIG = {
    "host": "localhost",
    "database": "ml_project",
    "user": "postgres",
    "password": "Farsi@2004",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
