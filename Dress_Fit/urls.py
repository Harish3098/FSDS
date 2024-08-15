from django.urls import path, include
from Dress_Fit import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.DRESS_ML, name='DRESS_ML'),


    path('DRESS_ML', views.DRESS_ML, name='DRESS_ML'),

    path('DRESS_OVER', views.DRESS_OVER, name='DRESS_OVER'),

    path('AdminLogin', views.AdminLogin, name='AdminLogin'),
    path('DRESS_OVER2', views.DRESS_OVER2, name='DRESS_OVER2'),
    path('', views.index, name='index'),




    path('login/', auth_views.LoginView.as_view(
        template_name='Dress_Fit/login.html'
    ),
         name='login'
         ),

    path('adminLogin/', auth_views.LoginView.as_view(
        template_name='Dress_Fit/adminLogin.html'
    ),
         name='adminLogin'
         ),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ),
         name='logout'
         ),

    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='Dress_Fit/change-password.html',
            success_url='/'
        ),
        name='change-password'
    ),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='Dress_Fit/password-reset/password_reset.html',
             subject_template_name='Dress_Fit/password-reset/password_reset_subject.txt',
             email_template_name='Dress_Fit/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='Dress_Fit/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='Dress_Fit/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='Dress_Fit/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('oauth/', include('social_django.urls', namespace='social')),









    ]
