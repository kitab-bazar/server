from typing import List, Callable
import logging
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

PERMISSION_DENIED_MESSAGE = _('You do not have permission to perform this action.')

logger = logging.getLogger(__name__)


def permission_checker(perms: List[str]) -> Callable[..., Callable]:
    def wrapped(func):
        def wrapped_func(root, info, *args, **kwargs):
            if not info.context.user.has_perms(perms):
                raise PermissionDenied(PERMISSION_DENIED_MESSAGE)
            return func(root, info, *args, **kwargs)
        return wrapped_func
    return wrapped


def is_authenticated() -> Callable[..., Callable]:
    def wrapped(func):
        def wrapped_func(root, info, *args, **kwargs):
            if not info.context.user.is_authenticated:
                raise PermissionDenied(PERMISSION_DENIED_MESSAGE)
            return func(root, info, *args, **kwargs)
        return wrapped_func
    return wrapped
