import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.openapi.utils import get_openapi
from pydantic import PositiveInt
from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey

from models import Message, MessageRequestDto

app = FastAPI()

API_KEY = "apikey123abc"
API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

Message_Model = pydantic_model_creator(Message, name="MessageOut", exclude=('id_message',))


async def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.post('/get_openapi')
async def get_openapi_info(api_key: APIKey = Depends(get_api_key)):
    return JSONResponse(
        get_openapi(title="FastAPI security test", version='1', routes=app.routes)
    )


@app.post('/messages', status_code=201)
async def send_message(messageDto: MessageRequestDto, api_key: APIKey = Depends(get_api_key)):
    message = Message(message_text=messageDto.message_text, view_counter=0)
    await message.save()
    return f'message was sent. It\'s id:{message.id_message}'


@app.put('/messages/{id_message}', status_code=204)
async def update_message(messageDto: MessageRequestDto, id_message: PositiveInt,
                         api_key: APIKey = Depends(get_api_key)):
    message = await Message.get(id_message=id_message)
    message.message_text = messageDto.message_text
    message.view_counter = 0
    await message.save()


@app.get('/messages/{id_message}', status_code=200)
async def get_message(id_message: PositiveInt, api_key: APIKey = Depends(get_api_key)):
    message = await Message.get(id_message=id_message)
    message.view_counter += 1
    await message.save()
    return await Message_Model.from_tortoise_orm(message)


@app.delete('/messages/{id_message}', status_code=204)
async def delete_message(id_message: PositiveInt, api_key: APIKey = Depends(get_api_key)):
    message = await Message.get(id_message=id_message)
    await message.delete()


if __name__ == '__main__':
    uvicorn.run(app)

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)
