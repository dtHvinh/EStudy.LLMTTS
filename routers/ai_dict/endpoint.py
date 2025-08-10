import os
from openai import OpenAI
from fastapi import APIRouter, Request, HTTPException, Response
from .types import DictionaryEntry

ai_dict_router = APIRouter()


@ai_dict_router.post("/dict")
def dict_endpoint(request: Request):
    data = request.json()
    term = data.get("term", "")
    if not term:
        raise HTTPException(status_code=400, detail="Missing 'term' in JSON body")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    return Response(content=response.output_parsed)
