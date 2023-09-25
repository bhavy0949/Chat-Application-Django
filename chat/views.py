from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from api.models import Users
from .serializers import OnlineUsersSerializer
from rest_framework.permissions import IsAuthenticated



class OnlineUsersView(ListAPIView):
    '''
        A view to list all the online users and their channel names. This can only be accessed by authenticated users.
        So the access token must be included in the header for this to return success. As usual the field for the header
        in the request is 'Authorization' : Bearer access_tokenvalue
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineUsersSerializer

    def get_queryset(self):
        return Users.objects.filter(is_online=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'message': 'Online users fetched successfully',
            'data': serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)




