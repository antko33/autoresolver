from fastapi import APIRouter
from starlette.responses import HTMLResponse

import app.dependencies

router = APIRouter()


@router.post("/generate_table")
async def generate_table():
    filepath = await app.dependencies.generate_table()
    return {"status": "ok", "path": filepath}


@router.get("/", response_class=HTMLResponse)
async def helloworld():
    return """
    <html>
    <title>Э!</title>
        <center>
            <h1>Вийди отсюда, розбiйник</h1>
        </center>
    </html>
    """
