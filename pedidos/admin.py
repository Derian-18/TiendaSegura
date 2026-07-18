from django.contrib import admin
from .models import Pedido, ArticuloPedido


class ArticuloPedidoInline(admin.TabularInline):
    model = ArticuloPedido
    extra = 0


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'creado_en')
    inlines = [ArticuloPedidoInline]


admin.site.register(Pedido, PedidoAdmin)