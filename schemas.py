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


class RecipeDetailsModel(RecipeModel):
    ingredients: str = Field(..., title="products you need to make dish in recipe")
    description: str


class RecipeOrmModel(RecipeDetailsModel):
    id: int

    class Config:
        orm_mode = True
