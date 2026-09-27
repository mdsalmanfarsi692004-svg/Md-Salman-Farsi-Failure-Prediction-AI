import psycopg2
import os

def get_connection():
    # Render cloud database ke liye environment variable check karega
    db_url = os.getenv("DATABASE_URL")
    
    if db_url:
        # Agar Render par hai, toh cloud database se connect hoga
        return psycopg2.connect(db_url)
    else:
        # Agar tere laptop par hai, toh purana local setup chalega
        DB_CONFIG = {
            "host": "localhost",
            "database": "ml_project",
            "user": "postgres",
            "password": "Farsi@2004",
            "port": 5432
        }
        return psycopg2.connect(**DB_CONFIG)
