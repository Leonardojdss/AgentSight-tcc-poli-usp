from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from ms_agents_server.src.usecase.analysis_usecase import analyze_document_usecase
from datetime import datetime
import tempfile
import os
import logging
import aiofiles

logging.basicConfig(level=logging.INFO)

router = APIRouter()