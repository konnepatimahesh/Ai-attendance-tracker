from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
import os
import csv

app = FastAPI()

# Mount the static directory for serving CSS, JS, and other files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates setup for rendering HTML
templates = Jinja2Templates(directory="app/templates")

# Ensure the uploads directory exists
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Route to serve the main page
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to handle file upload and process it
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Save the file to the uploads directory
        file_location = os.path.join(UPLOADS_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        print(f"[INFO] File received and saved: {file.filename}")

        # Call the face recognition function
        name, match_percentage = recognize_face(file_location)

        if name:
            print(f"[INFO] Recognized: {name} ({match_percentage}%)")
            mark_attendance(name)
            return JSONResponse(content={
                "status": "success",
                "name": name,
                "match_percentage": match_percentage,
                "message": f"Attendance marked for {name}"
            })
        else:
            print("[WARNING] Face not recognized.")
            return JSONResponse(content={
                "status": "error",
                "message": "No face detected or face not recognized"
            }, status_code=400)

    except Exception as e:
        print(f"[ERROR] {e}")
        return JSONResponse(content={
            "status": "error",
            "message": str(e)
        }, status_code=500)

# Dummy face recognition function (replace with real model later)
def recognize_face(image_path: str):
    print(f"[DEBUG] Processing image: {image_path}")
    return "Mahesh k", 98  # Example

# Attendance marker (writes to CSV)
def mark_attendance(name: str):
    print(f"[ATTENDANCE] Marked present for: {name}")
    with open("Attendance.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, "Present"])
