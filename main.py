from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
app = FastAPI()

load_dotenv()

db_url=os.getenv('MONGODB_URI')
db_name=os.getenv('DB_NAME')

client=AsyncIOMotorClient(db_url)
db=client[db_name]

@app.get('/',response_class=HTMLResponse)
async def read_root():
    if(await db):
        return 'yes'
    return """<h1>Hello</h1> """
