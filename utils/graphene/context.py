from django.utils.functional import cached_property
from config.dataloaders import GlobalDataLoaders
from config.permissions import BookPermissions
from config.permissions import PublisherPermissions
from config.permissions import SchoolPermissions
from config.permissions import InstitutionPermissions


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
            self.book_permissions = BookPermissions.get_permissions(request.user.user_type)
            self.request.book_permissions = self.book_permissions

            self.publisher_permissions = PublisherPermissions.get_permissions(request.user.user_type)
            self.request.publisher_permissions = self.publisher_permissions

            self.school_admin_permissions = SchoolPermissions.get_permissions(request.user.user_type)
            self.request.school_admin_permissions = self.school_admin_permissions

            self.institution_permissions = InstitutionPermissions.get_permissions(request.user.user_type)
            self.request.institution_permissions = self.institution_permissions

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def dl(self):
        return GlobalDataLoaders(context=self)
