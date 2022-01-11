
# import rest Apis
from rest_framework import serializers

# import product modules
from catalogue.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'