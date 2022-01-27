from rest_framework import serializers
from apps.notification.models import Notification


class ToggleNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'read', ]
