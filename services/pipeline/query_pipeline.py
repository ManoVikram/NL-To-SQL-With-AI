import logging
import psycopg
from psycopg_pool import ConnectionPool
from database.config import DB_CONFIG
from agents import query_enhancer, sql_generator
from database import schema_loader
from lib.utils import sql_validator, sql_executor

logger = logging.getLogger(__name__)


class QueryPipeline:
    def __init__(self):
        self.pool = ConnectionPool(
            conninfo=f"host={DB_CONFIG['host']} "
                        f"port={DB_CONFIG['port']} "
                        f"dbname={DB_CONFIG['dbname']} "
                        f"user={DB_CONFIG['user']} "
                        f"password={DB_CONFIG['password']} "
                        f"sslmode=require "
                        f"channel_binding=require",
            min_size=1,
            max_size=10,
            timeout=30
        )

    def execute(self, user_query):
        try:
            # Step 1 - Enhance the user query
            logging.info(f"Enhancing query: {user_query}")
            enhanced_query = query_enhancer.enhance(query=user_query)

            # Step 2 - Load the database schema
            logging.info("Loading database schema")
            with self.pool.connection() as db_connection:
                schema = schema_loader.load(connection=db_connection)

            # Step 3 - Generate the SQL query
            logging.info(f"Generating SQL for enhanced query: {enhanced_query}")
            sql_query = sql_generator.generate(schema=schema, query=enhanced_query)

            # Step 4 - Validate the SQL query
            logging.info(f"Validating SQL query: {sql_query}")
            validation_result = sql_validator.validate(sql_query=sql_query)

            if not validation_result["is_valid"]:
                return {
                    "is_success": False,
                    "sql_query": sql_query,
                    "results": None,
                    "error": validation_result["error"]
                }
            
            # Step 5 - Execute the SQL query
            logging.info(f"Executing SQL query: {sql_query}")
            with self.pool.connection() as db_connection:
                execution_result = sql_executor.execute(connection=db_connection, sql_query=sql_query)

            logging.info(f"Successfully executed the query. Returned {len(execution_result["rows"])} rows.")

            return {
                "is_success": True,
                "sql_query": sql_query,
                "results": execution_result,
                "error": None
            }
        except Exception as error:
            logger.error(f"Pipeline error: {error}", exc_info=True)
            return {
                "is_success": False,
                "sql_query": None,
                "results": None,
                "error": str(error)
            }