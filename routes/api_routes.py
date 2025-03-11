from fastapi import APIRouter
from apis import chat_with_doc

router = APIRouter()
router.include_router(chat_with_doc.router)