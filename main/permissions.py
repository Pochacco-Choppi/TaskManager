from rest_framework.permissions import DjangoObjectPermissions


class StaffPermissions(DjangoObjectPermissions):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return super().has_object_permission(request, view, obj)
