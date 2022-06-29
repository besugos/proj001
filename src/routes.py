from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Projeto 001"}


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "Healthy"}










