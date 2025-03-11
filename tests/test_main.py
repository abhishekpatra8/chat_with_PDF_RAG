from fastapi.testclient import TestClient
from fastapi import status
from ..apis import chat_with_doc

client = TestClient(chat_with_doc.router)

def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status_code": 200, "message": "App is working !!"}