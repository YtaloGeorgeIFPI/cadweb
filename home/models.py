from django.db import models
from django.core.exceptions import ValidationError
import base64
from io import BytesIO
from PIL import Image

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F", unique=True)
    datanasc = models.DateField(verbose_name="Data de Nascimento")

    def __str__(self):
        return self.nome

    @property
    def datanascimento(self):
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)  # Permitindo null
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)  # Novo campo para imagem
    img_base64 = models.TextField(blank=True)  # Campo base64 para imagem

    def __str__(self):
        return self.nome

    def clean(self):
        if self.preco is None or self.preco <= 0:
            raise ValidationError({'preco': 'O preço deve ser maior que zero.'})

    def save(self, *args, **kwargs):
        if self.imagem:
            # Converte a imagem para Base64 ao salvar
            self.img_base64 = self.convert_to_base64(self.imagem)
        super().save(*args, **kwargs)

    def convert_to_base64(self, image):
        """
        Converte uma imagem para string Base64.
        """
        img = Image.open(image)
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        img_str = base64.b64encode(img_io.read()).decode()
        return img_str

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
    


class Pedido(models.Model):


    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4


    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]


    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)

    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None


    def __str__(self):
            return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"  
