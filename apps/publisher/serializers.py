from rest_framework import serializers

from apps.publisher.models import Publisher


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = (
            'id', 'name', 'municipality', 'ward_number',
            'local_address', 'pan_number', 'vat_number'
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs


class PublisherUpdateSerializer(serializers.ModelSerializer):
    '''
    This is used to update user profile only
    '''
    class Meta:
        model = Publisher
        fields = (
            'id', 'name', 'municipality', 'ward_number', 'local_address'
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs
