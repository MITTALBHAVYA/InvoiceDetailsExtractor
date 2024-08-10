import os

def check_file_type(file_path):
    """
    Determine the type of a file based on its extension.

    Parameters:
    - file_path: Path to the file.

    Returns:
    - A string indicating the file type ("PDF", "Image", or "Other").
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")

    # Extract the file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # Define supported file types
    pdf_extensions = ['.pdf']
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']

    if file_extension in pdf_extensions:
        return "PDF"
    elif file_extension in image_extensions:
        return "Image"
    else:
        return "Other"

# Example usage
file_path = 'G:\Swipe\swipeinterntask\Sample invoices\selectableinvoice.pdf'
file_type = check_file_type(file_path)
print(f"The file type is: {file_type}")
