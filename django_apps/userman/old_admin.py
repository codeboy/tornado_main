from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm )

#from django.utils.translation import ugettext_lazy as _
from boss_tools.site.utils import lang_stub as _
from boss_tools.userman.models import (
    MainUser,
    GroupAsRole,
    UserContact
    )


class DefaultAdmin(admin.ModelAdmin):
    save_on_top = True
admin.site.register(GroupAsRole, DefaultAdmin)
admin.site.register(UserContact, DefaultAdmin)


###########################################################
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MainUser
        fields = ('username', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MainUser

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username',
                    'email',
        )
    #    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        (_('Contacts'), {
            'classes': ('wide',),
            'fields': (
                'email',
                )}
            ),
        (_('Permissions'),
         {'fields': (
             'is_active',
             'groups',
             #                'roles_as_groups',
             'user_permissions'
             )}
            ),
        ('Important dates', {'fields': ('last_login',)}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
            ),
        )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(MainUser, MyUserAdmin)
#admin.site.unregister(Group)