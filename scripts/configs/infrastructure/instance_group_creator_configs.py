from dataclasses import dataclass
from configs.infrastructure.instance_template_creator_configs import InstanceTemplateCreatorConfig

@dataclass
class InstanceGroupCreatorConfig:
    _target_: str = "instance_group_creator.InstanceGroupeCreator"
    instance_template_creator: InstanceTemplateCreatorConfig = InstanceTemplateCreatorConfig
    name: str = SI("${}")
    node_count: int = 1
    project_id: str = SI("${}")
    zone: str = SI("${}")