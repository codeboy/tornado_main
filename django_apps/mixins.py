# -*- coding: utf-8 -*-

#from django.contrib.auth.decorators import login_required
#from django.utils.decorators import method_decorator

from django.http import HttpResponseRedirect
from django.contrib import messages


from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
try:
    import json
except ImportError: # pragma: no cover
    from django.utils import simplejson as json



class LoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE:
        This should be the left-most mixin of a view.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.is_anonymous():
            messages.add_message(request, messages.ERROR, 'You need to be logged', fail_silently=True)
            return HttpResponseRedirect('/')

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(object):
    """
    одиночный пермишн

    usage:
        class SomeView(PermissionRequiredMixin, ListView):
            ...
            # required
            permission_required = "app.permission"

            # optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
            ...
    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    permission_required = None
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        if self.permission_required == None or len(
            self.permission_required.split(".")) != 2:
            raise ImproperlyConfigured("'PermissionRequiredMixin' requires "
                                       "'permission_required' attribute to be set.")

        has_permission = request.user.has_perm(self.permission_required)

        if not has_permission:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        return super(PermissionRequiredMixin, self).dispatch(request,
            *args, **kwargs)



class SuperuserRequiredMixin(object):
    """
    для запроса прав суперюзера
    """
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        return super(SuperuserRequiredMixin, self).dispatch(request,
            *args, **kwargs)


# TODO: доделать
class JSONResponseMixin(object):
    """
    НЕИСПОЛЬЗОВАТЬ - не доделан
    тестовый микшин для JSON
    """
    content_type = "application/json"

    def get_content_type(self):
        if self.content_type is None:
            raise ImproperlyConfigured("%(cls)s is missing a content type. "
                                       "Define %(cls)s.content_type, or override "
                                       "%(cls)s.get_content_type()." % {
                                           "cls": self.__class__.__name__
                                       })
        return self.content_type

    def render_json_response(self, context_dict):
        """
        сериализация тут
        """
        json_context = json.dumps(context_dict, cls=DjangoJSONEncoder, ensure_ascii=False)
        return HttpResponse(json_context, content_type=self.get_content_type())

    def render_json_object_response(self, objects, **kwargs):
        json_data = serializers.serialize("json", objects, **kwargs)
        return HttpResponse(json_data, content_type=self.get_content_type())


class AjaxResponseMixin(object):
    """
    для аяксового вывода
    """
    def dispatch(self, request, *args, **kwargs):
        request_method = request.method.lower()

        if request.is_ajax() and request_method in self.http_method_names:
            handler = getattr(self, '%s_ajax' % request_method,
                self.http_method_not_allowed)
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return handler(request, *args, **kwargs)

        return super(AjaxResponseMixin, self).dispatch(request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def put_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)