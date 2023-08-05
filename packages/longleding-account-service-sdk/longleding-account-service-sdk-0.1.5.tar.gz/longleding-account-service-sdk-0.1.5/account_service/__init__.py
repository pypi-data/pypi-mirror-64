# -*- coding: utf-8 -*-
import inspect
from typing import List, Optional

from .models import UserStatusEnum, AccountServiceException
from .grpc_client import AccountServiceGRPCClient
from .models import UserPagination, User

__all__ = [
    'init_service',
    'get_user_list',
    'get_user_page_list'
]

_client: AccountServiceGRPCClient


def _param_check(func):
    def wrapper(*args, **kwargs):
        global _client
        assert _client is not None, "system settings service sdk must be init first"
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        for i, v in enumerate(args):
            p = params[i]
            assert p.annotation is inspect.Parameter.empty or isinstance(v, p.annotation), "{} must be {}.".format(
                p.name, str(p.annotation))
        return func(*args, **kwargs)

    return wrapper


def init_service(endpoint: str, src: str) -> None:
    global _client
    assert type(endpoint) == str, "endpoint must be a str"
    _client = AccountServiceGRPCClient(endpoint=endpoint, src=src)


@_param_check
def get_user_list(id_list: list) -> List[User]:
    return _client.get_user_list(id_list)


@_param_check
def get_user_page_list(current_page: int = 1, page_size: int = 10, username: str = '', phone: str = '', email: str = '',
                       name: str = '', user_status_list: Optional[List] = None) -> UserPagination:
    if user_status_list is not None:
        validate_user_status_list(user_status_list)
    return _client.get_user_page_list(current_page, page_size, username, phone, email, name, user_status_list)


def validate_user_status_list(user_status_list: list):
    """判断user_status_list是否合法"""
    if not set(user_status_list).issubset(set(UserStatusEnum.value_list())):
        raise AccountServiceException('user_status_list参数不合法')
