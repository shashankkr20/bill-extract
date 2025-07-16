# Bill Information Extraction System

A comprehensive full-stack application that extracts structured information from bill images using Google's Gemini AI technology. Built with FastAPI backend and a modern, responsive frontend.

## 🌐 Live Demo

**Try it out:** [https://bill-extract-d5yl.onrender.com/](https://bill-extract-d5yl.onrender.com/)

> **Note:** This is a free instance hosted on Render, so response times may be slower than expected. The application may take a few seconds to wake up from sleep mode on the first request.

## 🚀 Features

### Core Functionality
- **Multi-format Support**: Accepts JPG, PNG, and PDF files
- **AI-Powered Extraction**: Uses Google Gemini Vision API for accurate text extraction
- **Structured Data Parsing**: Extracts and organizes bill information into structured format
- **Image Enhancement**: Automatic preprocessing for better extraction accuracy
- **Real-time Processing**: Fast and efficient bill processing

### Extracted Information
- **Invoice Details**: Invoice number and date
- **Seller Information**: Name, address, GSTIN, contact number
- **Buyer Information**: Name, address, GSTIN, contact number
- **Item Details**: Name, quantity, price per unit, tax rate, total amount
- **Summary Information**: Subtotal, tax amount, discount, net payable amount

### Export Options
- **PDF Export**: Professional PDF reports with formatted tables
- **Excel Export**: Multi-sheet Excel files with organized data
- **CSV Export**: Simple CSV format for data analysis

### User Interface
- **Modern Design**: Beautiful, responsive UI with gradient backgrounds
- **Drag & Drop**: Easy file upload with drag and drop support
- **Real-time Feedback**: Progress indicators and status messages
- **History Management**: View and manage previous extractions
- **Mobile Responsive**: Works seamlessly on all devices

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Google Gemini AI**: Advanced AI for text extraction and data parsing
- **SQLAlchemy**: Database ORM for data persistence
- **SQLite**: Lightweight database for storing extractions
- **Pillow/OpenCV**: Image processing and enhancement
- **ReportLab**: PDF generation
- **Pandas/OpenPyXL**: Excel and CSV export functionality

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: No framework dependencies
- **Inter Font**: Modern typography

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Modern web browser

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd bill-extract
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy the example environment file
cp env.example .env

# Edit .env file and add your Gemini API key
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 5. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 🏃‍♂️ Running the Application

### Start the Server
```bash
python main.py
```

The application will be available at `http://localhost:8000`

### Alternative: Using Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 Usage

### 1. Upload Bill Image
- Navigate to the application in your browser
- Drag and drop a bill image or click to browse files
- Supported formats: JPG, PNG, PDF (max 10MB)

### 2. Process and Extract
- The system will automatically process your image
- AI will extract and structure the bill information
- Results are displayed in an organized format

### 3. Export Results
- Click the export buttons (PDF, Excel, CSV) to download results
- Files are automatically generated with timestamps

### 4. Manage History
- View all previous extractions in the history section
- Click on any extraction to view details
- Delete extractions as needed

## 🏗️ Project Structure

```
bill-extract/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── README.md              # Project documentation
├── backend/               # Backend modules
│   ├── __init__.py
│   ├── database.py        # Database configuration
│   ├── models.py          # Database models
│   ├── gemini_service.py  # Gemini AI integration
│   ├── image_processor.py # Image enhancement
│   └── export_service.py  # Export functionality
├── templates/             # HTML templates
│   └── index.html         # Main application interface
├── static/                # Static files
├── uploads/               # Uploaded files (created automatically)
├── exports/               # Exported files (created automatically)
└── bill_extractions.db    # SQLite database (created automatically)
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `DATABASE_URL`: Database connection string (default: SQLite)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### File Size Limits
- Maximum file size: 10MB
- Supported formats: JPG, PNG, PDF

## 🐛 Troubleshooting

### Common Issues

1. **Gemini API Key Error**
   - Ensure your API key is correctly set in the `.env` file
   - Verify the API key is valid and has proper permissions

2. **Image Processing Errors**
   - Check if the image format is supported
   - Ensure the image is not corrupted
   - Try with a different image

3. **Database Errors**
   - Delete the `bill_extractions.db` file to reset the database
   - Ensure write permissions in the project directory

4. **Port Already in Use**
   - Change the port in the `.env` file
   - Or kill the process using the current port

### Error Messages
- **"Invalid file type"**: Only JPG, PNG, and PDF files are supported
- **"File size too large"**: Maximum file size is 10MB
- **"No text extracted"**: The image may be unclear or contain no text

## 🔒 Security Considerations

- API keys are stored in environment variables
- File uploads are validated for type and size
- No sensitive data is logged
- Database is local and not exposed

## 🚀 Deployment

### Local Development
The application is ready to run locally with the provided setup.

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn)
- Setting up a reverse proxy (Nginx)
- Using a production database (PostgreSQL)
- Implementing proper logging
- Setting up SSL/TLS certificates

## 📝 API Documentation

The FastAPI application automatically generates API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review the API documentation
- Open an issue on the repository

## 🔄 Updates

Stay updated with the latest features and improvements by:
- Following the repository
- Checking the changelog
- Reviewing release notes

---

**Note**: This application requires a valid Google Gemini API key to function. Make sure to obtain one from the Google AI Studio before running the application. #
