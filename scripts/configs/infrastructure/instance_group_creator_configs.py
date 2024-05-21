from dataclasses import dataclass
from .instance_template_creator_configs import InstanceTemplateCreatorConfig
from omegaconf import SI

@dataclass
class InstanceGroupCreatorConfig:
    _target_: str = "distributed_model_training.instance_group_creator.InstanceGroupCreator"
    instance_template_creator: InstanceTemplateCreatorConfig = InstanceTemplateCreatorConfig
    name: str = SI("${infrastructure.mlflow.experiment_name}-${infrastructure.mlflow.run_name}-${now:%Y%m%d%H%M%S}")
    node_count: int = 1
    project_id: str = SI("${infrastructure.project_id}")
    zone: str = SI("${infrastructure.zone}")