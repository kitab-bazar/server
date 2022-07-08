from rest_framework import serializers
# from django.utils.translation import gettext_lazy as _

from apps.common.models import ActivityLogFile
from config.serializers import CreatedUpdatedBaseSerializer


class ActivityLogFileSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = ActivityLogFile
        fields = ('type', 'file', )
