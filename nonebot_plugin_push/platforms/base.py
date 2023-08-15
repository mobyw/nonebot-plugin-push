import abc
from typing import Union

from ..message import Message, MessageSegment


class BasePush(abc.ABC):
    """
    Base class for push platforms.
    """

    def __init__(self, name: str, type: str):
        self.name: str = name
        self.type: str = type

    def __repr__(self) -> str:
        return f"Push(type={self.type!r}, name={self.name!r})"

    @abc.abstractmethod
    def send(self, message: Union[str, Message, MessageSegment]):
        raise NotImplementedError
