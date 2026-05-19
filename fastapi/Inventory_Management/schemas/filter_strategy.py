from abc import ABC, abstractmethod
from typing import Any, Protocol
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.Inventory import Products



"""
In a strategy pattern we encapsulated the code that keeps changing. 
we use polymorphism to assign new strategy at runtime. 

"""
class FilterCondition(BaseModel):
    field: str
    operator: str
    value: Any

class FilterRequest(BaseModel):
    filters: list[FilterCondition]

    model_config = {
        "json_schema_extra": {
            "example":{
                   "filters": [{
                        "field": "product_name",
                        "operator": "eq",
                        "value": "Tofu",
                   }]
            }
        }
    }

"""
{
  "filters": [
    {
      "field": "product_name",
      "operator": "contains",
      "value": "chai"
    },
    {
      "field": "unit_price",
      "operator": "gt",
      "value": 20
    }
  ]
}
because the stub would look like this
"""


# =========================
# Strategy Interface
# =========================

class FilterStrategy(Protocol):

    def apply(self, query, column, value):
        ... # to tell no implmentation


# =========================
# Concrete Strategies
# =========================



"""
issubclass(ExactMatchStrategy, FilterStrategy) return False
unlike using abstract method which expicitly inherit the the object. 
protocol/Interface only looks for method implementation.

Runtime enforcement:
abstract method catches error when assignment. 
// it ask has the subclass has written all method signature. 
protocol method catches error during method singature use, not during assignment.
"""

class ExactMatchStrategy:

    def apply(self, query, column, value):
        return query.where(column == value)


class GreaterThanStrategy:

    def apply(self, query, column, value):
        return query.where(column > value)


class GreaterThanEqualStrategy:

    def apply(self, query, column, value):
        return query.where(column >= value)


class LessThanStrategy:

    def apply(self, query, column, value):
        return query.where(column < value)


class LessThanEqualStrategy:

    def apply(self, query, column, value):
        return query.where(column <= value)


class ContainsStrategy:

    def apply(self, query, column, value):
        return query.where(column.ilike(f"%{value}%"))


class StartsWithStrategy:

    def apply(self, query, column, value):
        return query.where(column.ilike(f"{value}%"))


class EndsWithStrategy:

    def apply(self, query, column, value):
        return query.where(column.ilike(f"%{value}"))




STRATEGIES: dict[str, FilterStrategy] = {
    "eq": ExactMatchStrategy(),
    "gt": GreaterThanStrategy(),
    "gte": GreaterThanEqualStrategy(),
    "lt": LessThanStrategy(),
    "lte": LessThanEqualStrategy(),
    "contains": ContainsStrategy(),
    "startswith": StartsWithStrategy(),
    "endswith": EndsWithStrategy(),
}

# =========================
# Strategy Registry
# =========================

ALLOWED_FIELDS = {
    "product_name": Products.product_name,
    "unit_price": Products.unit_price,
}

