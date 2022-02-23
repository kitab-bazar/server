from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.package.models import (
    PublisherPackage,
    SchoolPackage,
    CourierPackage,
    PublisherPackageLog,
    SchoolPackageLog,
    CourierPackageLog,
)
from config.serializers import CreatedUpdatedBaseSerializer


class PublisherPackageSnapshotSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = PublisherPackage
        fields = ('status',)


class PublisherPackageLogSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = PublisherPackageLog
        fields = ('comment', 'files')

    def validate_files(self, files):
        for file in files:
            if self.context['request'].user != file.created_by:
                raise serializers.ValidationError(_('Invalid file'))
        return files


class PublisherPackageUpdateSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):
    log = PublisherPackageLogSerializer(required=False)

    class Meta:
        model = PublisherPackage
        fields = ('id', 'status', 'log')

    def update(self, instance, validated_data):
        log_data = validated_data.pop('log', None)
        package = super().update(instance, validated_data)
        snapshot_serializer = PublisherPackageSnapshotSerializer(instance=package)
        if log_data:
            files = log_data.pop('files', None)
            log = PublisherPackageLog.objects.create(
                package=package,
                snapshot=snapshot_serializer.data,
                **log_data,
                created_by=self.context['request'].user
            )
            if files:
                log.files.add(*files)
        return package

    def create(self, data):
        raise Exception('Not allowed')


class SchoolPackageUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolPackage
        fields = ('id', 'status')

    def update(self, instance, data):
        # Create a log
        SchoolPackageLog.objects.create(
            school_package=self.instance,
            created_by=self.context['request'].user,
            comment=data.pop('comment', '')
        )
        # Update
        return super().update(instance, data)

    def create(self, data):
        raise Exception('Not allowed')


class CourierPackageUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourierPackage
        fields = ('id', 'status')

    def update(self, instance, data):
        # Create a log
        CourierPackageLog.objects.create(
            courier_package=self.instance,
            created_by=self.context['request'].user,
            comment=data.pop('comment', '')
        )
        return super().update(instance, data)

    def create(self, data):
        raise Exception('Not allowed')
