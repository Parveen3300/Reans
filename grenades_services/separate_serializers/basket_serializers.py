"""
BasketSerializers
"""

# import rest Apis
from rest_framework import serializers

# import basket modules
from basket.models import Basket
from basket.models import BasketProductLine

# import Product serializers
from grenades_services.separate_serializers.product import ProductSerializer


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'


class BasketProductSerializer(serializers.ModelSerializer):

    products_list = serializers.SerializerMethodField('get_products_list')

    class Meta:
        model = BasketProductLine
        fields = '__all__'

    def get_products_list(self, obj):
        """
        This 'get_products_list' method used to get the all product list from basket instance
        """
        empty_list = list()
        try:
            if not obj:
                return empty_list
            return (ProductSerializer(obj.product, many=True).data
                    if obj.product else
                    empty_list)

        except Exception as e:
            print('G37')
            print(e)
            return empty_list
            