from fastapi import FastAPI
from app.database import Base, engine
import app.models

app=FastAPI(
    title="timberbiz API",
    description="Timber Business Platform — Tree Listings + Furniture Shop",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message":"Welcome"}