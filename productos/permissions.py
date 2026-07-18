from rest_framework import permissions


class EsAdminOSoloLectura(permissions.BasePermission):
    """
    Cualquier usuario autenticado puede leer (GET).
    Solo un usuario con rol 'admin' puede crear, editar o eliminar.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.es_admin()