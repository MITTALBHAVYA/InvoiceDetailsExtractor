from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key (Ensure it's valid and has text generation permission)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def extract_invoice_details(invoice_text):
    """
    Extract customer details, products, and total amount from an unstructured invoice text.

    Parameters:
    - invoice_text: The unstructured text data of an invoice.

    Returns:
    - A structured response with customer details, products, and total amount.
    """
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        
        # Construct a prompt to extract customer details, products, and total amount
        prompt = (
            "Extract the following details from this invoice text:\n"
            "1. Customer details (Name, Address, Contact).\n"
            "2. Products (Name, Quantity, Price).\n"
            "3. Total Amount.\n"
            "Provide the details in a structured format."
        )
        
        response = model.generate_content([invoice_text, prompt])
        
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
invoice_text = """
TAX INVOICE
Involce #: Inv41
US
TATAMOTORS LIMITED
GSTIN 27AAACT2727Q1ZW
Ferllzers LIc.No LASD34564756
Seeds LIc.No LASD67808360
Insectlclde LIc.No LAID26453734
TATA MOTORS LIMITED Nigadi Bhosari Road, PIMPRI
Pune, MAHARASHTRA, 411018
Blll To:
Involce Date:
18Jul2024
TEST
Place of Supply:
36-TELANGANA
Test
Enqulre ld
06-06-2024
Hyderabad, TELANGANA, 500089
Shlp To:
Test
Ph:9108239284
Hyderabad,TELANGANA,500089
test@gmail.com
IMEINO Item
Rate
Quantity
Total Amount
1
WASTE AND SCRAP OFSTAINLESS STEEL
95.00
6,790KGS
6,45,050.00
HSN: 72042190
Bank Detalls
Pay using UPI
Taxable Amount
6,45,050.00
Bank:
IDBI
IGST 18.0%
1,16,109.00
Account #
1234567890
IFSC Code:
Round Off
0.41
IBKL0000432
TCS@1%206C
7,611.59
Branch:
GACHIBOWLI
BENEFICIARY NAME: ROMOLIKA SAHANI
Total
7,68,771.00
Total amount (in words): INR Seven Lakh, Sixty-Eight Thousand, Seven Hundred And
Seventy-One Rupees Only.
Amount Payable:
7,68,771.00
For TATA MOTORS LIMITED
Notes:
Thankyou for shopping from us. See you again.
Terms and Conditions:e
Authorized Signatory
SPECIFIC TERMS&CONDITIONS
GOODS ONCE SOLD CANNOT BE RETURNED. ONLY GOODS THAT ARE DAMAGED CAN BE RETURNED UNDER
Receiver's Signature
"""

response = extract_invoice_details(invoice_text)

if response:
    print("Extracted Details:")
    print(response)
else:
    print("No response generated.")
