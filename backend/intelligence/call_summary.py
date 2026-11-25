from backend.agents.llm import generate_response


def generate_call_summary(messages):

    prompt = f"""
    Analyze this sales conversation:

    {messages}

    Generate a summary containing:
    1. Customer requirements
    2. Product interest
    3. Customer objections
    4. Purchase intention
    5. Next recommended action

    Keep the summary concise.
    """

    response = generate_response([
        {
            "role": "user",
            "content": prompt
        }
    ])

    return response