from rest_framework import serializers

from apps.school.models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'
