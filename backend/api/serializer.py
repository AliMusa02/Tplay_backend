from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from teams.models import Teams, TeamMember
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def get_token(self, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['user_name'] = user.user_name

        return token

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)


# class SimpleTeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teams
#         fields = ['id', 'team_name', 'team_logo']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ["id", "team_name", 'team_logo', 'captain']


class UserSerializer(serializers.ModelSerializer):
    # team = TeamSerializer(read_only=True)
    team = serializers.SerializerMethodField()

    # profilePic = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "email", "user_name", "first_name", 'password',
                  "about", "profilePic", 'team']
        extra_kwargs = {"password": {"write_only": True}}

        def validate(self, attrs):
            user = self.instance
        # Validate unique user_name if changed
            if 'user_name' in attrs and attrs['user_name'] != user.user_name:
                if User.objects.filter(user_name=attrs['user_name']).exists():
                    raise serializers.ValidationError(
                        {'user_name': 'This user name is already taken.'})

        # Validate unique email if changed
            if 'email' in attrs and attrs['email'] != user.email:
                if User.objects.filter(email=attrs['email']).exists():
                    raise serializers.ValidationError(
                        {'email': 'This email is already registered.'})

            return attrs

        def update(self, instance, validated_data):
            password = validated_data.pop('password', None)

            # Update normal fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            # Set password securely
            if password:
                instance.set_password(password)

            instance.save()
            return instance

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    # def validate_password(self, value):
    #     try:
    #         validate_password(value)
    #     except DjangoValidationError as e:
    #         raise DRFValidationError({"password": e.messages})
    #     return value
    def validate_password(self, value):
        validate_password(value)
        return value

    def get_team(self, obj):
        # from teams.serializer import TeamSerializer
        # print(f"Getting team for: {obj.user_name}")

        if hasattr(obj, 'team'):
            print("-> User is a captain")
            return TeamSerializer(obj.team).data

        try:
            member = TeamMember.objects.select_related("team").get(user=obj)
            print("-> User is a player")
            return TeamSerializer(member.team).data
        except TeamMember.DoesNotExist:
            print("-> No team found")
            return None

    # def create(self, validated_data):
    #     if 'profilePic' not in validated_data:
    #         validated_data['profilePic'] = "images/fallback.png"
    #     user = User.objects.create_user(**validated_data)
    #     return user
