from rest_framework import serializers
from voting.models import Voter
from django.contrib.auth.hashers import make_password


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id', 'university_id', 'phone_number',
                  'user', 'gender', 'date_of_birth']

    def validate_university_id(self, value):
        """
        Check that the university_id is unique
        """
        if self.instance is None and Voter.objects.filter(university_id=value).exists():
            raise serializers.ValidationError(
                "Student With University ID already exists.")
        return value

    def validate_phone_number(self, value):
        """
        Check that the phone_number is unique
        """
        if self.instance is None and Voter.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with Phone number already exists.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(VoterSerializer, self).create(validated_data)
