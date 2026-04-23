from fastapi import FastAPI
from app.routes.issues import router as issues_router

app = FastAPI()

app.include_router(issues_router)
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
	{"id": 3, "name": "Item 3"},
]

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items")
def get_items():
	return items


@app.get("/items/{item_id}")
def get_item(item_id: int):
	if item_id == 0:
		return items
	for item in items:
		if item["id"] == item_id:
			return item
	return {"error": "Item not found"}
