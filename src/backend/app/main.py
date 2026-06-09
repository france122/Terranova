from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, get_session
from app.routers import graph, map, learn, quest, achievement, social, auth

# Import models so SQLModel creates tables
from app.models import user, progress, achievement as ach_model, quest as q_model, social as s_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # Seed initial data
    from app.services.seed_service import seed_initial_data
    from sqlmodel import Session
    from app.database import engine
    with Session(engine) as session:
        seed_initial_data(session)
    yield


app = FastAPI(
    title="Terranova API",
    description="Terranova - 知识大陆游戏化学习系统",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(graph.router, prefix="/api/graph", tags=["知识图谱"])
app.include_router(map.router, prefix="/api/map", tags=["地图"])
app.include_router(learn.router, prefix="/api/learn", tags=["学习"])
app.include_router(quest.router, prefix="/api/quests", tags=["任务"])
app.include_router(achievement.router, prefix="/api/achievements", tags=["成就"])
app.include_router(social.router, prefix="/api/social", tags=["社交"])


@app.get("/")
def root():
    return {"message": "Welcome to Terranova - 知识大陆"}
