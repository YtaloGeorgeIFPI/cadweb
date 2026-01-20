from django.db import models
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)  # Garantir que o nome da categoria seja único
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F", unique=True)  # Garantir que o CPF seja único
    datanasc = models.DateField(verbose_name="Data de Nascimento")

    def __str__(self):
        return self.nome

    @property
    def datanascimento(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)  # Permitindo null
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    def clean(self):
        # Verifique se 'preco' é None e defina um valor padrão ou lance um erro
        if self.preco is None or self.preco <= 0:
            raise ValidationError({'preco': 'O preço deve ser maior que zero.'})

    @property
    def estoque(self):
        """
        Tenta buscar o estoque associado ao produto. Se não existir, cria um novo estoque com quantidade 0.
        """
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item


class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'
