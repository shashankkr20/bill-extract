from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import os
import json
import asyncio
from datetime import datetime
import aiofiles
from pathlib import Path

from backend.database import init_db
from backend.database import get_db
from backend.models import BillExtraction
from backend.gemini_service import GeminiService
from backend.export_service import ExportService
from backend.image_processor import ImageProcessor

app = FastAPI(title="Bill Information Extraction System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize services
gemini_service = GeminiService()
export_service = ExportService()
image_processor = ImageProcessor()

# Create uploads directory
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process bill image"""
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, and PDF files are allowed.")
        
        # Validate file size (10MB limit)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size too large. Maximum size is 10MB.")
        
        # Save file
        file_path = UPLOADS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Process image and extract information
        extracted_data = await process_bill_image(file_path)
        
        # Save to database
        db = next(get_db())
        bill_extraction = BillExtraction(
            filename=file.filename,
            file_path=str(file_path),
            extracted_data=extracted_data,
            processed_at=datetime.now()
        )
        db.add(bill_extraction)
        db.commit()
        db.refresh(bill_extraction)
        
        return {
            "success": True,
            "message": "Bill processed successfully",
            "data": extracted_data,
            "id": bill_extraction.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

async def process_bill_image(file_path: Path):
    """Process bill image using Gemini and return extracted data"""
    try:
        # Enhance image if needed
        enhanced_image_path = await image_processor.enhance_image(file_path)
        
        # Extract text using Gemini
        extracted_text = await gemini_service.extract_text_from_image(enhanced_image_path)
        
        # Parse structured data using Gemini
        structured_data = await gemini_service.parse_bill_data(extracted_text)
        
        return structured_data
        
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

@app.get("/extractions")
async def get_extractions():
    """Get all bill extractions"""
    db = next(get_db())
    extractions = db.query(BillExtraction).order_by(BillExtraction.processed_at.desc()).all()
    return extractions

@app.get("/extractions/{extraction_id}")
async def get_extraction(extraction_id: int):
    """Get specific bill extraction"""
    db = next(get_db())
    extraction = db.query(BillExtraction).filter(BillExtraction.id == extraction_id).first()
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    return extraction

@app.post("/export/{extraction_id}")
async def export_extraction(extraction_id: int, format: str):
    """Export extraction in specified format (pdf, csv, excel)"""
    db = next(get_db())
    extraction = db.query(BillExtraction).filter(BillExtraction.id == extraction_id).first()
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    
    try:
        if format.lower() == "pdf":
            file_path = await export_service.export_to_pdf(extraction)
        elif format.lower() == "csv":
            file_path = await export_service.export_to_csv(extraction)
        elif format.lower() == "excel":
            file_path = await export_service.export_to_excel(extraction)
        else:
            raise HTTPException(status_code=400, detail="Invalid format. Use pdf, csv, or excel")
        
        return FileResponse(file_path, filename=f"bill_extraction_{extraction_id}.{format}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting file: {str(e)}")

@app.delete("/extractions/{extraction_id}")
async def delete_extraction(extraction_id: int):
    """Delete bill extraction"""
    db = next(get_db())
    extraction = db.query(BillExtraction).filter(BillExtraction.id == extraction_id).first()
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    
    # Delete file
    if os.path.exists(extraction.file_path):
        os.remove(extraction.file_path)
    
    # Delete from database
    db.delete(extraction)
    db.commit()
    
    return {"message": "Extraction deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 