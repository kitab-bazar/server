from rest_framework import serializers

from apps.school.models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            'id', 'name', 'municipality', 'ward_number',
            'local_address', 'pan_number', 'vat_number'
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs
