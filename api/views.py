from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import Users
from rest_framework_simplejwt.authentication import JWTAuthentication
from .helpers import calculate_similarity
import json

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    '''
        A classic registration view with all the required fields. 
    '''
    permission_classes = (AllowAny,)
    queryset = Users.objects.all()
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, format='json'):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'message' : 'User Registered Successfully!',
                'response_data' : serializer.data
            }
            if user:
                return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    

class UserLoginView(generics.GenericAPIView):
    
    
    '''Note - After the login, the generated access-token needs to be stored locally on the frontend. 
       It is a Bearer token genereated by the DRF's simple JWT, so it is stateless. In order to log the user out,
       the token need to be sent as a header, so it's better to store the token somewhere.This way the expiry for
       the access token can be checked on the clientside as well.
    '''
    
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer


    def post(self, request, format='json'):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data.get('access_token')    

            if access_token:
                return Response(
                    {"message" : "Login Successful!", "access_token" : access_token},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class UserLogoutView(APIView):
    
    ''' Note : The token stored locally in the frontend is used to log the user out and set the is_online value to
        False. For this, the frontend need to send a POST request to this logout view with an authorization header.

        Header - 

        {Authorization : Bearer accesstokenvalue}

        After successful logout, remove the token from the local storage in the frontend.
    
    '''
    
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
   
    def post(self, request, *args, **kwargs):
        user_obj = request.user
        if user_obj:
            user_obj.is_online = False
            user_obj.save()
            return Response({
                "message" : "Logout successful!!"
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                "message" : "User Not Found!!"
            }, status=status.HTTP_400_BAD_REQUEST)
        

class FriendsRecommendationView(generics.RetrieveAPIView):
    '''
        A view to retrieve five recommended friends for the target user. These recommendations are based on the 
        similarities between users' interests. Based on these interests, a similarity score is calculated between
        the target user and other users. The five users with highest similarity score are recommended.
    '''
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']

        with open('users.json', 'r') as file:
            data = json.load(file)

        friends_recommended = []
        target_user = data["users"][user_id-1]
        target_interests = set(target_user["interests"])


        for user in data["users"]:
            if user not in friends_recommended and user!=target_user:
                user_interests = set(user["interests"])
                if not target_interests.isdisjoint(user_interests):
                    similarity = calculate_similarity(target_user, user)
                    friends_recommended.append({"user" : user, "similarity" : similarity})

        friends_recommended.sort(key=lambda x:x['similarity'], reverse=True)

        if len(friends_recommended)!=0:
            return Response(
                {
                    "message" : "Found recommendations!!",
                    "Recommended users" : friends_recommended[:5],
                },status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    "message" : "No Interest found!!",
                },status=status.HTTP_200_OK
            )
