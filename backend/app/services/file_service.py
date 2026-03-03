import os
import uuid
from datetime import datetime
from fastapi import UploadFile
from app.core.config import settings

class FileService:
    def __init__(self):
        self.base_path = settings.STORAGE_PATH
        self._ensure_dirs()

    def _ensure_dirs(self):
        os.makedirs(os.path.join(self.base_path, "equipos"), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "certificados"), exist_ok=True)

    async def save_file(self, file: UploadFile, folder: str) -> str:
        """
        Saves a file to the physical storage and returns the relative path.
        """
        extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}{extension}"
        
        relative_path = os.path.join(folder, unique_filename)
        full_path = os.path.join(self.base_path, relative_path)
        
        with open(full_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        return relative_path

file_service = FileService()
