import re


def validate(sql_query, allowed_tables=None):
    sql = sql_query.lower()
    
    allowed_tables = [table.lower() for table in allowed_tables]

    dangerous_keywords = ['drop', 'delete', 'update', 'insert', 'alter', 'truncate', 'exec', 'execute', 'create', 'grant', 'revoke']

    # Check whether the query starts with SELECT
    if not sql.startswith("select"):
        return {
            "is_valid": False,
            "error": "Only SELECT queries are allowed."
        }
    
    # Check for any dangerous keywords in the query
    for keyword in dangerous_keywords:
        keyword_pattern = rf"\b{keyword}\b"
        if re.search(keyword_pattern, sql):
            return {
                "is_valid": False,
                "error": f"Dangerous operation '{keyword}' not allowed."
            }
        
    # Check for no multiple queries / statements
    semicolon_count = sql.count(";")
    if semicolon_count > 1 or (semicolon_count == 1 and not sql.endswith(";")):
        return {
            "is_valid": False,
            "error": "Multiple SQL statements are not allowed."
        }
    
    return {
        "is_valid": True,
        "error": None
    }