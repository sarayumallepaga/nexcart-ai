from app.ai.groq_client import client


def compare_with_ai(product1, product2):
    prompt = f"""
You are an expert shopping assistant.

Compare these two products.

Product 1:
{product1}

Product 2:
{product2}

Explain:

1. Which is better overall?
2. Which offers better value?
3. Who should buy Product 1?
4. Who should buy Product 2?

Keep it under 200 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content