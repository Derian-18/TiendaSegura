from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Pedido
from .serializers import PedidoSerializer, PedidoCreateSerializer
from .permissions import EsDuenoOAdmin


class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, EsDuenoOAdmin]
    http_method_names = ['get', 'post', 'delete']  # sin PUT/PATCH: los pedidos no se "editan", se cancelan

    def get_queryset(self):
        usuario = self.request.user
        if usuario.es_admin():
            return Pedido.objects.all().order_by('-creado_en')
        # Filtro clave: un cliente SOLO ve sus propios pedidos
        return Pedido.objects.filter(usuario=usuario).order_by('-creado_en')

    def get_serializer_class(self):
        if self.action == 'create':
            return PedidoCreateSerializer
        return PedidoSerializer

    def destroy(self, request, *args, **kwargs):
        pedido = self.get_object()  # ya valida dueño/admin vía has_object_permission
        if request.user.es_admin():
            # Admin elimina de verdad
            pedido.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # Un cliente no elimina: cancela
        if pedido.estado == Pedido.Estado.CANCELADO:
            return Response(
                {"detail": "Este pedido ya está cancelado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pedido.estado = Pedido.Estado.CANCELADO
        pedido.save()
        return Response(PedidoSerializer(pedido).data, status=status.HTTP_200_OK)