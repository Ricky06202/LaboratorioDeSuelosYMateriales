import os
import uuid
import logging
from datetime import datetime
from fastapi import UploadFile, HTTPException
from starlette.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_415_UNSUPPORTED_MEDIA_TYPE
from app.core.config import settings

logger = logging.getLogger(__name__)

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_PDF_SIZE = 10 * 1024 * 1024   # 10MB
ALLOWED_MIMES = {'application/pdf', 'image/jpeg', 'image/png', 'image/jpg'}

class FileService:
    def __init__(self):
        self.base_path = settings.STORAGE_PATH
        self._ensure_dirs()

    def _ensure_dirs(self):
        os.makedirs(os.path.join(self.base_path, "equipos"), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "certificados"), exist_ok=True)

    async def save_file(self, file: UploadFile, folder: str) -> str:
        """
        Saves a file to the physical storage using a UUID and returns ONLY the filename.
        """
        # 1. MIME Validation
        if file.content_type not in ALLOWED_MIMES:
            raise HTTPException(
                status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                detail=f"Tipo de archivo no permitido: {file.content_type}. Solo PDF, JPG o PNG."
            )
            
        # 2. Size Validation
        # Read the file to the end to get the size without loading it entirely to RAM if we use SpooledTemporaryFile
        file.file.seek(0, 2) 
        file_size = file.file.tell()
        file.file.seek(0) # Reset pointer
        
        is_pdf = file.content_type == 'application/pdf'
        max_allowed = MAX_PDF_SIZE if is_pdf else MAX_IMAGE_SIZE
        
        if file_size > max_allowed:
            limit_mb = 10 if is_pdf else 5
            raise HTTPException(
                status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE, 
                detail=f"El archivo es demasiado grande. El límite es {limit_mb}MB para este formato."
            )

        extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{extension}"
        
        relative_path = os.path.join(folder, unique_filename)
        full_path = os.path.join(self.base_path, relative_path)
        
        # 3. Secure I/O Handling
        try:
            with open(full_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
        except (OSError, IOError) as e:
            logger.error(f"Error escribiendo al disco: {e}")
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
                detail={"error": "Error interno al acceder al almacenamiento del sistema."}
            )
            
        return unique_filename

file_service = FileService()
