from dataclasses import asdict, dataclass

from api.models import User


@dataclass
class UserData(object):
    username: str
    email: str
    password: str
    geo_data: dict

    def to_dict(self, exclude=[]):
        if len(exclude):
            return {k: v for k, v in self.__dict__.items() if k not in exclude}
        return asdict(self)


@dataclass
class PostData(object):
    author: User
    content: str
    likes_count: int

    def to_dict(self, exclude=[]):
        if len(exclude):
            return {k: v for k, v in self.__dict__.items() if k not in exclude}
        return asdict(self)
