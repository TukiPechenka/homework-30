from typing import List
from fastapi import FastAPI, Path
from sqlalchemy.future import select
from sqlalchemy import insert, update, CursorResult, ChunkedIteratorResult
from logging import getLogger
from db import engine, session
import schemas
import models


app = FastAPI()
uvicorn = getLogger("uvicorn")


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/recipes/", response_model=List[schemas.RecipeInListModel])
async def get_recipes():
    recipes: ChunkedIteratorResult = await session.execute(
        select(
            models.Recipe.id,
            models.Recipe.name,
            models.Recipe.views,
            models.Recipe.cook_time,
        ).order_by(models.Recipe.views)
    )
    return list(recipes.all())


@app.get("/recipes/{recipe_id}/", response_model=schemas.RecipeOrmModel)
async def get_recipe(
    recipe_id: int = Path(
        title="Id of recipe you want to get",
        gt=0,
    )
):
    recipe: ChunkedIteratorResult = await session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = recipe.first()[0]
    await session.execute(
        update(models.Recipe)
        .where(models.Recipe.id == recipe_id)
        .values(views=models.Recipe.views + 1)
    )
    return recipe


@app.post("/recipes/", response_model=schemas.RecipeOrmModel)
async def post_recipe(recipe: schemas.RecipeDetailsModel):
    new_recipe = models.Recipe(**recipe.dict())
    uvicorn.info("ak2c03o48w9812s734r89f01237qwks094e9812qio1e5uy891ws743k4r89msq74")
    async with session.begin():
        session.add(new_recipe)
    return new_recipe
