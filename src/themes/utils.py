import json
from pathlib import Path
from typing import List

from dacite.exceptions import WrongTypeError

from django.conf import settings

from themes.types import Theme


THEMES_DIR = Path(settings.BASE_DIR) / 'themes' / 'templates' / 'themes'


def get_themes_names() -> List[tuple]:
    return [
        (folder.name, folder.name) for folder in THEMES_DIR.glob('*')
    ]


def get_themes() -> List[Theme]:
    templates = []
    for folder in sorted(THEMES_DIR.glob('*')):
        config_file = folder / 'config.json'
        theme_config = json.loads(config_file.read_text())
        theme_config['folder_name'] = folder.name
        try:
            templates.append(Theme.from_dict(theme_config))
        except WrongTypeError:
            pass
    return templates


def get_theme(folder_name: str, language: str = 'en') -> Theme:
    config_file = THEMES_DIR / folder_name / 'config.json'
    theme_config = json.loads(config_file.read_text())
    if 'language' != 'en':
        for i, option in enumerate(theme_config['settings']):
            for key, value in option.items():
                if key.endswith(f'_{language}'):
                    theme_config['settings'][i][key[:-3]] = theme_config['settings'][i][key]
    theme_config['folder_name'] = folder_name
    return Theme.from_dict(theme_config)
