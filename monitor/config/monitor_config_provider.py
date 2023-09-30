from abc import ABC, abstractmethod
from .monitor_config import MonitorConfig

class MonitorConfigProvider(ABC):
    @abstractmethod
    def get_config(self) -> MonitorConfig:
        pass