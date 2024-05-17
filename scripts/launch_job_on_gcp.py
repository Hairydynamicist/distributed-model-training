from configs.config import setup_config
import hydra
from omegaconf import DictConfig

setup_config()


@hydra.main(config_path=".", config_name="config", version_base=None)
def run(config: DictConfig) -> None:
    pass


if __name__ =="__main__":
    run()