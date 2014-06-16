# -*- coding: utf-8 -*-
###################################################
#
#  This is API mixins collection for CBV
#  use in data exchange with front on ExtJs
#
#  Коллекция микшинов для json response
#
####################################################


import json
from django.core.serializers.json import DjangoJSONEncoder, Serializer
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    Http404
)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator




class ExtLimitSetMixin(object):
    """
    проверяем и создаём переменные для постраничного вывода
    """
    r_start = 0
    r_limit = 40
    r_limit_up = 40

    def dispatch(self, request, *args, **kwargs):
        try:
            self.r_start = int(request.POST.get('start'))
            self.r_limit = int(request.POST.get('limit'))
            self.r_limit_up = (self.r_start + self.r_limit)

#            self.r_start = int(request.POST.get('start')) if request.POST.get('start') else 1
#            self.r_limit = int(request.POST.get('limit')) if request.POST.get('limit') else 40
        except (TypeError, ValueError):
            self.success = False
            self.error_msg = 'Cant get limits ("start" \ "limit") for list'
        return super(ExtLimitSetMixin, self).dispatch(request, *args, **kwargs)


#from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator

class ExtBaseMixin(object):
    """
    основной микшин для формирования правильного ответа на запрос от ExtJs

    при передаче параметра <action> вызывается метод класса
    """

    login_url = '/'

    success = True
    context = dict()
    error_msg = 'Response error' # текст сообщения об ошибке
    r_post = dict() # здесть хранится обработаный POST
    r_data = dict() # здесь отпарсенный JSON из POST['data']
    r_filter = False # словарь для сортировки по значению
    kwarg_name = 'action' # для вызова именованного метода

    def __init__(self):
        self.context = dict()

#    def __del__(self):
#        print "DESTRUCTOR IS HERE!"


    def post(self, request, *args, **kwargs):
        """
        отдаём грамотный post запрос
        """
        context = self.context

        # в зависимости от результата обработки другими микшинами и условиями выполняем основной код
        if self.success:

            # если в kwargs есть переменная нужная нам, то запускаем обработку
            if kwargs.get(self.kwarg_name):
                action = kwargs.get(self.kwarg_name)
                call_classmethod = getattr(self, action)
                context = call_classmethod(request)
            else:
                context = self.get_context(request)

        context['success'] = self.success

        # формируем текст msg только если false
        if not self.success: context['msg'] = self.error_msg

        context = json.dumps(context, cls=DjangoJSONEncoder, ensure_ascii=False)
        return HttpResponse(context, content_type='application/json')


    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        ЗАПУСКАЕТСЯ ПЕРВЫМ
        тут формируем словари с обработанными данными
        """
        if not request.user.is_authenticated():
            if not request.path == '/api/v1/ext/login':
                raise Http404()


        self.r_post = request.POST.dict()

        # если есть параметр data, то парсим json внутри него
        try:
            self.r_post.get('data')
            self.r_data = json.loads(self.r_post['data'])
        except KeyError:
            self.r_data = False

        # для фильтра то же создаём словарь
        # из массива вида
        #   { propert : some_property
        #     value : some_value }
        # получаем массив { some_property : some_value }
        try:
            self.r_post.get('filter')
            filters_dict = dict()
            var_filters = json.loads(self.r_post['filter'])
            for i in var_filters:
                filters_dict[i['property']] = i['value']
            self.r_filter = filters_dict
        except KeyError:
            self.r_filter = False

#        также и для подстроки поиска
#        try:
#            self.r_post.get('filter')
#            self.r_filter = json.loads(self.r_post['filter'])
#        except KeyError:
#            self.r_filter = False

        return super(ExtBaseMixin, self).dispatch(request, *args, **kwargs)

# DO NOT USE!
'''
    def get(self, request, *args, **kwargs):
        """
        ТОЛЬКО ВРЕМЕННО!
        """
        context = self.context
        context['success'] = False
        context['msg'] = "method not allowed"
        context = self.get_context(request, **kwargs)
        context = json.dumps(context, cls=DjangoJSONEncoder, ensure_ascii=False)
        return HttpResponse(context, content_type='application/json')
'''