from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import analyze_pdf
import os
import uuid
from datetime import datetime

router = APIRouter(prefix="/pdf", tags=["PDF Analysis"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze")
async def analyze_uploaded_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_id = str(uuid.uuid4())[:8]
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    try:
        result = analyze_pdf(save_path)
        result["file_name"] = file.filename
        result["file_id"] = file_id
        result["analyzed_at"] = datetime.now().isoformat()
        # Don't send full huge text in API by default if too long
        if len(result.get("full_text", "")) > 5000:
            result["full_text"] = result["full_text"][:5000] + "...(truncated)"
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF analysis failed: {str(e)}")