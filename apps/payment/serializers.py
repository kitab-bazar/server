from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.payment.models import Payment, PaymentLog
from config.serializers import CreatedUpdatedBaseSerializer


class PaymentLogSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = PaymentLog
        fields = ('comment', 'files')

    def validate_files(self, files):
        for file in files:
            if self.context['request'].user != file.created_by:
                raise serializers.ValidationError(_('Invalid file'))
        return files


class PaymentSnapshotSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('status',)


class PaymentSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):
    payment_log = PaymentLogSerializer(required=False)

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        payment_log_data = validated_data.pop('payment_log', None)
        payment = super().create(validated_data)
        snapshot_serializer = PaymentSnapshotSerializer(instance=payment)
        if payment_log_data:
            files = payment_log_data.pop('files', None)
            payment_log = PaymentLog.objects.create(
                payment=payment,
                snapshot=snapshot_serializer.data,
                **payment_log_data,
                created_by=self.context['request'].user
            )
            if files:
                payment_log.add(*files)
        return payment
