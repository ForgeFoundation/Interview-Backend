import uvicorn
from fastapi import FastAPI, Depends, File, UploadFile, Path, status, BackgroundTasks, HTTPException


from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models
import os, json
from sqlalchemy.ext.declarative import declarative_base
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi.openapi.docs import get_swagger_ui_html

from routes import utils, api, forumRoutes




app = FastAPI(
    docs_url=None,
    title="Sase Project",
    description='API for SASE Hackathon',
    )

Base = declarative_base()

def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()



# userRoutes = SQLAlchemyCRUDRouter(
#     schema=models.ViewUser,
#     db_model=models.User,
#     prefix=models.User.__tablename__,
#     create_schema=models.CreateUser,
#     update_schema=models.CreateUser,
#     db=get_db
# )

# app.include_router(userRoutes)

@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="DD API",
    )



origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(utils.router)
app.include_router(api.router)
app.include_router(forumRoutes.router)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return { "message": "Welcome to api"}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')

