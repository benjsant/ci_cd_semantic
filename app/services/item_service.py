from sqlmodel import Session, select

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Opérations CRUD sur les items."""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
        """Récupère les items avec pagination."""
        statement = select(Item).offset(skip).limit(limit)
        return list(db.exec(statement).all())

    @staticmethod
    def get_by_id(db: Session, item_id: int) -> Item | None:
        """Récupère un item par ID, ou None."""
        return db.get(Item, item_id)

    @staticmethod
    def create(db: Session, item_data: ItemCreate) -> Item:
        """Crée un item et le persiste en base."""
        item = Item(**item_data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update(db: Session, item_id: int, item_data: ItemUpdate) -> Item | None:
        """Met à jour partiellement un item (exclude_unset)."""
        item = db.get(Item, item_id)
        if not item:
            return None

        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, item_id: int) -> bool:
        """Supprime un item. Retourne False s'il n'existe pas."""
        item = db.get(Item, item_id)
        if not item:
            return False

        db.delete(item)
        db.commit()
        return True
