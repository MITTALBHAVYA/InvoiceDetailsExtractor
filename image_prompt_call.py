from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key (Ensure it's valid and has text generation permission)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_text_from_image(image_path, prompt):
  try:
    sample_file = genai.upload_file(path=image_path, display_name="Image")
    print(f"Uploaded file as: {sample_file.uri}")
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([sample_file, prompt])
    return response.text
  
  except Exception as e:
    print(f"An error occurred: {e}")
    return None
  
image_path = "G:\Swipe\swipeinterntask\Sample invoices\invoice3.pdf"
prompt = "Provide details about Customer details, Products and Total"
response = generate_text_from_image(image_path, prompt)

if response:
  print("Response:")
  print(response)
else:
  print("No response generated.")
