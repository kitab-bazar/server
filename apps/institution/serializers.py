from rest_framework import serializers

from apps.institution.models import Institution


class InstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = (
            'name', 'municipality', 'ward_number',
            'local_address', 'pan_number', 'vat_number'
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs


class InstitutionUpdateSerializer(serializers.ModelSerializer):
    '''
    This is used to update user profile only
    '''
    class Meta:
        model = Institution
        fields = (
            'name', 'municipality', 'ward_number', 'local_address',
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs
