import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
  model="gpt-5.4-mini",
  input="What is powdery mildew on fruit trees",
  store=True,
)

print(response.output_text)
