from rest_framework import serializers
from django.core.exceptions import FieldDoesNotExist


def model_has_field(model, field):
    try:
        model._meta.get_field(field)
        return True
    except FieldDoesNotExist:
        return False


class CreatedUpdatedBaseSerializer(serializers.Serializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    updated_by = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_by = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        if model_has_field(self.Meta.model, 'created_by'):
            validated_data['created_by'] = self.context['request'].user
        if model_has_field(self.Meta.model, 'modified_by'):
            validated_data['modified_by'] = self.context['request'].user
        if model_has_field(self.Meta.model, 'modified_by'):
            validated_data['modified_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if model_has_field(self.Meta.model, 'created_by'):
            validated_data['created_by'] = self.context['request'].user
        if model_has_field(self.Meta.model, 'modified_by'):
            validated_data['modified_by'] = self.context['request'].user
        if model_has_field(self.Meta.model, 'modified_by'):
            validated_data['modified_by'] = self.context['request'].user
        return super().update(instance, validated_data)


class IntegerIDField(serializers.IntegerField):
    """
    This field is created to override the graphene conversion of the integerfield -> graphene.ID
    check out utils/graphene/mutation.py
    """
    pass


def IdListField(**args):
    return serializers.ListField(child=IntegerIDField(**args), default=list, allow_empty=True,)
