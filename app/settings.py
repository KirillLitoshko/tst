import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'app' / 'static'
TEMPLATE_PATH = BASE_DIR/ 'app' / 'templates'
CONFIG_PATH = BASE_DIR / 'config' / 'config.yaml'


def get_config(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config


