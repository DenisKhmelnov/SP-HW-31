from rest_framework import serializers

from ads.models import Ad, Category, Selection
from ads.validators import not_null
from users.models import User


class AdSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[not_null])
    class Meta:
        model = Ad
        fields = "__all__"


class AdListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    locations = serializers.SerializerMethodField()

    def get_locations(self, ad):
        return [loc.name for loc in ad.author.locations.all()]

    class Meta:
        model = Ad
        fields = "__all__"


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = "__all__"


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection


class SelectionDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    items = AdListSerializer(many=True)

    class Meta:
        model = Selection
        fields = ["__all__"]
