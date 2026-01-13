from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Categoria
from .forms import CategoriaForm

def index(request):
    return render(request, 'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)  # Instancia o modelo com os dados do form
        if form.is_valid():  # Faz a validação do formulário
            form.save()  # Salva a instância do modelo no banco de dados
            messages.success(request, 'Operação realizada com sucesso!')  # Mensagem de sucesso
            return redirect('categoria')  # Redireciona para a listagem
    else:  # Método é GET, novo registro
        form = CategoriaForm()  # Formulário vazio
    contexto = {
        'form': form,
    }
    return render(request, 'categoria/formulario.html', contexto)

def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')  # Redireciona para a listagem
    
    if request.method == 'POST':
        # Combina os dados do formulário com a instância do objeto existente, permitindo editar seus valores
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()  # Save retorna o objeto salvo
            messages.success(request, 'Operação realizada com Sucesso')  # Mensagem de sucesso
            return redirect('categoria')  # Redireciona para a listagem
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form,})

# Função para mostrar os detalhes de uma categoria
def detalhes_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

# Função para remover uma categoria
def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)  # Tentando encontrar a categoria
        categoria.delete()  # Exclui a categoria
        messages.success(request, 'Categoria removida com sucesso.')  # Mensagem de sucesso
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')  # Mensagem de erro se a categoria não existir

    return redirect('categoria')  # Redireciona para a listagem de categorias
