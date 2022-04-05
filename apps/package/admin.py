from django.contrib import admin

from apps.package.models import (
    PublisherPackageBook,
    PublisherPackage,
    SchoolPackageBook,
    SchoolPackage,
    CourierPackage,
    InstitutionPackage,
    InstitutionPackageBook,
)


class PublisherPackageBookAdmin(admin.ModelAdmin):
    search_fields = ['book__name', 'publisher_package__name']
    autocomplete_fields = ['book', 'publisher_package']


class PublisherPackageAdmin(admin.ModelAdmin):
    search_fields = ['publisher__name', 'related_orders__id']
    autocomplete_fields = ['publisher', 'related_orders']


class SchoolPackageBookAdmin(admin.ModelAdmin):
    search_fields = ['book__name', 'school_package__id']
    autocomplete_fields = ['book', 'school_package']


class SchoolPackageAdmin(admin.ModelAdmin):
    search_fields = ['school_name', 'related_orders__id']
    autocomplete_fields = ['school', 'related_orders']


class InstitutionPackageBookAdmin(admin.ModelAdmin):
    search_fields = ['book__name', 'school_package__id']
    autocomplete_fields = ['book',]


class InstitutionPackageAdmin(admin.ModelAdmin):
    search_fields = ['institution_name', 'related_orders__id']
    autocomplete_fields = ['institution', 'related_orders']


class CourierPackageAdmin(admin.ModelAdmin):
    pass


admin.site.register(PublisherPackageBook, PublisherPackageBookAdmin)
admin.site.register(PublisherPackage, PublisherPackageAdmin)
admin.site.register(SchoolPackageBook, SchoolPackageBookAdmin)
admin.site.register(SchoolPackage, SchoolPackageAdmin)
admin.site.register(CourierPackage, CourierPackageAdmin)
admin.site.register(InstitutionPackage, InstitutionPackageAdmin)
admin.site.register(InstitutionPackageBook, InstitutionPackageBookAdmin)
