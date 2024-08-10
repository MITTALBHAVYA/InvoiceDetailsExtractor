import fitz  # PyMuPDF
from PIL import Image
import io

def pdf_to_images(pdf_path, output_folder):
    """
    Convert each page of a PDF into an image and save to the output folder.

    Parameters:
    - pdf_path: Path to the PDF file.
    - output_folder: Folder to save the resulting images.
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        # Select the page
        page = pdf_document.load_page(page_num)

        # Render the page to a pixel-based image
        pix = page.get_pixmap()

        # Convert to PIL Image
        img = Image.open(io.BytesIO(pix.tobytes()))

        # Save image to file
        image_path = f"{output_folder}/page_{page_num + 1}.png"
        img.save(image_path)
        print(f"Saved page {page_num + 1} as {image_path}")

    pdf_document.close()

# Example usage
pdf_path = r'G:\Swipe\swipeinterntask\Sample invoices\invoice1.pdf'
output_folder = r'G:\Swipe\swipeinterntask\convertedfolder'
pdf_to_images(pdf_path, output_folder)
