from typing import Any, Dict

class DependencyContainer:
    _instances: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str, instance: Any) -> None:
        cls._instances[key] = instance

    @classmethod
    def get(cls, key: str) -> Any:
        return cls._instances.get(key)

container = DependencyContainer()
