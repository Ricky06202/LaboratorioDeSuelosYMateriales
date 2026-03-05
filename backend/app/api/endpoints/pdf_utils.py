from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
import uuid
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path

from app.api import deps
from app import models

# Configurar Jinja2
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def render_pdf(template_name: str, context: dict) -> bytes:
    try:
        # Inject assets_dir into context for logos
        if "assets_dir" not in context:
            context["assets_dir"] = Path(ASSETS_DIR).as_uri()
        
        template = env.get_template(template_name)
        html_out = template.render(context)
        return HTML(string=html_out, base_url=BASE_DIR).write_pdf()
    except Exception as e:
        logger.error(f"Error rendering PDF {template_name}: {str(e)}")
        raise e

# ... This will be appended or imported, but I will replace the endpoint files with this logic instead of redefining it everywhere.
