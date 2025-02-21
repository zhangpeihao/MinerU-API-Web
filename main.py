from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from models import BatchUrlExtractRequest, BatchUrlExtractResponse
from api_client import MineruAPIClient
from config import get_settings
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Document Extract Service",
    description="批量文档提取服务 API",
    version="1.0.0"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()
api_client = MineruAPIClient()

@app.post(
    "/api/batch-extract",
    response_model=BatchUrlExtractResponse,
    summary="批量提交URL文档提取任务",
    description="""
    批量提交URL文档提取任务。
    
    限制：
    - 单次最多支持200个文件
    - 每个文件大小不超过200MB
    - 每个文件页数不超过600页
    - 不建议使用github、aws等国外URL
    """
)
async def create_batch_extract(
    request: BatchUrlExtractRequest,
    background_tasks: BackgroundTasks
):
    try:
        # 验证文件数量
        if len(request.files) > settings.MAX_FILES:
            raise HTTPException(
                status_code=400,
                detail=f"Number of files exceeds maximum limit of {settings.MAX_FILES}"
            )

        # 记录请求日志
        logger.info(f"Received batch extract request with {len(request.files)} files")

        # 提交任务
        response = api_client.submit_batch_extract(request)
        
        # 如果有callback，添加后台任务处理结果通知
        if request.callback:
            background_tasks.add_task(
                handle_callback_notification,
                batch_id=response.data["batch_id"],
                callback_url=request.callback,
                seed=request.seed
            )

        return response

    except TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Request timeout. Please try again later."
        )
    except Exception as e:
        logger.error(f"Error processing batch extract request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get(
    "/api/batch-extract/{batch_id}",
    summary="获取批量任务状态",
    description="通过batch_id获取批量提取任务的状态和结果"
)
async def get_batch_extract_status(batch_id: str):
    try:
        return api_client.get_batch_status(batch_id)
    except Exception as e:
        logger.error(f"Error getting batch status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

async def handle_callback_notification(
    batch_id: str,
    callback_url: str,
    seed: str = None
):
    """处理回调通知"""
    # 实现回调逻辑
    pass