from abc import ABC, abstractmethod

class Connection(ABC):
    @abstractmethod
    async def connect(self):
        """Establish a connection."""
        pass

    @abstractmethod
    async def close(self):
        """Close the connection."""
        pass


class WithConnectionPool(ABC):
    @abstractmethod
    async def connection_pool_factory(self):
        raise NotImplementedError("Subclasses must implement get_session method")