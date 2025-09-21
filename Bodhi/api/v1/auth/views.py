from api.tasks import *
from api.v1.auth.serializers import *
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
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
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
from utils.functions import *
from django.db.models import Q


class SignUpView(generics.CreateAPIView):
    """
    This API view is used for user registration (sign up).
    """

    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JSONRenderer,)
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Hash the password before saving the user
            password = serializer.validated_data.pop("password")
            serializer.validated_data["password"] = make_password(password)
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Registered Successfully",
                    "data": serializer.data,
                    "status": "success",
                    "status_code": HTTP_200_OK,
                },
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e), "status": "error", "status_code": HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save()


class SendotpView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        username = request.data["username"]

        # Check if the input is an email
        if is_email(username):
            print(is_email(username))
            print("a1")
            user = User.objects.get(email=username)
            otp = generate_otp()
            user.otp = otp
            user.save()
            subject = f"VERIFICATION CODE"
            message = f"Dear {username}, Your verification code {otp} ."
            send_email.delay(subject, message, username)

        else:
            print("a2")

            # Start the verification process
            # client = Client(TWILO_ACCOUNT_SID, TWILO_ACCESS_TOKEN)
            # verification = client.verify \
            #     .services('VA8cb9f32f11d414fd4a57b59709d91e02') \
            #     .verifications \
            #     .create(to=username, channel='sms')
            # print(verification)

        return Response({"message": "OTP sent successfully."})


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        login_type = request.data["login_type"]
        if login_type == "PASSWORD":
            username = request.data["username"]
            password = request.data["password"]

            # Try to find a user that matches the entered username (either email or phone number)
            try:
                user = User.objects.get(Q(phone=username) | Q(email=username))
            except User.DoesNotExist:
                return Response(
                    {"message": "Invalid login credentials.", "status": "error", "status_code": HTTP_401_UNAUTHORIZED},
                    status=HTTP_401_UNAUTHORIZED,
                )

            if user.check_password(password):
                login(request, user)
                setattr(user, "is_active", True)
                user.save()
                refresh = RefreshToken.for_user(user)
                token = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(
                    {
                        "message": "You have logged in successfully.",
                        "status": "success",
                        "status_code": HTTP_200_OK,
                        "token": token,
                    }
                )

            else:
                return Response(
                    {"message": "Invalid login credentials.", "status": "error", "status_code": HTTP_401_UNAUTHORIZED},
                    status=HTTP_401_UNAUTHORIZED,
                )

        elif login_type == "OTP":
            entered_otp = request.data["otp"]
            username = request.data["username"]
            print(entered_otp, username)

            if is_email(username):
                try:
                    user = User.objects.get(email=username, otp=entered_otp)
                except User.DoesNotExist:
                    return Response(
                        {"message": "User not found.", "status": "error", "status_code": HTTP_404_NOT_FOUND},
                        status=HTTP_404_NOT_FOUND,
                    )
                login(request, user)

                refresh = RefreshToken.for_user(user)
                token = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }

                setattr(user, "otp", None)
                setattr(user, "is_active", True)
                user.save()

                return Response(
                    {
                        "message": "You have logged in successfully.",
                        "status": "success",
                        "status_code": HTTP_200_OK,
                        "token": token,
                    }
                )

            else:
                # Check the verification process
                client = Client(TWILO_ACCOUNT_SID, TWILO_ACCESS_TOKEN)

                try:
                    check = client.verify.services(TWILO_SERVICE_ID).verification_checks.create(
                        to=username, code=entered_otp
                    )

                except Exception as e:
                    return Response(
                        {
                            "message": f"Failed to verify OTP: {str(e)}",
                            "status": "error",
                            "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
                        },
                        status=HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                if check.status == "approved":
                    try:
                        user = User.objects.get(phone=username)
                    except User.DoesNotExist:
                        return Response(
                            {"message": "User not found.", "status": "error", "status_code": HTTP_404_NOT_FOUND},
                            status=HTTP_404_NOT_FOUND,
                        )
                    login(request, user)

                    refresh = RefreshToken.for_user(user)
                    token = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(
                        {
                            "message": "You have logged in successfully.",
                            "status": "success",
                            "status_code": HTTP_200_OK,
                            "token": token,
                        }
                    )

                else:
                    return Response(
                        {"message": "Incorrect OTP.", "status": "error", "status_code": HTTP_404_NOT_FOUND},
                        status=HTTP_404_NOT_FOUND,
                    )


# class LoginView(APIView):
#     authentication_classes = ()
#     permission_classes = ()
#     renderer_classes = (JSONRenderer, )

#     def post(self, request):
#         email = request.data.get('email')
#         phone_number = request.data.get('phone_number')
#         login_type = request.data.get('login_type')
#         password = request.data.get('password')
#         otp = request.data.get('otp')

#         if login_type == 'PASSWORD':
#             if not (email or phone_number):
#                 return Response({'message': 'Either email or phone number is required'}, status=HTTP_400_BAD_REQUEST)

#             print("hi")
#             print(email)
#             if email:
#                 print("hi2")
#                 # user = self.authenticate_with_email(email, password)
#                 user = authenticate(request,email=email, password=password)
#                 print("hi4")
#             elif phone_number:
#                 user = self.authenticate_with_phone(phone_number, password)

#             else:
#                 return Response({'message': 'Either email or phone number is required'}, status=HTTP_400_BAD_REQUEST)

#             if user is None:
#                 return Response({'message': 'Invalid email/phone number or password'}, status=HTTP_401_UNAUTHORIZED)

#         elif login_type == 'OTP':
#             if not (email or phone_number):
#                 return Response({'message': 'Either email or phone number is required for OTP login'}, status=HTTP_400_BAD_REQUEST)
#             if email:
#                 user = User.objects.filter(email=email).first()
#             else:
#                 user = User.objects.filter(phone_number=phone_number).first()

#             if not user:
#                 return Response({'message': 'User not found'}, status=HTTP_404_NOT_FOUND)


#         # Check the password
#         if user.check_password(password):
#             refresh = RefreshToken.for_user(user)
#             token = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }

#         user.is_active = True
#         user.save()

#         # Return user details or token if using JWT
#         # Replace this with your actual token generation logic
#         return Response({'message': 'User signed up successfully', 'user_id': user.id,'token':token}, status=HTTP_200_OK)


#     # def authenticate_with_email(self,email, password):
#     #     print("hi3")
#     #     print(email, password)
#     #     # Authenticate user with email and password
#     #     return authenticate(email=email, password=password)

#     def authenticate_with_phone(self, phone_number, password):
#         # Authenticate user with phone number and password
#         user = User.objects.filter(phone_number=phone_number).first()
#         if user and user.check_password(password):
#             return user
#         return None


class UserViews(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UsersViewsSerializer
    queryset = User.objects.filter(is_active=1)

    def list(self, request, *args, **kwargs):
        """
        Lists the user views for a specific user.
        """
        try:
            query = self.get_queryset().filter(id=kwargs["user_id"])
            message = "listed successfully"
            serializer_class = self.serializer_class(query, many=True)
            return Response(
                {"message": message, "results": serializer_class.data, "status": "success", "status_code": HTTP_200_OK},
                status=200,
            )

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Updates a specific user view.
        """

        try:
            instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("user_id"))
            interests_data = request.data.pop("interests", None)

            serializer = self.serializer_class(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Update interests separately
            if interests_data is not None:
                instance.interests.set(interests_data)

            serializer.save()
            message = "updated successfully"
            return Response({"message": message, "data": serializer.data}, status=200)

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPassword(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):

        username = request.data.get("username")
        if is_email(username):

            if not username:
                return Response(
                    {
                        "message": "Please provide an email address",
                        "status": "error",
                        "status_code": HTTP_400_BAD_REQUEST,
                    },
                    status=HTTP_400_BAD_REQUEST,
                )

            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return Response(
                    {
                        "message": "User with that email address does not exist",
                        "status": "error",
                        "status_code": HTTP_404_NOT_FOUND,
                    },
                    status=HTTP_404_NOT_FOUND,
                )

            otp = generate_otp()
            user.otp = otp
            user.save()

            send_email.delay(
                "Reset your password",
                f" The otp is {otp}",
                username,
            )
            return Response(
                {
                    "message": "OTP has been sent to your registered email address.",
                    "status": "success",
                    "status_code": HTTP_200_OK,
                }
            )

        else:

            print("hi3")
            try:
                user = User.objects.get(phone=username)
            except User.DoesNotExist:
                return Response({"message": "User with this phone does not exist"}, status=HTTP_400_BAD_REQUEST)

            # Start the verification process
            # client = Client(account_sid, auth_token)
            # verification = client.verify \
            #     .services('VA8cb9f32f11d414fd4a57b59709d91e02') \
            #     .verifications \
            #     .create(to=username, channel='sms')
            # print(verification)

            return Response({"message": "OTP sent successfully."})


class CustomPasswordResetConfirmView(APIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        try:
            username = request.data["username"]
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():

                try:
                    user = User.objects.get(Q(phone=username) | Q(email=username))

                except User.DoesNotExist:
                    return Response(
                        {
                            "message": "User with that email address does not exist",
                            "status": "error",
                            "status_code": HTTP_404_NOT_FOUND,
                        },
                        status=HTTP_404_NOT_FOUND,
                    )

                # Set the user's password to the new password and save
                user.password = make_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"message": "Password reset successfully", "status": "success", "status_code": HTTP_200_OK}
                )

            else:
                return Response(
                    {
                        "results": serializer.errors,
                        "message": "Something went wrong",
                        "status": "error",
                        "status_code": HTTP_400_BAD_REQUEST,
                    },
                    status=HTTP_400_BAD_REQUEST,
                )

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"message": "Your account has been deactivated.", "status": "success", "status_code": HTTP_200_OK},
            status=HTTP_200_OK,
        )
