import uvicorn

if __name__ == "__main__":
    uvicorn.run("services.user_service.app.main:app", reload=True)