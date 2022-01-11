from rest_framework import serializers
from django.utils.translation import ugettext as _

from apps.school.models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'

        def validate(self, data):
            province = data['province']
            district = data['district']
            municipality = data['municipality']

            if district.province != province:
                raise serializers.ValidationError(_('District should be under province'))

            if municipality.district != province:
                raise serializers.ValidationError(_('Municipality should be under district'))
