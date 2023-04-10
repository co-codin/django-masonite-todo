from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
from fastapi.background import BackgroundTasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="localhost",
    port=6379,
    decode_responses=True
)


class Order(HashModel):
    product_id: int
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)


async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

