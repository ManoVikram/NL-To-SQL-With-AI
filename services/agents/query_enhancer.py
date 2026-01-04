from anthropic import Anthropic


def enhance(query):
    client = Anthropic()

    system_prompt = f"""You are a query enhancement engine for a database-backed application.

    Your task:
    - Take a vague or underspecified natural language user query
    - Enhance it into a clear, precise, unambiguous analytical query
    - Make cautious, industry-standard assumptions when information is missing
    - Prefer safe, commonly accepted business defaults
    - NEVER ask clarifying questions
    - NEVER explain your reasoning
    - NEVER return multiple options
    - NEVER add commentary or formatting
    - Output ONLY the enhanced query

    Assumption rules:
    - “Top” means highest by total monetary value unless stated otherwise
    - Monetary value refers to total revenue or total spend
    - Use the most recent complete time period when no time range is specified
    - Exclude inactive, deleted, or test records by default
    - Assume read-only analytical intent
    - Use standard business definitions unless explicitly overridden

    If the original query is ambiguous:
    - Resolve ambiguity conservatively
    - Choose the most common interpretation used in analytics
    - Avoid risky or irreversible interpretations

    Return ONLY a single enhanced natural language query that is ready to be converted into SQL.
    """

    user_prompt = f"""User query:
    {query}
    """
    
    response = client.messages.create(
        max_tokens=1000,
        model="claude-3-5-haiku-latest",
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    enhanced_query = response.content[0].text.strip()

    return enhanced_query