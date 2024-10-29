from typing import Type, Dict

from src.core.transaction import TransactionProcessor


class ProcessFactory:
    _processors: Dict[str, Type[TransactionProcessor]] = {}

    @classmethod
    def register_processor(cls, process_name: str, processor_cls: Type[TransactionProcessor]):
        cls._processors[process_name] = processor_cls

    @classmethod
    def create_processor(cls, process_name: str) -> TransactionProcessor:
        processor_cls = cls._processors.get(process_name)
        if not processor_cls:
            raise ValueError(f"Процесс '{process_name}' не зарегистрирован.")
        return processor_cls()