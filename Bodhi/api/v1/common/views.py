from api.v1.common.serializers import *
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken



class InterestsListView(ListAPIView):
    """
      Returns the users under the user_type 'Customer'
    
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = InterestDropdownSerializer
   
 
    def get(self, request, *args, **kwargs):
        try:
            
            queryset = Interest.objects.values("id","title")
            return Response({"results":queryset,
                             "message": "Listed successfully",
                             'status': 'success',
                             "statusCode":HTTP_200_OK}, status=HTTP_200_OK)
        
        except Exception as error_message:
            response_data = {"message": f"Something went wrong : {error_message}",
                            "status": "error",
                            "statusCode": HTTP_500_INTERNAL_SERVER_ERROR}
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)