"""Definition of Types"""
from dataclasses import dataclass
from enum import auto, Enum
from typing import Dict, List


class Type(Enum):
    """Types of supported validation templates"""
    def __str__(self) -> str:
        return self.name
    
    SQL         = auto()
    STORED_PROC = auto()
    FUNCTION    = auto()

class TypeAttr(Enum):
    """Types of attributes supported for validation types"""

    def __str__(self) -> str:
        return self.name

    QUERY      = auto()
    INPUT_ARGS = auto()
    FUNCTION   = auto()
    CALLBACK   = auto()

@dataclass(repr=False)
class Template:

    name : str
    type : Type
    desc : str
    attrs: List[TypeAttr]

    def __repr__(self) -> str:
        return f"NAME: {self.name}, TYPE: {self.type}, DESC: {self.desc}, ATTRS: {[attr for attr in self.attrs]}"



@dataclass(repr=False)
class Validation:
    # TODO: move this to a separate module
    
    name : str
    type : Type
    desc : str
    attrs: List[Dict[TypeAttr, str]]

    def __repr__(self) -> str:
        return f"NAME: {self.name}, TYPE: {self.type}, DESC: {self.desc}, ATTRS: {[attr for attr in self.attrs]}"
