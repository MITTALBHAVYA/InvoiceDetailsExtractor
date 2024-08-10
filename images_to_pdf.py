from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def image_to_pdf(image_paths, output_pdf_path):
    """
    Convert a list of image files to a single PDF file.

    Parameters:
    - image_paths: List of paths to the image files.
    - output_pdf_path: Path to the output PDF file.
    """
    # Ensure the output path ends with ".pdf"
    if not output_pdf_path.endswith('.pdf'):
        output_pdf_path += '.pdf'

    # Initialize the canvas for PDF
    pdf_canvas = canvas.Canvas(output_pdf_path, pagesize=letter)

    for image_path in image_paths:
        # Open the image
        image = Image.open(image_path)

        # Get image size
        img_width, img_height = image.size

        # Resize image to fit within letter-sized page while maintaining aspect ratio
        max_width, max_height = letter
        scale = min(max_width / img_width, max_height / img_height)
        img_width = int(img_width * scale)
        img_height = int(img_height * scale)

        # Center image on the page
        x_pos = (max_width - img_width) / 2
        y_pos = (max_height - img_height) / 2

        # Add the image to the PDF canvas
        pdf_canvas.drawImage(image_path, x_pos, y_pos, img_width, img_height)

        # Add a new page if there are more images
        pdf_canvas.showPage()

    # Save the PDF
    pdf_canvas.save()

# Example usage
image_paths = [r'G:\Swipe\swipeinterntask\Sample invoices\invoice2.png']  # Add more paths as needed
output_pdf_path = r'G:\Swipe\swipeinterntask\convertedfolder\invoice_output.pdf'
image_to_pdf(image_paths, output_pdf_path)
print(f"PDF created at: {output_pdf_path}")
