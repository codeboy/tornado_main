# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic.edit import UpdateView
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
#from accounts.forms import UserForm
from django.contrib.auth.models import User
from django.utils.http import base36_to_int
#----------------------


# TODO: need refactory imports up there ... and down
import urlparse

from django.shortcuts import  redirect

from django.views.generic.base import  TemplateResponseMixin
from django.views.generic.edit import FormView
from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import  HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from django.conf import settings

#from django.utils.translation import ugettext_lazy as _
from django_apps.utils import lang_stub as _
from django_apps.utils import page_message



class LogoutView(View):
    success_message = _("Successfully logged out.")

    def get(self, request, *args, **kwargs):
        logout(request)
#        messages.success(request, self.success_message, fail_silently=True)
        return HttpResponseRedirect('/')
#        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginView(View, TemplateResponseMixin):
    """
    login
    """
    http_method_names = ['post']
    template_name = 'site/main.html'

    def get_context(self, request):
        context = dict()
        return context

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)


    def check_user(self, request):
        """
        checking params, return user
        """
        if request.POST.get('login') and request.POST.get('password'):
            user = authenticate(username=request.POST.get('login'), password=request.POST.get('password'))
            if user:
                login(request, user)
                return user
            else:
                return False


    def post (self, request, *args, **kwargs):
        """
        perform work for POST
        """

        user = self.check_user(request)
        if not user:
#            page_message(request, code=None, text='Login error', type='ERROR')
            page_message(request, 40, None, 'error')

        if request.POST.get('loginurl'):
            return redirect(request.POST.get('loginurl'))
        else:
            return redirect('/')



######################################################
class Login3(FormView):
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'accounts/login.html'

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def form_valid(self, form):
        login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(Login, self).form_valid(form)

    #@method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(Login, self).dispatch(*args, **kwargs)


class Logout3(RedirectView):
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_redirect_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
        if redirect_to:
            netloc = urlparse.urlparse(redirect_to)[1]
            if netloc and netloc != self.request.get_host():
                redirect_to = ''
        return redirect_to or '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, u'You have been logged out.')
        return super(Logout, self).get(request, *args, **kwargs)


class PasswordReset(FormView):
    form_class = PasswordResetForm
    token_generator = default_token_generator
    template_name = 'accounts/password_reset_form.html'
    email_template_name='accounts/password_reset_email.html'
    subject_template_name='accounts/password_reset_subject.txt'
    from_email = None
    success_url = '/'

    def form_valid(self, form):
        form.save(use_https=self.request.is_secure(),
            token_generator=self.token_generator,
            from_email=self.from_email,
            email_template_name=self.email_template_name,
            subject_template_name=self.subject_template_name,
            request=self.request)
        messages.success(self.request, u'Check your email for the password reset link.')
        return super(PasswordReset, self).form_valid(form)

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(PasswordReset, self).dispatch(*args, **kwargs)


class PasswordResetConfirm(FormView):
    form_class = SetPasswordForm
    token_generator = default_token_generator
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('home')

    def get_user(self, uid=None):
        if not hasattr(self, '_user'):
            if uid is None:
                uidb36 = self.kwargs.get('uidb36', 0)
                uid = base36_to_int(uidb36)
            try:
                self._user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                self._user = None
        return self._user

    def get_form_kwargs(self):
        kwargs = super(PasswordResetConfirm, self).get_form_kwargs()
        kwargs['user'] = self.get_user()
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, u'Password reset.')
        return super(PasswordResetConfirm, self).form_valid(form)

    #@method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        uidb36 = kwargs.get('uidb36', 0)
        uid = base36_to_int(uidb36)
        user = self.get_user(uid)
        token = kwargs.get('token', '')
        if self.token_generator.check_token(user, token):
            return super(PasswordResetConfirm, self).dispatch(*args, **kwargs)
        else:
            raise Http404
