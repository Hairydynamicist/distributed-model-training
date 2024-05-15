from dataclasses import dataclass
from typing import Any
from omegaconf import SI

@dataclass
class BootDiskConfig:
    project_id: str = "ubuntu-os-cloud"
    name: str = "ubuntu-2204-jammy-v20230714"
    size_gb: int = 50
    labels: Any = SI("${}")

@dataclass
class VMConfig:
    machine_type: str = "n1-standard-1"
    accelerator_count: int = 0
    accelerator_type: str = "nvidia-tesla-t4"
    vm_type: VMType = VMType.STANDARD
    disks: list[str] = field(default_factory=lambda: []) 

@dataclass
class VMMetaDataConfig:
    instance_group_name: str = SI(${})
    docker_image: str = SI(${})
    zone: str = SI(${})
    python_hash_seed: int = 442
    mlflow_tracking_uri: str = SI(${})
    node_count: int = SI(${})
    disks: list[str] = SI(${})   
