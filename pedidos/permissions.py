from rest_framework import permissions


class EsDuenoOAdmin(permissions.BasePermission):
    """
    - list/create: cualquier autenticado (el queryset ya filtra qué ve cada quien).
    - retrieve/update/delete de un objeto puntual: solo el dueño del pedido o un admin.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.es_admin():
            return True
        return obj.usuario_id == request.user.id