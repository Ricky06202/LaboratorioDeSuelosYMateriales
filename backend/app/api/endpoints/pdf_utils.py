from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
import uuid
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from app.api import deps
from app import models

# Configurar Jinja2
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def render_pdf(template_name: str, context: dict) -> bytes:
    template = env.get_template(template_name)
    html_out = template.render(context)
    return HTML(string=html_out).write_pdf()

# ... This will be appended or imported, but I will replace the endpoint files with this logic instead of redefining it everywhere.
