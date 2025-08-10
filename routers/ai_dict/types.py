from pydantic import BaseModel, Field, StringConstraints
from typing import List
from typing_extensions import Annotated


NonEmptyString = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]


class Definition(BaseModel):
    definition: NonEmptyString = Field(..., description="The text of the definition.")
    example: NonEmptyString = Field(
        ..., description="An example sentence using the word."
    )


class DictionaryEntry(BaseModel):
    """Model representing a dictionary entry."""

    word: NonEmptyString = Field(..., description="The main word being defined.")
    phonetic: NonEmptyString = Field(
        ..., description="The pronunciation (IPA) of the word."
    )
    part_of_speech: NonEmptyString = Field(
        ..., description="The grammatical category of the word."
    )
    definitions: List[Definition] = Field(
        ..., description="List of definitions for the word."
    )
    origin: NonEmptyString = Field(
        ..., description="The etymology or origin of the word."
    )

    class Config:
        extra = "forbid"  # Disallow unexpected fields
