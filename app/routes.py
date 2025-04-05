from fastapi import APIRouter
from starlette.background import BackgroundTasks
from starlette.responses import HTMLResponse

import app.dependencies
from app.sender import send_file_to_user

router = APIRouter()


@router.post("/generate_table")
async def generate_table(bg_tasks: BackgroundTasks):
    bg_tasks.add_task(__run_generation)
    return {"status": 200}


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


async def __run_generation():
    filepath = await app.dependencies.generate_table()
    await send_file_to_user(filepath)
