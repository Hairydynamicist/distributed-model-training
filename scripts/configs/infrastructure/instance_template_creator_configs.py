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

@dataclass:
class InstanceTemplateCreatorConfig:
_target_: str = "instance_template_creator.InstanceTemplateCreator"
scopes: list[str] =  field(default_factory=lambda:[
    "https://www.googleapis.com/auth/cloud-platform"
    "https://www.googleapis.com/auth/clouduseraccounts.readonly"
    "https://www.googleapis.com/auth/cloudruntimeconfig"
])
network: str = SI("https://www.googleapis.com/compute/v1/projects/${.project_id}/global/networks/default")
subnetwork: str = SI("https://www.googleapis.com/compute/v1/projects/${.project_id}/regions/europe-west4/subnetworks/default")
startup_script_path: str = "scripts/task_runner_startup_script.sh"
vm_config: VMConfig = VMConfig()
boot_disk_config: BootDiskConfig = BootDiskConfig()
vm_metadata_config: VMMetaDataConfig = VMMetaDataConfig()
template_name: str = SI("${}")
project_id: str = SI("${}")
labels: dict[str, str] = field(default_factory=lambda: {
    "project": cybulde
})