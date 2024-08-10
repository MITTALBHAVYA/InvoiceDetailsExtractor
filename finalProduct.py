import streamlit as st
import os
import io
from PIL import Image
import fitz  # PyMuPDF
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai
from paddleocr import PaddleOCR
import logging
import json

# Load environment variables and configure generative AI
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
logging.getLogger('ppocr').setLevel(logging.WARNING)

# Function definitions
def extract_invoice_details(content, from_image=False):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        
        if from_image:
            content = genai.upload_file(path=content, display_name="Invoice Image")
        
        prompt = (
            "Extract the following details from this invoice text and provide the output in JSON format, just give braces and its data, nothing else:\n"
            "1. Customer details:\n"
            "   - Name\n"
            "   - Address\n"
            "   - Contact (multiple entries allowed, use an array of strings)\n"
            "2. Products:\n"
            "   - Name\n"
            "   - Quantity\n"
            "   - Price\n"
            "3. Total Amount\n"
            "The JSON response should be structured as follows:\n"
            "{\n"
            "  \"Customer Details\": {\n"
            "    \"Name\": \"\",\n"
            "    \"Address\": \"\",\n"
            "    \"Contact\": [\n"
            "      \"\"\n"
            "    ]\n"
            "  },\n"
            "  \"Products\": [\n"
            "    {\n"
            "      \"Name\": \"\",\n"
            "      \"Quantity\": \"\",\n"
            "      \"Price\": \"\"\n"
            "    }\n"
            "  ],\n"
            "  \"Total Amount\": \"\"\n"
            "}\n"
            "Provide the output in this exact JSON structure. Do not include any additional text or formatting."
        )
        
        response = model.generate_content([content, prompt])
        return response.text
    
    except Exception as e:
        st.error(f"An error occurred while extracting details: {e}")
        return None

def extract_text_from_image(image):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(np.array(image), cls=True)
    return "\n".join([line[1][0] for line in result[0]])

def extract_text_from_pdf(pdf_path):
    all_text = ""
    try:
        pdf_document = fitz.open(pdf_path)
        for page in pdf_document:
            text = page.get_text() or extract_text_from_image(Image.open(io.BytesIO(page.get_pixmap().tobytes())))
            all_text += text + "\n"
        pdf_document.close()
    except Exception as e:
        st.error(f"An error occurred while extracting text from PDF: {e}")
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
        st.error("Unsupported file type detected.")
        return None

    return response

# Streamlit app
st.set_page_config(page_title="Invoice Extraction App", page_icon=":memo:", layout="wide")

# Centered title and styled welcome message
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        color: #007BFF;
        text-align: center;
        margin-bottom: 10px;
    }
    .description {
        font-size: 20px;
        text-align: center;
        color: #555555;
    }
    </style>
    <div class="title">Invoice Extraction Application</div>
    <div class="description">
        Welcome to the Invoice Extraction App! Upload your invoice file and choose the method of extraction. 
        The app supports both PDF and image files.
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an invoice file", type=['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'])

if uploaded_file:
    st.success("File uploaded successfully.")
    option = st.selectbox(
        "Choose extraction method",
        ["Direct Extraction (Image-based)", "Text Extraction (Text-based)"]
    )

    flag = 0 if option == "Direct Extraction (Image-based)" else 1

    if st.button("Process"):
        with st.spinner("Processing..."):
            try:
                if uploaded_file.type == 'application/pdf':
                    pdf_path = os.path.join("/tmp", uploaded_file.name)
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_file.read())
                    response = process_file(pdf_path, flag)
                else:
                    image = Image.open(uploaded_file)
                    image_path = os.path.join("/tmp", uploaded_file.name)
                    image.save(image_path)
                    response = process_file(image_path, flag)

                if response:
                    try:
                        # Attempt to parse the response as JSON
                        json_response = json.loads(response)
                        st.subheader("Extracted Details:")
                        
                        # Display Customer Details
                        if "Customer Details" in json_response:
                            st.markdown("**Customer Details:**", unsafe_allow_html=True)
                            for key, value in json_response["Customer Details"].items():
                                st.markdown(f"**{key}:** {value}", unsafe_allow_html=True)

                        # Display Products
                        if "Products" in json_response:
                            st.markdown("**Products:**", unsafe_allow_html=True)
                            for product in json_response["Products"]:
                                st.markdown(f"**Name:** {product['Name']}", unsafe_allow_html=True)
                                st.markdown(f"**Quantity:** {product['Quantity']}", unsafe_allow_html=True)
                                st.markdown(f"**Price:** {product['Price']}", unsafe_allow_html=True)
                                st.markdown("---", unsafe_allow_html=True)

                        # Display Total Amount
                        if "Total Amount" in json_response:
                            st.markdown(f"**Total Amount:** {json_response['Total Amount']}", unsafe_allow_html=True)

                    except json.JSONDecodeError as e:
                        st.error(f"Error parsing JSON response: {e}")
                else:
                    st.warning("No response generated.")
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
