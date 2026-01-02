import psycopg2
from database.config import DB_CONFIG
from agents import query_enhancer, sql_generator
from database import schema_loader
from lib.utils import sql_validator, sql_executor


class QueryPipeline:
    def __init__(self):
        self.db_connection = psycopg2.connect(**DB_CONFIG)

    def execute(self, user_query):
        # Step 1 - Enhance the user query
        enhanced_query = query_enhancer.enhance(query=user_query)

        # Step 2 - Load the database schema
        schema = schema_loader.load(connection=self.db_connection)

        # Step 3 - Generate the SQL query
        sql_query = sql_generator.generate(schema=schema, query=enhanced_query)

        # Step 4 - Validate the SQL query
        validation_result = sql_validator.validate(sql_query=sql_query)

        if not validation_result["is_valid"]:
            return {
                "is_success": False,
                "sql_query": sql_query,
                "results": None,
                "error": validation_result["error"]
            }
        
        # Step 5 - Execute the SQL query
        execution_result = sql_executor.execute(connection=self.db_connection, sql_query=sql_query)

        return {
            "is_success": True,
            "sql_query": sql_query,
            "results": execution_result,
            "error": None
        }