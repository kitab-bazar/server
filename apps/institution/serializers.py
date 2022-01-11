from rest_framework import serializers
from django.utils.translation import ugettext as _

from apps.institution.models import Institution


class InstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = '__all__'

    def validate(self, data):
        province = data['province']
        district = data['district']
        municipality = data['municipality']

        if district.province != province:
            raise serializers.ValidationError(_('District should be under province'))

        if municipality.district != province:
            raise serializers.ValidationError(_('Municipality should be under district'))
