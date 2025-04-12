from fastapi import FastAPI

from .metadata import fetch_project_metadata

metadata = fetch_project_metadata()
app = FastAPI(**metadata)


@app.get("/")
async def test_app():
    return "Hello World"
