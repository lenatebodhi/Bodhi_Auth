from api.filters.course_filters import *
from api.v1.courses.serializers import *
from courses.models import *
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
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from utils.paginator import CustomPagination


class CoursesListView(ListAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Courses.objects.filter(is_active=1, is_delete=0).order_by("-id")
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ModuleListView(ListAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ModuleDeatilSerializer
    pagination_class = CustomPagination
    filterset_class = ModuleFilter

    def get_queryset(self):
        queryset = Module.objects.filter(is_active=True, is_deleted=False).order_by("-id")
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class LessonListView(ListAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = LessonDetailSerializer
    pagination_class = CustomPagination
    filterset_class = LessonFilter

    def get_queryset(self):
        queryset = Courses.objects.filter(is_active=1).order_by("-id")
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class CoursesView(viewsets.GenericViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Courses.objects.filter(
            is_active=1,
            is_deleted=0,
        ).order_by("-id")
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))

        instance.is_deleted = True
        instance.is_active = False
        instance.save()
        message = "Deleted successfully"
        return Response({"message": message, "status": "success", "status_code": HTTP_200_OK}, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))
        serializer = CourseCreateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = "updated successfully"
        return Response({"message": message, "status": "success", "status_code": HTTP_200_OK}, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """ """
        try:
            instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))
            serializer = self.serializer_class(instance)
            message = "Detail Page view Listed successfully"
            return Response({"results": serializer.data, "message": message}, status=HTTP_200_OK)

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class CourseCreateView(viewsets.GenericViewSet):
    """ """

    permission_classes = ()
    authentication_classes = ()
    serializer_class = CourseCreateSerializer
    queryset = Courses.objects.filter(is_deleted=0, is_active=1)

    def create(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Created successfully", "status": "success", "status_code": HTTP_201_CREATED},
                status=HTTP_201_CREATED,
            )

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class CourseDetailCreateView(viewsets.GenericViewSet):
    """ """

    permission_classes = ()
    authentication_classes = ()
    serializer_class = CourseDetailsCreateSerializer
    queryset = CourseDetails.objects.filter(is_deleted=0, is_active=1)

    def create(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Created successfully", "status": "success", "status_code": HTTP_201_CREATED},
                status=HTTP_201_CREATED,
            )

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class CoursesDetailsView(viewsets.GenericViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CourseDetailsSerializer

    def get_queryset(self):
        queryset = CourseDetails.objects.filter(
            is_active=1,
            is_deleted=0,
        ).order_by("-id")
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))

        instance.is_deleted = True
        instance.is_active = False
        instance.save()
        message = "Deleted successfully"
        return Response({"message": message, "status": "success", "status_code": HTTP_200_OK}, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))
        serializer = CourseCreateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = "updated successfully"
        return Response({"message": message, "status": "success", "status_code": HTTP_200_OK}, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """ """
        try:
            instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))
            serializer = self.serializer_class(instance)
            message = "Detail Page view Listed successfully"
            return Response({"results": serializer.data, "message": message}, status=HTTP_200_OK)

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ModuleCreateView(viewsets.GenericViewSet):
    """ """

    permission_classes = ()
    authentication_classes = ()
    serializer_class = ModuleCreateSerializer
    queryset = Module.objects.filter(is_deleted=0, is_active=1)

    def create(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Created successfully", "status": "success", "status_code": HTTP_201_CREATED},
                status=HTTP_201_CREATED,
            )

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ModulesView(viewsets.GenericViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ModuleDeatilSerializer

    def get_queryset(self):
        queryset = Module.objects.filter(
            is_active=1,
            is_deleted=0,
        ).order_by("-id")
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))

        instance.is_deleted = True
        instance.is_active = False
        instance.save()
        message = "Deleted successfully"
        return Response({"message": message, "status": "success", "status_code": HTTP_200_OK}, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))
        serializer = CourseCreateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = "updated successfully"
        return Response({"message": message, "status": "success", "status_code": HTTP_200_OK}, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """ """
        try:
            instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))
            serializer = self.serializer_class(instance)
            message = "Detail Page view Listed successfully"
            return Response({"results": serializer.data, "message": message}, status=HTTP_200_OK)

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class LessonCreateView(viewsets.GenericViewSet):
    """ """

    permission_classes = ()
    authentication_classes = ()
    serializer_class = LessonCreateSerializer
    queryset = Lesson.objects.filter(is_deleted=0, is_active=1)

    def create(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Created successfully", "status": "success", "status_code": HTTP_201_CREATED},
                status=HTTP_201_CREATED,
            )

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class LessonView(viewsets.GenericViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = LessonDetailSerializer

    def get_queryset(self):
        queryset = Lesson.objects.filter(
            is_active=1,
            is_deleted=0,
        ).order_by("-id")
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))

        instance.is_deleted = True
        instance.is_active = False
        instance.save()
        message = "Deleted successfully"
        return Response({"message": message, "status": "success", "status_code": HTTP_200_OK}, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))
        serializer = LessonCreateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = "updated successfully"
        return Response({"message": message, "status": "success", "status_code": HTTP_200_OK}, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """ """
        try:
            instance = get_object_or_404(self.get_queryset(), object_id=kwargs.get("object_id"))
            serializer = self.serializer_class(instance)
            message = "Detail Page view Listed successfully"
            return Response({"results": serializer.data, "message": message}, status=HTTP_200_OK)

        except Exception as error_message:
            response_data = {
                "message": f"Something went wrong: {error_message}",
                "status": "error",
                "statusCode": HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)
