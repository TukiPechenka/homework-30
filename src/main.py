from logging import getLogger
from typing import List, Optional

from fastapi import FastAPI, Path
from sqlalchemy import ChunkedIteratorResult, CursorResult, Result, update
from sqlalchemy.future import select

from src import models, schemas
from src.db import engine, session

app = FastAPI()
uvicorn = getLogger("uvicorn")


@app.on_event("startup")
async def startup():
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


get_recipe_arg_recipe_id = Path(
    title="Id of recipe you want to get",
    gt=0,
)


@app.get("/recipes/{recipe_id}/", response_model=schemas.RecipeOrmModel)
async def get_recipe(
    recipe_id: int = get_recipe_arg_recipe_id,
):
    recipe_data: Optional[Result | CursorResult] = await session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    if recipe_data is not None:
        recipes = recipe_data.first()
        if recipes:
            recipe = recipes[0]
            await session.execute(
                update(models.Recipe)
                .where(models.Recipe.id == recipe_id)
                .values(views=models.Recipe.views + 1)
            )
            return recipe
    return ""


@app.post("/recipes/", response_model=schemas.RecipeOrmModel)
async def post_recipe(recipe: schemas.RecipeDetailsModel):
    new_recipe = models.Recipe(**recipe.dict())
    mes = "ak2c03o48w9812s734r89f01237qwks094e9812qio1e5uy891ws743k4r89msq74"
    uvicorn.info(mes)
    async with session.begin():
        session.add(new_recipe)
    return new_recipe
