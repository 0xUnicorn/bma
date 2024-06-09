"""API schema for tags."""
from ninja import ModelSchema
from ninja import Schema
from utils.schema import ApiResponseSchema

from .models import BmaTag


class MultipleTagRequestSchema(Schema):
    """The schema used for tags in requests."""

    tags: list[str] = []  # noqa: RUF012


##################################################################################################################


class TagResponseSchema(ModelSchema):
    """The schema used to represent a tag in a response."""

    name: str
    weight: int

    class Config:
        """Specify the model fields to allow."""

        model = BmaTag
        model_fields = ("name",)

    @staticmethod
    def resolve_weight(obj: BmaTag) -> int:
        """Get the number of times this tag has been applied to the object."""
        # NOTE: weight is only available if the weighted tag manager has
        # been used in the endpoint using this schema
        return obj.weight  # type: ignore[no-any-return]


class MultipleTagResponseSchema(ApiResponseSchema):
    """The schema used to return a response with multiple tag objects."""

    bma_response: list[TagResponseSchema]
