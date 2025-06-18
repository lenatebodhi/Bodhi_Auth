from django.urls import path
from api.v1 import *

app_name = 'api'

urlpatterns = [

    # authorization and authentication
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:user_id>/',UserViews.as_view({
        'patch': 'update',
        'get': 'list'}), name='user-views'),
    path('send-otp/', SendotpView.as_view(), name='send-otp'),
    path('forgot-password-link/', ForgotPassword.as_view(), name='forgot-password'),
    path('reset-password/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('deactivate/', DeactivateAccountView.as_view(), name='deactivate'),
    path('user/interest/values/', InterestsListView.as_view(), name='user-interest-list'),


    #courses
    path('courses-list/', CoursesListView.as_view(), name='courses-list'),
    path('module-list/', ModuleListView.as_view(), name='module-list'),
    path('lesson-list/', LessonListView.as_view(), name='lesson-list'),

    path('courses/create/', CourseCreateView.as_view
         ({
             'post': 'create'
         }), name='course-create'),


    path('courses/<str:object_id>/',CoursesView.as_view
         ({ 'patch': 'update',
            'delete': 'destroy',
            'get': 'retrieve',
         }), name='courses'),

    path('courses-details/create/', CourseDetailCreateView.as_view
         ({
             'post': 'create'
         }), name='course-detail-create'),


    path('courses-details/<str:object_id>/',CoursesDetailsView.as_view
         ({ 'patch': 'update',
            'delete': 'destroy',
            'get': 'retrieve',
         }), name='courses-detail'),

    path('module-create/', ModuleCreateView.as_view
         ({
             'post': 'create'
         }), name='module-create'),

    path('module/<str:object_id>/',ModulesView.as_view
         ({ 'put': 'update',
            'delete': 'destroy',
            'get': 'retrieve',
         }), name='module-details'),

     path('lesson-create/', LessonCreateView.as_view
         ({
             'post': 'create'
         }), name='lesson-create'),


    path('lesson/<str:object_id>/',LessonView.as_view
         ({ 'put': 'update',
            'delete': 'destroy',
            'get': 'retrieve',
         }), name='lesson-details'),



]
