"""Serialization helpers — map between domain entities and MongoDB BSON documents.

Stores UUIDs as strings, enums as their values, and nests value objects via pydantic.
"""
from __future__ import annotations

from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_doc(entity: BaseModel) -> dict:
    """Convert a pydantic entity to a Mongo document. Uses _id = string(id)."""
    data = entity.model_dump(mode="json")
    if "id" in data:
        data["_id"] = str(data.pop("id"))
    return data


def to_entity(doc: dict, cls: Type[T]) -> T:
    """Reconstruct an entity from a Mongo document."""
    if not doc:
        return None
    doc = dict(doc)
    if "_id" in doc and "id" not in doc:
        doc["id"] = doc.pop("_id")
    else:
        doc.pop("_id", None)
    return cls.model_validate(doc)