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
from apps.order.models import Order
from config.serializers import CreatedUpdatedBaseSerializer


class SnapshotSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = PublisherPackage
        fields = ('status',)


class UpdateLogMixin(metaclass=serializers.SerializerMetaclass):
    files = serializers.FileField(max_length=None, allow_null=True, required=False)
    comment = serializers.CharField(required=False)

    def update(self, instance, validated_data):
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

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        instance.related_orders.update(status=status)
        _order_status_map = {
            SchoolPackage.Status.PENDING.value: Order.Status.PENDING.value,
            SchoolPackage.Status.IN_TRANSIT.value: Order.Status.IN_TRANSIT.value,
            SchoolPackage.Status.ISSUE.value: Order.Status.PENDING.value,
            SchoolPackage.Status.DELIVERED.value: Order.Status.COMPLETED.value,
        }
        Order.objects.filter(
            order_code__in=instance.related_orders.all().values_list('order_code', flat=True)
        ).update(status=_order_status_map.get(status))
        return super().update(instance, validated_data)


class CourierPackageUpdateSerializer(UpdateLogMixin, serializers.ModelSerializer):

    class Meta:
        model = CourierPackage
        fields = ('id', 'status', 'files', 'comment')

    def create(self, data):
        raise Exception('Not allowed')

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        _order_status_map = {
            CourierPackage.Status.PENDING.value: Order.Status.PENDING.value,
            CourierPackage.Status.IN_TRANSIT.value: Order.Status.IN_TRANSIT.value,
            CourierPackage.Status.ISSUE.value: Order.Status.PENDING.value,
            CourierPackage.Status.DELIVERED.value: Order.Status.COMPLETED.value,
        }

        _school_packages_status_map = {
            CourierPackage.Status.PENDING.value: SchoolPackage.Status.PENDING.value,
            CourierPackage.Status.IN_TRANSIT.value: SchoolPackage.Status.IN_TRANSIT.value,
            CourierPackage.Status.ISSUE.value: SchoolPackage.Status.ISSUE.value,
            CourierPackage.Status.DELIVERED.value: SchoolPackage.Status.DELIVERED.value,
        }

        _update_institution_package_status_map = {
            CourierPackage.Status.PENDING.value: InstitutionPackage.Status.PENDING.value,
            CourierPackage.Status.IN_TRANSIT.value: InstitutionPackage.Status.IN_TRANSIT.value,
            CourierPackage.Status.ISSUE.value: InstitutionPackage.Status.ISSUE.value,
            CourierPackage.Status.DELIVERED.value: InstitutionPackage.Status.DELIVERED.value,
        }

        # Update school packages and orders
        school_courier_package_ids = instance.courier_package.all().values_list('id', flat=True)
        SchoolPackage.objects.filter(
            id__in=school_courier_package_ids
        ).update(
            status=_school_packages_status_map.get(status),
        )
        Order.objects.filter(school_related_orders__in=school_courier_package_ids).update(
            status=_order_status_map.get(status)
        )

        # Update institution packages and orders
        institution_courier_package_ids = instance.institution_courier_package.all().values_list('id', flat=True)
        InstitutionPackage.objects.filter(
            id__in=institution_courier_package_ids
        ).update(
            status=_update_institution_package_status_map.get(status),
        )
        Order.objects.filter(institution_related_orders__in=institution_courier_package_ids).update(
            status=_order_status_map.get(status)
        )
        return super().update(instance, validated_data)


class InstitutionPackageUpdateSerializer(UpdateLogMixin, serializers.ModelSerializer):

    class Meta:
        model = InstitutionPackage
        fields = ('id', 'status', 'files', 'comment')

    def create(self, data):
        raise Exception('Not allowed')

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        instance.related_orders.update(status=status)
        _order_status_map = {
            InstitutionPackage.Status.PENDING.value: Order.Status.PENDING.value,
            InstitutionPackage.Status.IN_TRANSIT.value: Order.Status.IN_TRANSIT.value,
            InstitutionPackage.Status.ISSUE.value: Order.Status.PENDING.value,
            InstitutionPackage.Status.DELIVERED.value: Order.Status.COMPLETED.value,
        }
        Order.objects.filter(
            order_code__in=instance.related_orders.all().values_list('order_code', flat=True)
        ).update(status=_order_status_map.get(status))
        return super().update(instance, validated_data)
