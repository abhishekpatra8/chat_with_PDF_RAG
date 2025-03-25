from fastapi import APIRouter
from apis import chat_with_doc, file_ops

router = APIRouter()
router.include_router(file_ops.router)
router.include_router(chat_with_doc.router)