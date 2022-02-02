from django.utils.functional import cached_property
from config.dataloaders import GlobalDataLoaders
from config.permissions import UserPermissions


class GQLContext:
    def __init__(self, request):
        self.request = request
        # global dataloaders
        self.one_to_many_dataloaders = {}
        self.count_dataloaders = {}
        # ----------------------------------------------------------------------
        # Set permissions by user type
        # ----------------------------------------------------------------------
        if not request.user.is_anonymous:
            self.user_permissions = UserPermissions.get_permissions(request.user.user_type)
            self.request.user_permissions = self.user_permissions

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def dl(self):
        return GlobalDataLoaders(context=self)
