from rest_framework import serializers

from apps.school.models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            'id', 'name', 'municipality', 'ward_number',
            'local_address', 'pan_number', 'vat_number', 'school_id'
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs


class SchoolUpdateSerializer(serializers.ModelSerializer):
    '''
    This is used to update user profile only
    '''
    class Meta:
        model = School
        fields = (
            'id', 'name', 'municipality', 'ward_number', 'local_address', 'school_id'
        )

    def validate(self, attrs):
        municipality = attrs['municipality']
        attrs['district'] = municipality.district
        attrs['province'] = municipality.province
        return attrs
