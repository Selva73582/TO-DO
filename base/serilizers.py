from django.contrib.auth.models import User

from rest_framework import serializers


from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','password2']

        extra_kwargs={
            'password2':{'write_only':True},
        }

    def save(self):
        required_fields = ['username', 'email', 'password', 'password2']

        print(self.validated_data)
        for field in required_fields:
            if field not in self.validated_data:
                raise serializers.ValidationError({field: "This field is required"})
            elif not self.validated_data:
                raise serializers.ValidationError({field: "This field cannot be empty"})
            


        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2 :
            raise serializers.ValidationError({"error":"Password does not match"})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"error":"Email already exists"})
        
        account=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )

        account.set_password(self.validated_data['password'])

        account.save()

        return account
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Both username and password are required")

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return token.key



from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_at', 'due_date', 'priority', 'is_completed')

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()
        return instance





    