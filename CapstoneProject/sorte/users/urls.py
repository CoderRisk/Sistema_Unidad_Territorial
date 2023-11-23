from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm
from .forms import UserPasswordResetConfirmForm

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('profile_user', views.profile_user, name="profile_user"),
    path('update_profile_user', views.update_profile_user, name="update_profile_user"),
    # Paths para restablecer la contraseña
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authenticate/reset_password.html", form_class=UserPasswordResetForm), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="authenticate/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authenticate/password_reset_confirm.html", form_class=UserPasswordResetConfirmForm), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authenticate/password_reset_done.html"), name='password_reset_complete'),
    # Path para la activación de la cuenta del miembro
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    # Paths para el certificado de residencia
    path('generar_certificado/', views.generar_certificado, name='generar_certificado'),
]