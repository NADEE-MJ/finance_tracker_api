from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.crud.base import CRUDBase
from api.db.models import Crypto
from api.schema.crypto import CryptoCreate, CryptoUpdate


class CRUDCrypto(CRUDBase[Crypto, CryptoCreate, CryptoUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CryptoCreate, owner_id: int
    ) -> Crypto:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Crypto]:
        return (
            db.query(self.model)
            .filter(Crypto.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crypto = CRUDCrypto(Crypto)
