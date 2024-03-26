from dotenv import load_dotenv
from fastapi import FastAPI, File , UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from fastapi import File, UploadFile, Form
from query import embed, query
import filecmp

# Load environment variables from .env file (if any)
load_dotenv()

class Response(BaseModel):
    result: str | None

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
    "https://proud-mushroom-0a39b0a10.5.azurestaticapps.net/"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
import shutil
@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.post("/predict", response_model=Response)
async def predict(file: UploadFile = File(...), question: str = Form(...)) -> Any:
    save_directory = "SOURCE_DOCUMENTS"
    os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist
    
    # Full path for the uploaded file
    file_location = f"{save_directory}/{file.filename}"
    
    # Save the uploaded file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Ensure the file pointer is reset to the start
    file.file.seek(0)
    
    # Call the query function with the user's question
    response = query(question)
        
    # Check if the new file is different from what is present in source_documents
    if not are_files_identical(file_location, save_directory):
        # Delete all files in source_documents except the newly uploaded one
        for filename in os.listdir(save_directory):
            if filename != file.filename:
                file_path = os.path.join(save_directory, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting file: {e}")
                # Delete qdrant_img_db_2 if it exists
        qdrant_db_img_2_path = os.path.join(save_directory, "qdrant_img_db_2")
        if os.path.exists(qdrant_db_img_2_path):
            try:
                os.remove(qdrant_db_img_2_path)
            except Exception as e:
                print(f"Error deleting qdrant_img_db_2: {e}")


    return {"result": response}

def are_files_identical(new_file_location, directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename != os.path.basename(new_file_location) and filecmp.cmp(new_file_location, file_path):
            return True
    return False
