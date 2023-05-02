from rest_framework import serializers
from voting.models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'
        read_only_fields = ['id']

    #handle patch requests for the settings based on key, value and user
    def partial_update(self, instance, validated_data):
        instance.key = validated_data.get('key', instance.key)
        instance.value = validated_data.get('value', instance.value)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
