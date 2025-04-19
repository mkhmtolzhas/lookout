from abc import ABC, abstractmethod
from io import BytesIO


class Storage(ABC):
    @abstractmethod
    async def upload(self, file: BytesIO, file_name: str) -> str:
        """Upload a file to the storage and return the URL."""
        pass


