from google import genai

API_KEY = "YOUR_AQ_KEY"

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence.",
)

print(response.text)