from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ["user", "title", "description", "created", "complete"]


# from collections import UserDict
# from rest_framework import serializers

# class CustomTokenObtainPairSerializer(serializers.Serializer):
#     username_field = UserDict.USERNAME_FIELD

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields[self.username_field] = serializers.CharField()
#         self.fields['password'] = serializers.CharField(write_only=True)

# # class CustomTokenObtainPairView(TokenObtainPairView):
# #     serializer_class = CustomTokenObtainPairSerializer