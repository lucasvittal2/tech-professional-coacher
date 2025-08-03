from langsmith import traceable
from openai import OpenAI

@traceable
def call_openai(prompt: str) -> str:
    result = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return result.choices[0].message.content

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    # Example usage
    response = call_openai("Hello, how are you?")
    print(response)
