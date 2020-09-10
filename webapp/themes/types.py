from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

from dacite import from_dict

from django.conf import settings


@dataclass
class ThemeSetting:
    id: str
    name: str
    type: str
    default: str
    help_text: Optional[str]
    choices: Optional[Dict[str, str]]

    @property
    def to_dict(self):
        return asdict(self)


@dataclass
class Theme:
    name: str
    folder_name: str
    author: str
    settings: List[ThemeSetting]
    author_website: Optional[str] = None

    @property
    def to_dict(self):
        return asdict(self)

    @property
    def cover(self) -> str:
        return f'{settings.STATIC_URL}themes/{self.folder_name}/img/cover.png'

    @property
    def tablet(self) -> str:
        return f'{settings.STATIC_URL}themes/{self.folder_name}/img/tablet.png'

    @property
    def mobile(self) -> str:
        return f'{settings.STATIC_URL}themes/{self.folder_name}/img/mobile.png'

    @classmethod
    def from_dict(cls, data: dict):
        return from_dict(cls, data)
