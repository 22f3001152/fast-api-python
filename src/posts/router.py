from class_based_fastapi import Routable, delete, get, post, put
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.configs.database.database import get_db
from src.posts import models, schemas

router = APIRouter()


class ItemsAPI(Routable):
    """
    Items API
    """

    NAME_MODULE = models.Item.__name__
    db: Session = Depends(get_db)

    @get("/items")
    async def read_items(self) -> list[schemas.Item]:
        """
        Get all Items
        """
        items = self.db.query(models.Item).all()
        return items

    @put("/items/{item_id}")
    async def update_item(self, item_id: int, data: schemas.ItemUpdate) -> schemas.Item:
        """
        Update Item
        """
        item = self.db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        for key, value in data.model_dump().items():
            setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)

        return item

    @post("/items")
    async def create_item(self, data: schemas.ItemCreate) -> schemas.Item:
        """
        Create new Item
        """
        item = models.Item(**data.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item

    @delete("/items/{item_id}")
    async def delete_item(self, item_id: int) -> None:
        """
        Delete Item
        """
        item = self.db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        self.db.delete(item)
        self.db.commit()
