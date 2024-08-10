import os
import io
import logging
from paddleocr import PaddleOCR
from PIL import Image
import fitz  # PyMuPDF
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables and configure generative AI
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
logging.getLogger('ppocr').setLevel(logging.WARNING)

def extract_invoice_details(content, from_image=False):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        
        # If content is an image path, upload the file
        if from_image:
            content = genai.upload_file(path=content, display_name="Invoice Image")
        
        # Construct the prompt for extracting invoice details
        prompt = (
            "Extract the following details from this invoice text:\n"
            "1. Customer details (Name, Address, Contact).\n"
            "2. Products (Name, Quantity, Price).\n"
            "3. Total Amount.\n"
            "Provide the details in a structured format."
        )
        
        # Generate and return the response
        response = model.generate_content([content, prompt])
        return response.text
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_text_from_image(image):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(np.array(image), cls=True)
    return "\n".join([line[1][0] for line in result[0]])

def extract_text_from_pdf(pdf_path):
    all_text = ""
    pdf_document = fitz.open(pdf_path)
    for page in pdf_document:
        text = page.get_text() or extract_text_from_image(Image.open(io.BytesIO(page.get_pixmap().tobytes())))
        all_text += text + "\n"
    pdf_document.close()
    return all_text.strip()

def check_file_type(file_path):
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return "PDF"
    elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
        return "Image"
    return "Other"

def process_file(file_path, flag):
    file_type = check_file_type(file_path)
    extracted_text, response = None, None
    
    if file_type == "PDF":
        extracted_text = extract_text_from_pdf(file_path)
        response = extract_invoice_details(extracted_text) if extracted_text else None
    elif file_type == "Image":
        if flag == 1:
            extracted_text = extract_text_from_image(Image.open(file_path))
            response = extract_invoice_details(extracted_text) if extracted_text else None
        else:
            response = extract_invoice_details(file_path, from_image=True)
    else:
        print("Unsupported file type detected.")
        return

    if response:
        print("Extracted Details:\n", response)
    else:
        print("No response generated.")

# Example usage
file_path = r'G:\Swipe\swipeinterntask\Sample invoices\invoice2.png'
process_file(file_path, flag=1)
