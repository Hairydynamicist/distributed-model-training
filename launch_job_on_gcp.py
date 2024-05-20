from scripts.configs.config import setup_config
import hydra
from omegaconf import DictConfig
import sys

sys.path

setup_config()


@hydra.main(config_path=".", config_name="config", version_base=None)
def run(config: DictConfig) -> None:
    sys.path


if __name__ =="__main__":
    run()