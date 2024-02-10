
from fastapi import APIRouter

router = APIRouter(
    prefix="/utils",
    responses={404: {"description": "Not found"}},
    tags=["Utils"]
)





