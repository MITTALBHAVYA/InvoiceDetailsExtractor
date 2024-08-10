from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

def extract_text_from_image(image_path):
    """
    Extract text from an image file using PaddleOCR.

    Parameters:
    - image_path: Path to the image file.

    Returns:
    - Extracted text from the image.
    """
    # Initialize PaddleOCR model
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # You can specify language here

    # Perform OCR
    result = ocr.ocr(image_path, cls=True)
    
    # Extract and concatenate text
    text = []
    for line in result[0]:
        text.append(line[1][0])
    
    return "\n".join(text)

# Example usage
image_path = r'G:\Swipe\swipeinterntask\Sample invoices\invoice2.png'  # Update with your image path
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:")
print(extracted_text)
