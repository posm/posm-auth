from rest_framework import serializers

from .models import PosmComponentPermission, User


class PosmComponentPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosmComponentPermission
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='profile.get_display_name')
    allowed_posm_components = PosmComponentPermissionSerializer(
        source='profile.get_allowed_posm_components', many=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'display_name', 'allowed_posm_components')
