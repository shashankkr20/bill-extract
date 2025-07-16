# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### 3. Set Up Environment
```bash
# Copy the example file
cp env.example .env

# Edit .env and add your API key
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Test Your Setup
```bash
python test_setup.py
```

### 5. Start the Application
```bash
python run.py
```

### 6. Open in Browser
Navigate to: `http://localhost:8000`

## 🎯 What You Can Do

1. **Upload Bill Images**: Drag & drop JPG, PNG, or PDF files
2. **Extract Information**: AI automatically extracts structured data
3. **View Results**: See organized invoice, seller, buyer, and item details
4. **Export Data**: Download as PDF, Excel, or CSV
5. **Manage History**: View and manage previous extractions

## 📋 Supported Bill Information

- ✅ Invoice number and date
- ✅ Seller details (name, address, GSTIN, contact)
- ✅ Buyer details (name, address, GSTIN, contact)
- ✅ Item details (name, quantity, price, tax, total)
- ✅ Summary (subtotal, tax, discount, net amount)

## 🔧 Troubleshooting

### Common Issues:
- **"API key not found"**: Set GEMINI_API_KEY in .env file
- **"Import errors"**: Run `pip install -r requirements.txt`
- **"Port in use"**: Change port in .env file or kill existing process

### Need Help?
- Check the full README.md for detailed documentation
- Run `python test_setup.py` to diagnose issues
- Review API documentation at `http://localhost:8000/docs`

## 🎉 You're Ready!

Your Bill Information Extraction System is now running! Upload a bill image and see the magic happen. 