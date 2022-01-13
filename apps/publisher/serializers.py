from rest_framework import serializers

from apps.publisher.models import Publisher


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = (
            'id', 'name', 'email', 'municipality', 'ward_number',
            'local_address', 'pan_number', 'vat_number'
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs
