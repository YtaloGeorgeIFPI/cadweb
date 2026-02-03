from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.apps import apps
from .models import Categoria, Cliente, Produto, Pedido, ItemPedido, Pagamento
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm, PedidoForm, ItemPedidoForm, PagamentoForm
from django.contrib.auth.decorators import login_required

# ------------------- PRODUTO -------------------
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produto/detalhes.html', {'produto': produto})


# ------------------- CATEGORIA -------------------
@login_required
def index(request):
    return render(request, 'index.html')

def categoria(request):
    contexto = {'lista': Categoria.objects.all().order_by('-id')}
    return render(request, 'categoria/lista.html', contexto)
@login_required
def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('categoria')
    else:
        form = CategoriaForm()
    return render(request, 'categoria/formulario.html', {'form': form})
@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form})
@login_required
def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})
@login_required
def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso.')
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')
    return redirect('categoria')

def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '')
    try:
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)

    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)

    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)


# ------------------- CLIENTE -------------------
@login_required
def cliente(request):
    contexto = {'lista': Cliente.objects.all().order_by('-id')}
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
    return render(request, 'cliente/formulario.html', {'form': form})

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
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


# ------------------- PRODUTO -------------------
@login_required
def produto(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/lista.html', {'produtos': produtos})

def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('produto')
    else:
        form = ProdutoForm()
    return render(request, 'produto/formulario.html', {'form': form})
@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto/formulario.html', {'form': form})
@login_required
def remover_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('produto')
@login_required
def ajustar_estoque(request, id):
    produto = get_object_or_404(Produto, pk=id)
    estoque = produto.estoque
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            return redirect('produto')
    else:
        form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form})


# ------------------- TESTES -------------------
def teste1(request):
    return render(request, 'testes/teste1.html')

def teste2(request):
    return HttpResponse("Página teste 2")


# ------------------- PEDIDO -------------------
@login_required
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})
@login_required
def novo_pedido(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()  # salva e guarda o objeto
            messages.success(request, 'Pedido criado com sucesso!')
            # redireciona para detalhes do pedido recém-criado
            return redirect('detalhes_pedido', id=pedido.id)
    else:
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)

    return render(request, 'pedido/form.html', {'form': form})

@login_required
def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.pedido = pedido
            item_pedido.preco = item_pedido.produto.preco  # preço automático

            # 🔹 Tratamento de estoque
            estoque = item_pedido.produto.estoque
            if estoque.qtde < item_pedido.qtde:
                messages.error(request, 'Estoque insuficiente para este produto!')
            else:
                estoque.qtde -= item_pedido.qtde
                estoque.save()
                item_pedido.save()
                messages.success(request, 'Item adicionado com sucesso!')
            return redirect('detalhes_pedido', id=pedido.id)
        else:
            messages.error(request, 'Erro ao adicionar produto')
    else:
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)

    contexto = {
        'pedido': pedido,
        'form': form,
        'itens': pedido.itempedido_set.all(),
        'pagamentos': pedido.pagamento_set.all(),  # 🔹 agora os pagamentos são enviados
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def editar_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    pedido = item_pedido.pedido
    quantidade_anterior = item_pedido.qtde

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            estoque = item_pedido.produto.estoque

            diferenca = item_pedido.qtde - quantidade_anterior
            if diferenca > 0 and estoque.qtde < diferenca:
                messages.error(request, 'Estoque insuficiente para este produto!')
            else:
                estoque.qtde -= diferenca
                estoque.save()
                item_pedido.preco = item_pedido.produto.preco
                item_pedido.save()
                messages.success(request, 'Item atualizado com sucesso!')
                return redirect('detalhes_pedido', id=pedido.id)
        else:
            messages.error(request, 'Erro ao atualizar item do pedido')
    else:
        form = ItemPedidoForm(instance=item_pedido)

    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido,
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Item não encontrado')
        return redirect('pedido')

    pedido = item_pedido.pedido
    estoque = item_pedido.produto.estoque

    # devolve a quantidade ao estoque
    estoque.qtde += item_pedido.qtde
    estoque.save()

    item_pedido.delete()
    messages.success(request, 'Item removido com sucesso!')
    return redirect('detalhes_pedido', id=pedido.id)
@login_required
def remover_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido não encontrado')
        return redirect('pedido')

    # devolve os itens ao estoque antes de remover
    for item in pedido.itempedido_set.all():
        estoque = item.produto.estoque
        estoque.qtde += item.qtde
        estoque.save()
        item.delete()

    pedido.delete()
    messages.success(request, 'Pedido removido com sucesso!')
    return redirect('pedido')

@login_required
def novo_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if request.method == "POST":
        form = PagamentoForm(request.POST, instance=Pagamento(pedido=pedido))
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, "Pagamento registrado com sucesso!")
            return redirect("detalhes_pedido", id=pedido.id)
        else:
            print(form.errors)
            messages.error(request, "Erro ao registrar pagamento")
    else:
        form = PagamentoForm(instance=Pagamento(pedido=pedido))
    return render(request, "pagamento/formulario.html", {"form": form, "pedido": pedido})

@login_required
def editar_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    pedido = pagamento.pedido
    if request.method == "POST":
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Pagamento atualizado com sucesso!")
            return redirect("detalhes_pedido", id=pedido.id)
        else:
            messages.error(request, "Erro ao atualizar pagamento")
    else:
        form = PagamentoForm(instance=pagamento)
    return render(request, "pagamento/formulario.html", {"form": form, "pedido": pedido})

@login_required
def remover_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    pedido = pagamento.pedido
    pagamento.delete()
    messages.success(request, "Pagamento removido com sucesso!")
    return redirect("detalhes_pedido", id=pedido.id)


def nota_fiscal(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    return render(request, 'pedido/nota_fiscal.html', {'pedido': pedido})
