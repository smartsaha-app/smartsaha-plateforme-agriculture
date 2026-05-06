from django.contrib import admin
from apps.groups.models import Group, MemberGroup, Organisation, GroupType, GroupRole

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'type', 'status')

@admin.register(MemberGroup)
class MemberGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'status', 'initiated_by')  # ✅ initiated_by ajouté
    list_filter = ('status', 'initiated_by')                             # ✅ filtre dans la sidebar
