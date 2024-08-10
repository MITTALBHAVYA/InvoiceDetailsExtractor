import fitz  # PyMuPDF
import os

def extract_text_from_selectable_pdf(pdf_path):
    """Extract text from a PDF that contains selectable text using PyMuPDF."""
    all_text = ""

    try:
        # Open the PDF file
        pdf = fitz.open(pdf_path)

        # Loop through each page and extract text
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text = page.get_text()
            if text.strip():
                all_text += text

        # Close the PDF file
        pdf.close()

    except Exception as e:
        print(f"Error reading PDF with PyMuPDF: {e}")

    return all_text.strip()

def process_pdf(file_path):
    """Extract text from a PDF file with selectable text."""
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    text = extract_text_from_selectable_pdf(file_path)
    
    if not text:
        raise ValueError("No text could be extracted from the PDF.")
    
    return text

# Example usage
file_path = r'G:\Swipe\swipeinterntask\convertedfolder\invoice_output.pdf'  # Update with your file path
extracted_text = process_pdf(file_path)
print("Extracted Text:")
print(extracted_text)
