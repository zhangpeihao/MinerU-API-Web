import requests
from typing import Optional, Dict, Any, List
import json

class MineruClient:
    def __init__(self, token: str, base_url: str = "https://mineru.net/api/v4"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

    def create_single_task(self, url: str, is_ocr: bool = False, 
                          enable_formula: bool = True, enable_table: bool = True,
                          layout_model: str = "doclayout_yolo", 
                          language: str = "ch", data_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a single file parsing task"""
        endpoint = f"{self.base_url}/extract/task"
        data = {
            "url": url,
            "is_ocr": is_ocr,
            "enable_formula": enable_formula,
            "enable_table": enable_table,
            "layout_model": layout_model,
            "language": language
        }
        if data_id:
            data["data_id"] = data_id

        response = requests.post(endpoint, headers=self.headers, json=data)
        return response.json()

    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """Get the result of a task"""
        endpoint = f"{self.base_url}/extract/task/{task_id}"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

    def create_batch_upload_urls(self, files: List[Dict[str, Any]], 
                               enable_formula: bool = True,
                               enable_table: bool = True,
                               layout_model: str = "doclayout_yolo",
                               language: str = "ch") -> Dict[str, Any]:
        """Create batch file upload URLs"""
        endpoint = f"{self.base_url}/file-urls/batch"
        data = {
            "enable_formula": enable_formula,
            "enable_table": enable_table,
            "layout_model": layout_model,
            "language": language,
            "files": files
        }
        response = requests.post(endpoint, headers=self.headers, json=data)
        return response.json()

    def upload_file(self, upload_url: str, file_data: bytes) -> bool:
        """Upload a file to the provided URL"""
        response = requests.put(upload_url, data=file_data)
        return response.status_code == 200

    def get_batch_results(self, batch_id: str) -> Dict[str, Any]:
        """Get batch processing results"""
        endpoint = f"{self.base_url}/extract-results/batch/{batch_id}"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()