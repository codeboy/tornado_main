# -*- coding: utf-8 -*-

import urllib2
import re
import time
import warnings
import pprint

from datetime import datetime, date
import calendar

from django.utils.timezone import is_aware, utc

from django.db import connection, connections, transaction
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core import urlresolvers

import django_apps.page_messages_list as pml

try:
    from projectapps.mail_e.utils import send_mail2 as send
except ImportError:
    send = ()


def class_view_decorator(function_decorator):
    """
    Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.

    Usage:
    @class_view_decorator(login_required)
    class MyView(View):
        # this view now decorated
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


def get_named_patterns():
    """
    Returns list of urlpatterns (pattern-name, pattern) tuples
    """
    resolver = urlresolvers.get_resolver(None)
    patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ])
    return patterns


def send_mail(email_to, subject, content):
    return send(email_to, subject, content)


def db_query_dict(query):
    """
    принимает query - SQL запрос
    выполняет запрос к базе и отдаёт ассоциативный массив
    имена полей в query должны быть либо уникальными либо именоваными
    """

    cursor = connection.cursor()
    cursor.execute(query)
    desc = cursor.description
    q_list = list()

    for i in range(cursor.rowcount):
        q_dict = dict()
        data = cursor.fetchone()
        for name, value in zip(desc, data) :
            q_dict[name[0]] = value
        q_list.append(q_dict)

    warnings.warn("use db_aliases_query_dict instead this",
    DeprecationWarning)
    return q_list, cursor.rowcount
#    return q_list


def db_aliases_query_dict(query, database='default'):
    """
    ДЛЯ ВЫБОРКИ БАЗЫ
    принимает query - SQL запрос
    выполняет запрос к базе и отдаёт ассоциативный массив
    имена полей в query должны быть либо уникальными либо именоваными
    """

    cursor = connections[database].cursor()
    cursor.execute(query)
    desc = cursor.description

    q_list = list()
    for i in range(cursor.rowcount):
        q_dict = dict()
        data = cursor.fetchone()
        for name, value in zip(desc, data) :
            q_dict[name[0]] = value
        q_list.append(q_dict)

    return q_list, cursor.rowcount
#    return q_list



def page_message(request, code=None, text=None, type='ERROR'):
    """
    send message using django framework
    """
    message_text = ''
    fail_flag = True

    if text:
        message_text = text
    else:
        if code == '':
            message_text = 'Blank'
        else:
            if code in pml.m_text:
                message_text = pml.m_text[code]
            elif code in pml.m_code :
                message_text = pml.m_code[code]

    if type == 'error':
        messages.add_message(request, messages.ERROR, message_text, fail_silently=fail_flag)
    elif type == 'info':
        messages.add_message(request, messages.INFO, message_text, fail_silently=fail_flag)
    elif type == 'success':
        messages.add_message(request, messages.SUCCESS, message_text, fail_silently=fail_flag)
    else:
        messages.add_message(request, messages.ERROR, message_text, fail_silently=fail_flag)



def render_me_price(r_string):
    """
    форматирование цены в не зависимости от передаваемого типа
    """
    string = r_string

    if type(r_string) == float:
        string = "%0.2f" % (r_string)
    elif type(r_string) == int:
        string = str(r_string)
    elif type(r_string) == str and len(r_string.split('.')) > 1:
        string = "%0.2f" % (float(r_string))

    if 'None' in str(type(r_string)):
        data = r_string
    else:
        data = ''

        if len(string.split('.')) > 1:
            str_int, str_dec = string.split('.')
        else:
            str_int = string

        for i in range(len(str_int)):
            str_int_revert = str_int[::-1]
            data += str_int_revert[len(str_int)-(len(str_int)-i)]
            z = str((float(i)+1)/3).split('.')
            if z[1] == '0':
                data += ' '
        data = data[::-1]

        try:
            data += '.%s' % str_dec
        except UnboundLocalError:
            pass

    return data


def send_sms(r_to, r_str):
    text = r_str.replace(' ', '%20')

    theurl = 'http://gate.sms-start.ru/send/'
    theurl2 = 'http://gate.sms-start.ru/send/?phone={phone}&text={text}&sender=STAKOS.RU'.format(
        phone = r_to,
        text = text
        )
    username = 'stakos'
    password = 's13s11'

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    pagehandle = urllib2.urlopen(theurl2)

#    print pagehandle.read()
    return pagehandle.read()


def sms_request_status(sms_id='57338207'):
    theurl = 'http://gate.sms-start.ru/status/'
    theurl2 = 'http://gate.sms-start.ru/status/?id={sms_id}'.format(
        sms_id = sms_id,
        )
    username = 'stakos'
    password = 's13s11'

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    pagehandle = urllib2.urlopen(theurl2)

#    print pagehandle.read()
    return pagehandle.read()


def phone_validate_util(function):
    """
    декоратор создаёт сообщение если моб.номер не подтверждён
    """
    def new(request, *args, **kwargs):
#        print request
        if not request.user.phone_mobile_status:
            page_message(request, 70, None, 'info')
        return function(request, *args, **kwargs)
    return new


def phone_formater(r_str):
    """
    форматирует телефон
    удаляет всё не цифровое
    отдаёт только 10 первых цифр
    """

    string = re.sub(r"\D", '', r_str)
    string = string.encode()
    if len(string) >= 10:
        string = string[-10:]
    return string




def timeit(method):
    """
    декоратор принтит время выполнния метода
    !!! не использовать в продакшене, или переписать принт !!!
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r) %2.2f sec' % (method.__name__, kw, te-ts)
        return result

    return timed


def cleanup_util(r_str):
    """
    очищает строку от всего лишнего
    нужно для поиска
    работает с кириллицей
    """
    return re.sub(ur'[^а-яa-z0-9]', u'', r_str.lower(), re.UNICODE)


def lang_stub(text=''):
    """
    заглушко для перевода текста
    """
    return text


def get_timedelta_days(d, now=False):
    """
    отсчитывает время от сегодня до даты в днях
    """

    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime):
        d = datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime):
        now = datetime(now.year, now.month, now.day)

    if not now:
        now = datetime.now(utc if is_aware(d) else None)

    delta = (d - now) if reversed else (now - d)
    return delta.days


def create_django_list(dict2iterate):
    u"""
    возвращает кошерный список для choices джанго созданый из словаря
    """
    new_list = list()
    for k, v in dict2iterate.iteritems():
        new_list.append([k, v])
    return new_list


def create_dict_from_choices(original_list):
    """
    создаёт юзабельный словарь из Django choice списка
    """
    created_dict = dict()
    for i in original_list:
        if len(i) > 2:
            return False
        else:
            created_dict[i[0]] = i[1]
    return created_dict


def pretty_print_simple(pdict):
    u"""
    выводит на печать словарь с красивыми отступами
    """
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(pdict)

def pretty_print(d, indent=0):
    u"""
    То же самое, что и выше, но более красивее ;)
    """
    for key, value in d.iteritems():
        print '\t' * indent + str(key)
        if isinstance(value, dict):
            pretty_print(value, indent+1)
        else:
            print '\t' * (indent+1) + str(value)


def add_months(sourcedate, months):
    u"""
    Добавляет к дате месяцы

    set_date =  datetime.date(2010, 12, 9)
    print add_months(set_date, 1)
    > 2011-01-09

    если нужны дни то есть - (datetime.now()+datetime.timedelta(days=30)
    """
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.db.models.query import QuerySet

class InheritanceQuerySet(QuerySet):
    """
    обработка наследуемых моделей
    -----------------------------

    class Base(models.Model):
        name = models.CharField(max_length=255)

    class SubA(Base):
        sub_field_a = models.CharField(max_length=255)

    class SubB(Base):
        sub_field_b = models.CharField(max_length=255)

    >> qs = InheritanceQuerySet(model=Base)
    >> qs
    [<Base: Base object>, <Base: Base object>]
    >> qs.select_subclasses()
    [<SubA: SubA object>, <SubB: SubB object>]
    >> qs.select_subclasses('suba')
    [<SubA: SubA object>, <Base: Base object>]
    >> qs.select_subclasses('subb').exclude(name__icontains="a")
    [<SubA: SubB object>]
    """
    def select_subclasses(self, *subclasses):
        if not subclasses:
            subclasses = [o for o in dir(self.model)
                          if isinstance(getattr(self.model, o), SingleRelatedObjectDescriptor)\
                          and issubclass(getattr(self.model,o).related.model, self.model)]
        new_qs = self.select_related(*subclasses)
        new_qs.subclasses = subclasses
        return new_qs

    def _clone(self, klass=None, setup=False, **kwargs):
        try:
            kwargs.update({'subclasses': self.subclasses})
        except AttributeError:
            pass
        return super(InheritanceQuerySet, self)._clone(klass, setup, **kwargs)

    def iterator(self):
        iter = super(InheritanceQuerySet, self).iterator()
        if getattr(self, 'subclasses', False):
            for obj in iter:
                obj = [getattr(obj, s) for s in self.subclasses if getattr(obj, s)] or [obj]
                yield obj[0]
        else:
            for obj in iter:
                yield obj


def sorting_list_of_dicts(source_dict, dict_keys):
    """
    сортирует список словарей по одному или нескольким ключам

    A = [{'name':'john','age':45},
     {'name':'andi','age':23},
     {'name':'john','age':22},
     {'name':'paul','age':35},
     {'name':'john','age':21}]

     >> sorting_list_of_dictis(A, ('name', 'age'))
     [{'age': 23, 'name': 'andi'}, {'age': 21, 'name': 'john'}, {'age': 22, 'name': 'john'}, {'age': 45, 'name': 'john'}, {'age': 35, 'name': 'paul'}]
    """

    from operator import itemgetter
    newlist = sorted(source_dict, key=itemgetter(dict_keys))
    return newlist


def slice_list_of_dicts(source_dict, dict_key):
    """
    создаёт срез списка словарей по ключу
    """
    from operator import itemgetter
    newlist = map(itemgetter(dict_key), source_dict)
    return newlist
