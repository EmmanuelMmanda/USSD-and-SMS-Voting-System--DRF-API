from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from voting.models import Settings
from voting.serializers.SettingsSerializer import SettingsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class SettingsView(APIView):
    permission_classes = [AllowAny]
    # get all user settings

    def get(self, request, format=None):
        settings = Settings.objects.all()
        serializer = SettingsSerializer(settings, many=True)
        return Response(serializer.data)

    # create a new user setting
    def post(self, request, format=None):
        serializer = SettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SettingsDetailView(APIView):
    permission_classes = [AllowAny]


    def get_object(self, pk):
        try:
            return Settings.objects.get(pk=pk)
        except Settings.DoesNotExist:
            raise Http404

    def get(self, request, setting_id, format=None):
        setting = self.get_object(setting_id)
        serializer = SettingsSerializer(setting)
        return Response(serializer.data)

    def put(self, request, setting_id, format=None):
        setting = self.get_object(setting_id)
        serializer = SettingsSerializer(setting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, setting_id, format=None):
        setting = self.get_object(setting_id)
        setting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # patch requests
    def patch(self, request, setting_id, format=None):
        setting = self.get_object(setting_id)
        serializer = SettingsSerializer(
            setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

    def change_language(self, request, setting_id, language):
        setting = self.get_object(setting_id)
        if not setting:
            #create a default setting for user language == en
            return Response(
                {"error": "Setting does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SettingsSerializer(setting, data={"language": language}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    #add a new setting for a user given user id and the language to EN
    def addDefaultLang(self, request, user_id, format=None):
        serializer = SettingsSerializer(data={"user": user_id, "language": "EN"})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    


class getSeetingsByUser(APIView):
    #get settings of A PARTICULAR USER
    permission_classes = [AllowAny]

    def get(self, request, user_id, format=None):
        settings = Settings.objects.filter(user=user_id)
        serializer = SettingsSerializer(settings, many=True)
        return Response(serializer.data)
    
    #patch settings of A PARTICULAR USER
    def patch(self, request, user_id, format=None):
        settings = Settings.objects.get(user=user_id)
        serializer = SettingsSerializer(
            settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )