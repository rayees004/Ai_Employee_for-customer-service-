from google import genai
from decouple import config

client = genai.Client(api_key=config("GEMINI_API_KEY"))
response = client.models.generate_content(
    model=config("GEMINI_MODEL"),
    contents={'text': 'list 5 animals'}
)

print(response.text)


