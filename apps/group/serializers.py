from rest_framework import serializers

from .models import PosmComponentPermission


class PosmComponentPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosmComponentPermission
        fields = '__all__'
