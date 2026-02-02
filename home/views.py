from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Categoria, Cliente, Produto  # Certifique-se de importar o modelo Produto
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm  # Adicione ProdutoForm aqui

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Produto

def detalhes_produto(request, id):
    # Recupera o produto com base no ID
    produto = get_object_or_404(Produto, id=id)
    
    # Passa o produto para o template
    return render(request, 'produto/detalhes.html', {'produto': produto})

# Funções para Categoria
def index(request):
    return render(request, 'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('categoria')
    else:
        form = CategoriaForm()
    contexto = {'form': form}
    return render(request, 'categoria/formulario.html', contexto)

def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form})

def detalhes_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso.')
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')
    return redirect('categoria')

# Funções para Cliente
def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html', contexto)

def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('cliente')
    else:
        form = ClienteForm()
    contexto = {'form': form}
    return render(request, 'cliente/formulario.html', contexto)

def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado')
        return redirect('cliente')

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente/formulario.html', {'form': form})

def remover_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        cliente.delete()
        messages.success(request, 'Cliente removido com sucesso.')
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
    return redirect('cliente')

# Funções para Produto
def produto(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/lista.html', {'produtos': produtos})

# Formulário para criar um novo produto
def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)  # Certifique-se de incluir request.FILES
        if form.is_valid():
            form.save()
            return redirect('produto')
    else:
        form = ProdutoForm()
    return render(request, 'produto/formulario.html', {'form': form})

# Editar produto
def editar_produto(request, id):
    produto = Produto.objects.get(id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)  # Adicionar request.FILES
        if form.is_valid():
            form.save()
            return redirect('produto')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto/formulario.html', {'form': form})

# Remover produto
def remover_produto(request, id):
    produto = Produto.objects.get(id=id)
    produto.delete()
    return redirect('produto')

def ajustar_estoque(request, id):
    produto = Produto.objects.get(pk=id)
    estoque = produto.estoque  # pega o objeto estoque relacionado ao produto
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = []
            lista.append(estoque.produto)
            return render(request, 'produto/lista.html', {'lista': lista})
    else:
        form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form})

def teste1(request):
     return render(request, 'testes/teste1.html')

def teste2(request):
    return HttpResponse("Página teste 2")
