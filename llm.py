import requests
import os

api_key = os.getenv("GEMINI_API_KEY")

with open("crap.py", "r") as f:
    code = f.read()

prompt = f"""You are a code reviewer. Review the following Python code and point out:
- Security issues
- Bugs
- Bad practices

Code:
{code}
"""

response = requests.post(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}",
    headers={"Content-Type": "application/json"},
    json={
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
)

data = response.json()
print(data["candidates"][0]["content"]["parts"][0]["text"])
