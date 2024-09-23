import os
import google.generativeai as genai

# Configure the API key from environment variables
genai.configure(api_key=os.environ["API_KEY"])

# Create a generative model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate content
response = model.generate_content("Write an email to my boss for resignation.")

# Print the response
print(response.text)
