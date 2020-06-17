"""
REST API serializers for reading and writing to the edX Hedgehog Database.
"""

from rest_framework import serializers


# pylint: disable=abstract-method


class HedgehogSerializer(serializers.Serializer):
    """
    Serializer for a hedgehog.
    """
    uuid = serializers.UUIDField()
    key = serializers.SlugField()
    name = serializers.CharField()
    weight_grams = serializers.IntegerField()
    weight_ounces = serializers.SerializerMethodField()
    fav_food = serializers.ChoiceField(
        [
            ('critters', 'Critters'),
            ('crawlies', 'Crawly things'),
            ('strawberries', 'Strawberries'),
        ],
        allow_blank=True,
        source='favorite_food',
    )
    is_college_graduate = serializers.BooleanField(default=False)

    def get_weight_ounces(self, obj) -> float:
        """
        Convert the hedgehog's (`obj`) weight from grams (int) to ounces (float).
        """
        return obj.weight_grams * 28.3495
