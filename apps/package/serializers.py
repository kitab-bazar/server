from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.package.models import (
    PublisherPackage,
    SchoolPackage,
    CourierPackage,
    PublisherPackageLog,
    SchoolPackageLog,
    CourierPackageLog,
    InstitutionPackage,
    InstitutionPackageLog,
)
from config.serializers import CreatedUpdatedBaseSerializer


class SnapshotSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = PublisherPackage
        fields = ('status',)


class UpdateLogMixin(metaclass=serializers.SerializerMetaclass):
    files = serializers.FileField(max_length=None, allow_null=True, required=False)
    comment = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        print(instance.__class__.__name__)
        log_model = {
            'PublisherPackage': PublisherPackageLog,
            'SchoolPackage': SchoolPackageLog,
            'CourierPackage': CourierPackageLog,
            'InstitutionPackage': InstitutionPackageLog,
        }.get(instance.__class__.__name__)

        log_field = {
            'PublisherPackage': 'publisher_package',
            'SchoolPackage': 'school_package',
            'CourierPackage': 'courier_package',
            'InstitutionPackage': 'institution_package',
        }.get(instance.__class__.__name__)

        comment = validated_data.get('comment', None)
        files = validated_data.get('files', None)
        package = super().update(instance, validated_data)
        snapshot_serializer = SnapshotSerializer(instance=package)
        log_data = {log_field: package}

        if comment or files:
            log = log_model.objects.create(
                **log_data,
                snapshot=snapshot_serializer.data,
                comment=comment,
                created_by=self.context['request'].user
            )
            if files:
                log.files.add(*files)
        return package

    def validate_files(self, files):
        for file in files:
            if self.context['request'].user != file.created_by:
                raise serializers.ValidationError(_('Invalid file'))
        return files


class PublisherPackageUpdateSerializer(UpdateLogMixin, serializers.ModelSerializer):

    class Meta:
        model = PublisherPackage
        fields = ('id', 'status', 'files', 'comment')

    def create(self, data):
        raise Exception('Not allowed')


class SchoolPackageUpdateSerializer(UpdateLogMixin, serializers.ModelSerializer):

    class Meta:
        model = SchoolPackage
        fields = ('id', 'status', 'files', 'comment')

    def create(self, data):
        raise Exception('Not allowed')


class CourierPackageUpdateSerializer(UpdateLogMixin, serializers.ModelSerializer):

    class Meta:
        model = CourierPackage
        fields = ('id', 'status', 'files', 'comment')

    def create(self, data):
        raise Exception('Not allowed')


class InstitutionPackageUpdateSerializer(UpdateLogMixin, serializers.ModelSerializer):

    class Meta:
        model = InstitutionPackage
        fields = ('id', 'status', 'files', 'comment')

    def create(self, data):
        raise Exception('Not allowed')
