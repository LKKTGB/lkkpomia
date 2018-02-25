from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from website.models.profile import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'

    fields = ('avatar',)
    readonly_fields = ('avatar',)

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_superuser',)}),
    )
    readonly_fields = ('username', 'first_name', 'last_name')

    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)
