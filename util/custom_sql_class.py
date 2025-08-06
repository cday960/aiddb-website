from typing import List

# from pyodbc import DatabaseError
import pyodbc
import os
import logging
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename="web.log")
# username = os.getenv("DB_USERNAME")
# password = os.getenv("DB_PASSWORD")


class SQLConnection:
    def __init__(
        self,
        server="aiddb",
        database="Columbia",
        username=None,
        password=None,
    ):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        """
        Connects to the given DB (default: aiddb:Columbia) and
        initializes all attributes of the SQL object
        """
        conn_str = ""
        try:
            if self.username and self.password:
                conn_str = (
                    f"DRIVER=FreeTDS;"
                    f"SERVER={self.server};"
                    f"PORT=1433;"
                    f"UID={self.username};"
                    f"PWD={self.password};"
                    f"DATABASE={self.database};"
                    f"TDS_Version=8.0;"
                )
            else:
                raise ConnectionError(
                    "Failed to connect to database: No credentials provided."
                )
            self.connection = pyodbc.connect(conn_str)
            logger.info(f"Connected to {self.database} on {self.server}.")
            return True
        except Exception as e:
            logger.exception("Database connection failed.")
            raise ConnectionError("Failed to connect to database.")

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("Disconnected")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # Executes the query and returns the result which is a list of rows
    def query(self, query, params=None) -> List[pyodbc.Row]:
        """
        Executes the query and returns a list of rows from the result.

        :param query: The SQL query that will be executed
        :param params: Extra parameters to pass to pyodbc.cursor.execute()
        """
        if not self.connection:
            logger.exception("Database query failed")
            raise ConnectionError("Not connected to database")

        query = query[5:]  # strip "--sql" prefix for syntax highlighting

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                logger.info("Executing!")
                cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                list_of_rows: List[pyodbc.Row] = cursor.fetchall()
                return list_of_rows
            else:
                # self.connection.commit()
                print("whoa there buddy calm down. none of that yet")
                return []
        except Exception as e:
            logger.exception(f"Error while executing query: {e}")
            raise pyodbc.DatabaseError("Query execution failed") from e


class SQLUtilities(SQLConnection):
    # Returns a list of column names for specified table
    def get_column_names(self, table_name):
        if not self.connection:
            print("Not connected")
            return None
        try:
            query = """
            SELECT
                TABLE_NAME,
                STRING_AGG(COLUMN_NAME, ', ') AS COLUMNS
            FROM information_schema.columns
            WHERE TABLE_NAME = ?
            GROUP BY TABLE_NAME;
            """
            columns = self.query(query, (table_name))
            result = [columns[0][0]] + columns[0][1].split(",")
            return result
        except Exception as e:
            print(f"Error getting column names: {e}")
            return None
