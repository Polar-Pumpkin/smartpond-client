from datetime import datetime
from typing import List

from client.network.packet import serializable


@serializable()
class Pond:
    _id: str
    name: str
    owner: str
    collaborators: List[str]
    activated: bool
    created: datetime
