# swagger ui: http://127.0.0.1:8000/docs#

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# path parameter with type
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


"""
All the data validation is performed under the hood by pydantic, so you get all the benefits from it, 
and you know you are in good hands.

You can use the same type declarations with str, float, bool and many other complex data types.
"""


# order mathhers

"""
When creating path operations, you may find situations where you have a fixed path, like /users/me. 
Let’s say that it’s to get data about the current user. 
You might also have the path /users/{user_id} to get data about a specific user by some user ID.

Because path operations are evaluated in order, 
you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:

Otherwise, the path for /users/{user_id} would also match for /users/me, 
thinking that it’s receiving the parameter user_id with a value of "me".
"""

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# request body: receiving json data

"""
Use pydantic to Declare JSON Data Models (Data Shapes)

First, you need to import BaseModel from pydantic 
and then use it to create subclasses defining the schema, or data shapes, you want to receive.

Next, you declare your data model as a class that inherits from BaseModel, 
using standard Python types for all the attributes:
"""

from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

"""
When a model attribute has a default value, it is not required. 
Otherwise, it is required. To make an attribute optional, you can use None.

The parameter item has a type hint of Item, which means that item is declared as an instance of the class Item.

By using standard type hints with pydantic, 
FastAPI helps you build APIs that have all these best practices by default, with little effort.
"""

"""
With that Python type declaration, FastAPI will:

Read the body of the request as JSON
- Convert the corresponding types if needed
- Validate the data and return a clear error if it is invalid
- Give you the received data in the parameter item—since you declared it to be of type Item, 
    you will also have all the editor support, with completion and type checks for all the attributes and their types
- Generate JSON Schema definitions for your model that you can also use anywhere else that makes sense for your project
"""

# request body and path parameters

@app.put("/items/{item_id}")
async def replace_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

"""
This way, you can declare path parameters and JSON request bodies, 
and FastAPI will take care of doing all the data validation, serialization, and documentation for you. 

In a similar way, you can declare more complex request bodies, like lists, and other types of request data, 
like query parameters, cookies, headers, form inputs, files, and so on.
"""











