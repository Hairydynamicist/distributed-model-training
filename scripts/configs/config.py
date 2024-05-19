from dataclasses import dataclass, field
from scripts.configs.infrastructure.infrastructure_configs import InfrastructureConfig

from hydra.core.config_store import ConfigStore

@dataclass
class Config:
    infrastructure: InfrastructureConfig = field(default_factory=InfrastructureConfig)
    docker_image: str = "asd"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
