from rest_framework import serializers

from apps.helpdesk.models import Faq, ContactMessage


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = (
            # Model fields
            'id',

            # English fields
            'question_en', 'answer_en',

            # Nepali fields
            'question_ne', 'answer_ne',
        )


class ContactMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        fields = '__all__'
