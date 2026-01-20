from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página inicial
    path('', views.index, name='index'),  # Página inicial

    # Rotas para categoria
    path('categoria/', views.categoria, name="categoria"),
    path('categoria/form', views.form_categoria, name="form_categoria"),
    path('categoria/editar/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categoria/detalhes/<int:id>/', views.detalhes_categoria, name="detalhes_categoria"),
    path('categoria/remover/<int:id>/', views.remover_categoria, name="remover_categoria"),

    # Rotas para cliente
    path('cliente/', views.cliente, name='cliente'),  # Exibe a lista de clientes
    path('cliente/form', views.form_cliente, name='form_cliente'),  # Formulário de cliente
    path('cliente/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),  # Edita um cliente
    path('cliente/remover/<int:id>/', views.remover_cliente, name='remover_cliente'),  # Remove um cliente

    # Rotas para produto
    # Listagem de Produtos
    path('produto/', views.produto, name='produto'),
    # Formulário de Produtos
    path('produto/form', views.form_produto, name='form_produto'),
    # Detalhes do Produto
    path('produto/detalhes/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    # Editar Produto
    path('produto/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    # Remover Produto
    path('produto/remover/<int:id>/', views.remover_produto, name='remover_produto'),
    path('produto/ajustar_estoque/<int:id>/', views.ajustar_estoque, name='ajustar_estoque'),

]
