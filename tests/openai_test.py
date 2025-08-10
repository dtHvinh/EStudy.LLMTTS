import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from dotenv import load_dotenv
from routers.ai_dict.types import DictionaryEntry

load_dotenv(".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

term = "accommodation"

response = client.responses.parse(
    model="gpt-4o-mini",
    input=[
        {"role": "system", "content": "You are a dictionary."},
        {
            "role": "user",
            "content": "Provide the definition and usage of the term: " + term,
        },
    ],
    text_format=DictionaryEntry,
)

print(response.output_parsed)
