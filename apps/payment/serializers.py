from rest_framework import serializers

from apps.payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ('created_by', 'modified_by',)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['modified_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['modified_by'] = self.context['request'].user
        return super().update(validated_data)
