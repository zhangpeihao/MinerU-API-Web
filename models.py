from pydantic import BaseModel, HttpUrl, Field, constr
from typing import Optional, List
from datetime import datetime

class FileUrlRequest(BaseModel):
    url: HttpUrl
    is_ocr: Optional[bool] = False
    data_id: Optional[constr(
        max_length=128, 
        pattern=r'^[a-zA-Z0-9_\-\.]+$'
    )] = None

class BatchUrlExtractRequest(BaseModel):
    enable_formula: Optional[bool] = True
    enable_table: Optional[bool] = True
    layout_model: Optional[str] = Field(
        default="doclayout_yolo",
        pattern='^(doclayout_yolo|layoutlmv3)$'
    )
    language: Optional[str] = "ch"
    callback: Optional[HttpUrl] = None
    seed: Optional[constr(
        max_length=64,
        pattern=r'^[a-zA-Z0-9_]+$'
    )] = None
    files: List[FileUrlRequest] = Field(..., max_items=200)

class BatchUrlExtractResponse(BaseModel):
    code: int
    data: dict
    msg: str
    trace_id: str