from pydantic import BaseModel, Field


class RecipeModel(BaseModel):
    name: str
    cook_time: int = Field(
        ...,
        ge=1,
    )


class RecipeInListModel(RecipeModel):
    id: int
    views: int = Field(
        ...,
        title="How many times recipe details were looked",
        ge=0,
    )


title_recipe_details = "products you need to make dish in recipe"


class RecipeDetailsModel(RecipeModel):
    ingredients: str = Field(..., title=title_recipe_details)
    description: str


class RecipeOrmModel(RecipeDetailsModel):
    id: int

    class Config:
        orm_mode = True
