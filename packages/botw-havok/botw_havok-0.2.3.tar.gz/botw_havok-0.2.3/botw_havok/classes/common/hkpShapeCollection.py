from ..enums.CollectionType import CollectionType
from .hkpShape import hkpShape


class hkpShapeCollection(hkpShape):
    disableWelding: bool
    collectionType: int
