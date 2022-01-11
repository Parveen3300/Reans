
from rest_framework import serializers
from customer.models import CustomerProfile



class CustomerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = "__all__"