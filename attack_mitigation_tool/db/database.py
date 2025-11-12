import pymysql
import os
from config import Config

def get_db_connection(secure=False):
    """
    Creates a database connection based on the security setting.
    
    Args:
        secure (bool): Whether to use secure database practices
    
    Returns:
        connection: A database connection object
    """
    # For demonstration purposes, we're using the same connection
    # In a real app, you would implement different security practices
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def execute_query(query, params=None, secure=False):
    """
    Executes a database query.
    
    Args:
        query (str): SQL query to execute
        params (tuple): Parameters for the query
        secure (bool): Whether to use secure database practices
    
    Returns:
        result: Query result
    """
    conn = get_db_connection(secure)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def execute_update(query, params=None, secure=False):
    """
    Executes a database update query.
    
    Args:
        query (str): SQL query to execute
        params (tuple): Parameters for the query
        secure (bool): Whether to use secure database practices
    
    Returns:
        int: Number of affected rows
    """
    conn = get_db_connection(secure)
    try:
        with conn.cursor() as cursor:
            affected_rows = cursor.execute(query, params)
            conn.commit()
            return affected_rows
    finally:
        conn.close()

def init_db():
    """Initialize the database with test data."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Read schema.sql file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.join(current_dir, 'schema.sql')
            
            with open(schema_path, 'r') as f:
                sql_schema = f.read()
            
            # Execute schema commands
            for statement in sql_schema.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            
            conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()