import re

from accounts.models import User
from api.v1.common.serializers import *
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "user_role", "phone", "first_name", "last_name", "get_full_name")

    def validate(self, data):
        # password validation
        password = data.get("password")
        if password:
            if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})", password):
                raise serializers.ValidationError(
                    {
                        "message": "Password must have minimum 8 characters, alphanumeric with at least one uppercase, one lowercase and one special character."
                    }
                )

        # email and phone validation
        email = data.get("email")
        phone = data.get("phone")
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "This email already exists!"})
        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"message": "This phone number already exists!"})

        return data


from django.db import transaction


class UsersViewsSerializer(serializers.ModelSerializer):

    # Same as before
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.filter(is_active=1), message="This email already exists!")]
    )
    phone = serializers.IntegerField(
        required=False,
        validators=[
            UniqueValidator(queryset=User.objects.filter(is_active=1), message="This phone number already exists!")
        ],
    )

    interests = InterestDropdownSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)
    qualifications = QualificationSerializer(many=True, required=False)
    achievements = AchievementsSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "user_role",
            "phone",
            "first_name",
            "last_name",
            "get_full_name",
            "middle_name",
            "website",
            "interests",
            "educations",
            "qualifications",
            "achievements",
        )

    from django.db import transaction

    def update(self, instance, validated_data):
        # Extract nested data
        educations = validated_data.pop("educations", [])
        qualifications = validated_data.pop("qualifications", [])
        achievements = validated_data.pop("achievements", [])
        interests = validated_data.pop("interests", None)

        with transaction.atomic():
            # Update scalar fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Update M2M
            if interests is not None:
                instance.interests.set(interests)

            # Sync nested relationships
            self._sync_nested(instance, Education, educations, "educations")
            self._sync_nested(instance, Qualification, qualifications, "qualifications")
            self._sync_nested(instance, Achievements, achievements, "achievements")

        return instance

    def _sync_nested(self, user, model, payload, related_name):
        existing = {obj.id: obj for obj in getattr(user, related_name).all()}
        incoming_ids = []

        for item in payload:
            obj_id = item.get("id")
            if obj_id and obj_id in existing:
                obj = existing[obj_id]
                for attr, val in item.items():
                    if attr != "id":
                        setattr(obj, attr, val)
                obj.save()
                incoming_ids.append(obj_id)
            elif obj_id and obj_id not in existing:
                raise serializers.ValidationError(f"{model.__name__} with ID {obj_id} not found for this user.")
            else:
                new = model.objects.create(user=user, **item)
                incoming_ids.append(new.id)

        # Delete removed ones
        for obj in existing.values():
            if obj.id not in incoming_ids:
                obj.delete()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        validators=[
            RegexValidator(
                regex=("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})"),
                message="Password must have minimum 8 characters, alphanumeric with at least one uppercase, one lowercase and one special character.",
                code="invalid_password",
            )
        ],
    )
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"message": "Passwords do not match."})
        return data
