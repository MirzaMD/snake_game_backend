from fastapi import FastAPI, HTTPException
from src.models.scoreboard import SnakeBoard
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import List
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client["snake_game_db"]
sb = db["scoreboard"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://snake-game-taupe-nu.vercel.app","http://localhost:3000","http://localhost:30001"],
    allow_credentials=True,
    allow_methods=["POST","GET","DELETE","PUT"],
    allow_headers=["*"]
)

def helper_function(item:SnakeBoard)->dict:
    return{
        "_id": str(item["_id"]),
        "user": item["user"],
        "score": item["score"]
    }

@app.post("/api/snake_game")
async def adding_score(item:SnakeBoard):
    try:
        res = await sb.insert_one(item.model_dump())
        if not res.inserted_id:
            raise HTTPException(status_code=500, detail="failed to add the score")
        return {"message":"scoreboard updated succesfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/api/snake_game")
async def retrieve_scoreboard()->List[SnakeBoard]:
    try:
        items=[]
        async for ele in sb.find():
            items.append(helper_function(ele))
        return items
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))        