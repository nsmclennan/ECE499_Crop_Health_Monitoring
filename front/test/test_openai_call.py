import os
import base64
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

# Setup paths for universal running
script_dir = Path(__file__).resolve().parent
prompt_path = script_dir / ".." / "prod" / "config" / "openai_prompt.txt"
image_path = script_dir / "images" / "sample_powdery_mildew.jpg"

# Setup OpenAI API
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Setup image and prompt

with open(prompt_path, "r", encoding="utf-8") as f:
    mildew_prompt = f.read()

with open(image_path, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")



# Call
response = client.responses.create(
    model="gpt-5.4-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": mildew_prompt},
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{image_b64}"
                }
            ]
        }],
    store=True,
)

print(response.output_text)