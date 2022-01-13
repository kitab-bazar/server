from rest_framework import serializers

from apps.institution.models import Institution


class InstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = (
            'name', 'email', 'municipality', 'ward_number',
            'local_address', 'pan_number', 'vat_number'
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs
