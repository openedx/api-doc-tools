"""
REST API serializers for reading and writing to the edX Hedgehog Database.
"""
from __future__ import absolute_import, unicode_literals

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

    def get_weight_ounces(self, obj):
        """
        Convert the hedgehog's (`obj`) weight from grams (int) to ounces (float).

        TODO:
            In Python 2, there is no easy way of telling drf-yasg that this method
            returns a `float`, so it assumes that `weight_ounces` is a string field.
            For those that don't need to support Python 2, however, this method could
            have been defined as:

                def get_weight_ounces(self, obj) -> float:

            which would correctly mark `weight_ounces` as a numeric field in the schema.
        """
        return obj.weight_grams * 28.3495
