from django import forms
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido, Pagamento
from datetime import date

# Formulário para Categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem <= 0:
            raise forms.ValidationError("O campo ordem deve ser maior que zero.")
        return ordem


# Formulário para Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%Y-%m-%d'),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if len(cpf) != 14 or not cpf.replace('.', '').replace('-', '').isdigit():
            raise forms.ValidationError("O CPF deve ser válido (formato: XXX.XXX.XXX-XX).")
        return cpf

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc.year < 1900:
            raise forms.ValidationError("A data de nascimento não pode ser anterior a 1900.")
        if datanasc and datanasc > date.today():
            raise forms.ValidationError("A data de nascimento não pode ser maior que a data atual.")
        return datanasc


# Formulário para Produto
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64']
        widgets = {
            'categoria': forms.HiddenInput(),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'img_base64': forms.HiddenInput(),
            'preco': forms.TextInput(attrs={'class': 'money form-control', 'maxlength': 500, 'placeholder': '0.000,00'}),
        }
        labels = {
            'nome': 'Nome do Produto',
            'preco': 'Preço do Produto',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True


# Formulário para Estoque
class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'qtde']
        widgets = {
            'produto': forms.HiddenInput(),
            'qtde': forms.TextInput(attrs={'class': 'inteiro form-control'}),
        }


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput(),
        }


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido', 'produto', 'qtde']
        widgets = {
            'pedido': forms.HiddenInput(),
            'produto': forms.HiddenInput(),
            'qtde': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Formulário para Pagamento
class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['forma', 'valor']  # 🔹 removemos 'pedido'
        widgets = {
            'forma': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'money form-control', 'maxlength': 500, 'placeholder': '0.000,00'}),
        }

    def __init__(self, *args, **kwargs):
        super(PagamentoForm, self).__init__(*args, **kwargs)
        self.fields['valor'].localize = True
        self.fields['valor'].widget.is_localized = True

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        pedido = getattr(self.instance, 'pedido', None)

        if valor is None:
            raise forms.ValidationError("Informe um valor válido.")

        if valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")

        if pedido:
            # Se for edição, considerar o valor anterior
            valor_anterior = self.instance.valor if self.instance.pk else 0
            limite = pedido.debito + valor_anterior
            if valor > limite:
                raise forms.ValidationError(
                    f"O valor não pode ser maior que o débito restante (máx permitido: {limite})."
                )

        return valor
