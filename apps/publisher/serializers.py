from apps.publisher.models import Publisher
from rest_framework import serializers


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = '__all__'
