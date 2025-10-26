from fastapi import FastAPI
from database import engine, base
from routers import users, todos
from fastapi.middleware.cors import CORSMiddleware


base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo APP")


app.include_router(users.router)
app.include_router(todos.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # برای تست همه منبع‌ها
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

