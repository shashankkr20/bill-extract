import google.generativeai as genai
import os
from PIL import Image
import json
import asyncio
from typing import Dict, Any, Optional
import base64
from pathlib import Path

class GeminiService:
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.text_model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def extract_text_from_image(self, image_path: Path) -> str:
        """Extract text from image using Gemini Vision"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Prepare prompt for text extraction
            prompt = """
            Extract all text content from this bill/invoice image. 
            Return the text exactly as it appears, maintaining the original formatting and structure.
            Include all numbers, dates, names, addresses, and any other text visible in the image.
            Be thorough and capture all text elements including headers, footers, and fine print.
            """
            
            # Generate response
            response = self.model.generate_content([prompt, image])
            
            if response.text:
                return response.text.strip()
            else:
                raise Exception("No text extracted from image")
                
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    async def parse_bill_data(self, extracted_text: str) -> Dict[str, Any]:
        """Parse extracted text into structured bill data using Gemini"""
        try:
            # Prepare prompt for structured data extraction
            prompt = f"""
            Please analyze the following bill/invoice text and extract structured information in JSON format.
            
            Text to analyze:
            {extracted_text}
            
            Extract the following information and return it as a valid JSON object:
            {{
                "invoice_number": "string or null",
                "invoice_date": "string in YYYY-MM-DD format or null",
                "seller": {{
                    "name": "string or null",
                    "address": "string or null",
                    "gstin": "string or null",
                    "contact_number": "string or null"
                }},
                "buyer": {{
                    "name": "string or null",
                    "address": "string or null",
                    "gstin": "string or null",
                    "contact_number": "string or null"
                }},
                "items": [
                    {{
                        "name": "string",
                        "quantity": "number",
                        "price_per_unit": "number",
                        "tax_rate": "number",
                        "total_amount": "number"
                    }}
                ],
                "summary": {{
                    "subtotal": "number or null",
                    "tax_amount": "number or null",
                    "discount": "number or null",
                    "net_payable_amount": "number or null"
                }}
            }}
            
            Important notes:
            - If a field is not found, use null
            - For numbers, extract only the numeric value (remove currency symbols)
            - For dates, convert to YYYY-MM-DD format if possible
            - For items, create an array of all items found
            - Ensure the response is valid JSON
            """
            
            # Generate response
            response = self.text_model.generate_content(prompt)
            
            if response.text:
                # Try to parse JSON from response
                try:
                    # Find JSON in the response (in case there's extra text)
                    start_idx = response.text.find('{')
                    end_idx = response.text.rfind('}') + 1
                    
                    if start_idx != -1 and end_idx != 0:
                        json_str = response.text[start_idx:end_idx]
                        parsed_data = json.loads(json_str)
                        
                        # Validate and clean the data
                        return self._validate_and_clean_data(parsed_data)
                    else:
                        raise Exception("No valid JSON found in response")
                        
                except json.JSONDecodeError as e:
                    raise Exception(f"Invalid JSON response: {str(e)}")
            else:
                raise Exception("No response from Gemini")
                
        except Exception as e:
            raise Exception(f"Error parsing bill data: {str(e)}")
    
    def _validate_and_clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the parsed data"""
        # Ensure all required fields exist
        required_fields = {
            "invoice_number": None,
            "invoice_date": None,
            "seller": {
                "name": None,
                "address": None,
                "gstin": None,
                "contact_number": None
            },
            "buyer": {
                "name": None,
                "address": None,
                "gstin": None,
                "contact_number": None
            },
            "items": [],
            "summary": {
                "subtotal": None,
                "tax_amount": None,
                "discount": None,
                "net_payable_amount": None
            }
        }
        
        # Merge with existing data
        for key, default_value in required_fields.items():
            if key not in data:
                data[key] = default_value
            elif isinstance(default_value, dict) and isinstance(data[key], dict):
                for sub_key, sub_default in default_value.items():
                    if sub_key not in data[key]:
                        data[key][sub_key] = sub_default
        
        return data 