from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Deposit, RVM


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'phone_number']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}


class DepositSerializer(serializers.ModelSerializer):
    machine_id = serializers.CharField(write_only=True)
    points_earned = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Deposit
        fields = ['material_type', 'weight_kg', 'machine_id', 'points_earned', 'deposited_at']
        read_only_fields = ['points_earned', 'deposited_at']
    
    def validate_machine_id(self, value):
        try:
            rvm = RVM.objects.get(machine_id=value, is_active=True)
            return rvm
        except RVM.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive machine ID")
    
    def validate_weight_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be positive")
        if value > 100:  # Reasonable upper limit
            raise serializers.ValidationError("Weight seems too high")
        return value
    
    def create(self, validated_data):
        rvm = validated_data.pop('machine_id')
        validated_data['rvm'] = rvm
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserSummarySerializer(serializers.ModelSerializer):
    recent_deposits = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['username', 'total_points', 'total_weight_recycled', 'recent_deposits']
    
    def get_recent_deposits(self, obj):
        recent = obj.deposits.all()[:5]
        return DepositSerializer(recent, many=True).data