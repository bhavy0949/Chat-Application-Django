from rest_framework import serializers
from .models import Users
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate



#Serializer for the user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    #One user can register with only one email
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(Users.objects.all())]
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password],
        style = {"input_type" : "password"}
    )
    verify_password = serializers.CharField(#For re-verifying the password
       write_only = True, 
       required = True, 
       style = {"input_type" : "password"})

    class Meta:
        model = Users
        fields = ('username', 'email', 'password', 'verify_password', 'contact_number', 'birth_date')

    def validate(self, attrs):
        if attrs['password'] != attrs['verify_password']:
            raise serializers.ValidationError({"password ": "password fields didn't match"})
        return attrs
    
    def create(self, validated_data):
        user = Users.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            contact_number = validated_data.get('contact_number'),
            birth_date = validated_data.get('birth_date')
        )

        
        return user

def authenticate_user(username, password):
    if username:
        user = authenticate(username= username, password = password)
    else:
        return None
    
    return user


#Serializer for the login
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required= False)
    password = serializers.CharField(style= {'input_type' : 'password'})

    class Meta:
        model = Users
        fields = ('username', 'password')
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        #username is required
        if not (username):
            raise serializers.ValidationError(
                {"message" : "Username is required!!"}
            )

        user = authenticate_user(username, password)
        
        if user is None:
            raise serializers.ValidationError(
                {"message" : "Invalid Credentials", "access_token" : None}
            )
    
        attrs['access_token'] = user.get_tokens_for_user()
        user.is_online = True
        user.save()
        return attrs



