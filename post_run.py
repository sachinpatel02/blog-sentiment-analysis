import uvicorn

if __name__ == "__main__":
    uvicorn.run("services.post_service.app.main:app", reload=True, port=8001)