"Django admin support for treebeard"

from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.contrib.admin.views.main import ChangeList
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from boss_tools.treebeard.templatetags.admin_tree import check_empty_dict
from boss_tools.treebeard.exceptions import (InvalidPosition, MissingNodeOrderBy,
        InvalidMoveToDescendant, PathOverflow)
from boss_tools.treebeard.forms import MoveNodeForm


class TreeChangeList(ChangeList):

    def get_ordering(self, *args):
        """
        Overriding ChangeList.get_ordering if using the Django version <= 1.3
        default of '-id' but passing through the >= 1.4 default of '[]'.
        """
        ordering = super(TreeChangeList, self).get_ordering(*args)

        if not isinstance(ordering, list):
            if not check_empty_dict(self.params):
                return ordering
            else:
                return None, 'asc'

        return ordering


class TreeAdmin(admin.ModelAdmin):
    "Django Admin class for treebeard"
    change_list_template = 'admin/tree_change_list.html'
    form = MoveNodeForm

    def get_changelist(self, request, **kwargs):
        return TreeChangeList

    def queryset(self, request):
        from boss_tools.treebeard.al_tree import AL_Node
        if issubclass(self.model, AL_Node):
            # AL Trees return a list instead of a QuerySet for .get_tree()
            # So we're returning the regular .queryset cause we will use
            # the old admin
            return super(TreeAdmin, self).queryset(request)
        else:
            return self.model.get_tree()

    def changelist_view(self, request, extra_context=None):
        from boss_tools.treebeard.al_tree import AL_Node
        if issubclass(self.model, AL_Node):
            # For AL trees, use the old admin display
            self.change_list_template = 'admin/tree_list.html'
        return super(TreeAdmin, self).changelist_view(request, extra_context)

    def get_urls(self):
        """
        Adds a url to move nodes to this admin
        """
        urls = super(TreeAdmin, self).get_urls()
        new_urls = patterns('',
            url('^move/$',
                self.admin_site.admin_view(self.move_node),),
            url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {
                'packages': ('treebeard',)}),
        )
        return new_urls + urls

    def move_node(self, request):
        try:
            node_id = request.POST['node_id']
            sibling_id = request.POST['sibling_id']
            as_child = request.POST.get('as_child', False)
            as_child = bool(int(as_child))
        except (KeyError, ValueError), e:
            # Some parameters were missing return a BadRequest
            return HttpResponseBadRequest(u'Malformed POST params')

        node = self.model.objects.get(pk=node_id)
        # Parent is not used at this time, need to handle special case
        # for root elements that do not have a parent
        #parent = self.model.objects.get(pk=parent_id)
        sibling = self.model.objects.get(pk=sibling_id)

        try:
            try:
                if as_child:
                    node.move(sibling, pos='target')
                else:
                    node.move(sibling, pos='left')
            except InvalidPosition, e:
                # This could be due two reasons (from the docs):
                # :raise InvalidPosition:
                #       when passing an invalid ``pos`` parm
                # :raise InvalidPosition:
                #       when :attr:`node_order_by` is enabled and
                #       the``pos`` parm wasn't ``sorted-sibling``
                #       or ``sorted-child``
                #
                # If it happened because the node is not a 'sorted-sibling'
                # or 'sorted-child' then try to move just a child without
                # preserving the order, so try a different move
                if as_child:
                    try:
                        # Try as unsorted tree
                        node.move(sibling, pos='last-child')
                    except InvalidPosition:
                        # We are talking about a sorted tree
                        node.move(sibling, pos='sorted-child')
                else:
                    node.move(sibling)

            # Call the save method on the (reloaded) node in order to trigger
            # possible signal handlers etc.
            node = self.model.objects.get(pk=node.pk)
            node.save()
            # If we are here, means that we moved it in one of the tries
            if as_child:
                messages.info(request,
                    _(u'Moved node "%(node)s" as child of "%(other)s"') % {
                        'node': node,
                        'other': sibling
                    })
            else:
                messages.info(request,
                    _(u'Moved node "%(node)s" as sibling of "%(other)s"') % {
                        'node': node,
                        'other': sibling
                    })

        except (MissingNodeOrderBy, PathOverflow, InvalidMoveToDescendant,
            InvalidPosition), e:
            # An error was raised while trying to move the node, then set an
            # error message and return 400, this will cause a reload on the
            # client to show the message
            # error message and return 400, this will cause a reload on
            # the client to show the message
            messages.error(request,
                _(u'Exception raised while moving node: %s') % _(
                    force_unicode(e)))
            return HttpResponseBadRequest(u'Exception raised during move')

        return HttpResponse('OK')
