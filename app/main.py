from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router import user, post, auth, vote

# models.Base.metadata.create_all(bind=engine) # Creates all of our models in models.py 
# the above line is commented because, now, alembic does it's job

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World from CI/CD all the way to ubuntu!!"}
