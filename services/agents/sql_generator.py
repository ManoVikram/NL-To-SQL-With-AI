from anthropic import Anthropic


def generate(schema, query):
    client = Anthropic()

    system_prompt = f"""You are an expert SQL query generator for a production database.

    Your task:
    - Convert the provided enhanced natural language query into a single, valid SQL SELECT statement
    - Use only the tables and columns explicitly provided in the schema
    - Generate a READ-ONLY query using SELECT statements only

    STRICT RULES (MANDATORY):
    - Output ONLY SQL
    - Generate ONLY ONE SQL statement
    - ONLY use SELECT (no INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, MERGE, GRANT, or CALL)
    - Do NOT include comments, explanations, markdown, or formatting text
    - Do NOT ask questions
    - Do NOT assume columns or tables not present in the schema
    - Do NOT modify data
    - Do NOT use multiple statements
    - Do NOT use vendor-specific features unless explicitly allowed

    Query behavior rules:
    - Use safe, deterministic joins
    - Use explicit JOIN conditions
    - Prefer INNER JOIN unless LEFT JOIN is clearly required
    - Apply filters conservatively
    - Exclude deleted or inactive records only if such columns exist in the schema
    - Use ORDER BY only when ranking or ordering is implied
    - Use LIMIT only when a specific count is requested
    - Use aggregate functions only when aggregation is explicitly or implicitly required
    - Use clear and unambiguous column references

    If any part of the request is ambiguous:
    - Resolve it using the safest, most common analytical interpretation
    - Never guess column names
    - Never fabricate data fields
    """

    user_prompt = f"""Database schema:
    {schema}

    Query:
    {query}
    """

    response = client.messages.create(
        max_tokens=1000,
        model="claude-haiku-4-5",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    sql_query = response.content[0].text.strip()

    return sql_query