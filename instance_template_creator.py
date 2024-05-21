from enum import Enum
from dataclasses import dataclass
from google.cloud import compute_v1 
from pathlib import Path
from utils import get_logger

class VMType(Enum):
    STANDARD = "STANDARD"
    SPOT = "SPOT"
    PREEMPTIBLE = "PREEMPTIBLE" # Like spot, but WILL be preempted after 24h

@dataclass
class BootDiskConfig:
    project_id: str
    name: str
    size_gb: int
    labels: dict[str, str]


@dataclass
class VMConfig:
    machine_type: str
    accelerator_count: int
    accelerator_type: str
    vm_type: VMType
    disks: list[str]


@dataclass
class VMMetaDataConfig:
    instance_group_name: str
    docker_image: str
    zone: str
    python_hash_seed: int
    mlflow_tracking_uri: str
    node_count: int
    disks: list[str]


@dataclass
class InstanceTemplateCreator:
    def __init__(
        self,
        scopes: list[str],
        network: str,
        subnetwork: str,
        startup_script_path: str,
        vm_config: VMConfig,
        boot_disk_config: BootDiskConfig,
        vm_metadata_config: VMMetaDataConfig,
        template_name: str,
        project_id: str,
        labels: dict[str, str]
    ) -> None:
        self.logger = get_logger(self.__class__.__name__)

        self.scopes : list[str] = scopes,
        self.network : str = network,
        self.subnetwork : str = subnetwork,
        self.startup_script_path  : str = startup_script_path,
        self.vm_config : VMConfig = vm_config,
        self.boot_disk_config  : BootDiskConfig = boot_disk_config,
        self.vm_metadata_config : VMMetaDataConfig = vm_metadata_config,
        self.template_name : str = template_name,
        self.project_id : str = project_id,
        self.labels : dict[str, str] = labels 

        self.template = compute_v1.InstanceTemplate()
        self.template.name = self.template_name

    def create_template(self) -> compute_v1.InstanceTemplate:
        self.logger.info("Started creating instance template...")
        self.logger.info(f"{self.vm_metadata_config}")

        self._create_boot_disk()
        self._attach_disks()
        self._create_network_interface()
        self._create_machine_configuration()
        self._attach_metadata()

        self.logger.info("Createing instance template ...")
        template_client = compute_v1.InstanceTemplatesClient()
        operation = template_client.insert(project=self.project_id, instance_template_resource=self.template)
        wait_for_extended_operation(operation, "instance template creation")

        self.logger.info("Instance template has been cretaed...")
        return template_client.get(project=self.project_id, instance_template=self.template_name)


    def _create_boot_disk(self) -> None:
        boot_disk = compute_v1.AttachedDisk()
        boot_disk_initialize_params = compute_v1.AttachedDiskInitializeParams()
        boot_disk_image = self._get_disk_image(self.boot_disk_config.project_id, 
                                               self.boot_disk_config.name)
        boot_disk_initialize_params.source_image = boot_disk_image.self_link
        boot_disk_initialize_params.disk_size_gb = self.boot_disk_config.size_gb
        boot_disk_initialize_params.labels = self.boot_disk_config.labels
        boot_disk_initialize_params = boot_disk_initialize_params
        boot_disk.auto_delete = True
        boot_disk.boot = True
        boot_disk.device_name = self.boot_disk_config.name

        self.template.properties.disks = [boot_disk]

    def _get_disk_image(self, project_id: str, image_name: str) -> compute_v1.Image:
        image_client = compute_v1.ImageClient()
        return image_client.get(project=project_id, image=image_name)
    
    def _attach_disks(self) -> None:
        disk_names = self.vm_config.disks 
        for disk_name in disk_names:
            disk = compute_v1.AttachedDisk(auto_delete=False, boot=False, mode="READ_ONLY",
                                           device_name=disk_name, source=disk_name)
            self.template.properties.disks.append(disk)

        if len(disk_names) > 0:
            self.template.properties.metadata.items.append(compute_v1.Items(key="disks", value="\n".jion(disk_names)))


    def _create_network_interface(self) -> None:
        network_interface = compute_v1.Network_Interface()
        network_interface.name = "nic0"
        network_interface.network = self.network
        network_interface.subnetwork = self.subnetwork
        self.template.properties.network_interfaces = [network_interface]

    def _create_machine_configuration(self) -> None:
        self.template.properties.machine_type = self.vm_config.machine_type
        if self.vm_config.accelerator_count > 0:
            self.template.properties.guest_accelerators = [
                compute_v1.AcceleratorConfig(
                    accelerator_type=self.vm_config.accelerator_type,
                    accelerator_count=self.vm_config.accelerator_count,
                )
            ]
        self.template.properties.service_accounts = [compute_v1.ServiceAccount(email="default", scopes=self.scopes)]
        self.template.properties.labels = self.labels

        vm_type = self.vm_config.vm_type
        if vm_type == VMType.PREEMPTIBLE:
            self.logger.info("using PREEMPTIBLE machine")
            self.template.properties.scheduling = compute_v1.Scheduling(preemptible=True)
        elif vm_type == VMType.SPOT:
            self.logger.info("using SPOT machine")
            self.template.properties.scheduling = compute_v1.Scheduling(
                provisioning_model=compute_v1.Scheduling.ProvisioningModel.Spot.name,
                on_host_maintenance=compute_v1.Scheduling.OnHostMaintenance.TERMINATE.name,
            )
        elif vm_type == VMType.STANDARD:
            self.logger.info("using STANDARD machine")
            self.template.properties.scheduling = compute_v1.Scheduling(
                provisioning_model=compute_v1.Scheduling.ProvisioningModel.STANDARD.name,
                on_host_maintenance=compute_v1.Scheduling.OnHostMaintenance.TERMINATE.name,
            )
        else:
            raise RuntimeError(f"Unsupported {vm_type=}")
        
    def _attach_metadata(self) -> None:
        startup_script = self._read_startup_script(self.startup_script_path)
        self.template.properties.metadata.items.append(compute_v1.Items(key="startup-script",
                                                                        value=startup_script))
        
        for meta_data_name, meta_data_value in self.vm_config.items():
            self.template.properties.metadata.items.append(compute_v1.Items(key=meta_data_name, value=meta_data_value))

    def _read_startup_script(self, startup_script_path) -> str:
        return Path(startup_script_path).read_text()





            







