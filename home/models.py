from django.db import models
from django.core.exceptions import ValidationError
import base64
from io import BytesIO
from decimal import Decimal
from PIL import Image
import random
import string


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
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    def clean(self):
        if self.preco is None or self.preco <= 0:
            raise ValidationError({'preco': 'O preço deve ser maior que zero.'})

    def save(self, *args, **kwargs):
        if self.imagem:
            self.img_base64 = self.convert_to_base64(self.imagem)
        super().save(*args, **kwargs)

    def convert_to_base64(self, image):
        img = Image.open(image)
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        img_str = base64.b64encode(img_io.read()).decode()
        return img_str

    @property
    def estoque(self):
        estoque_item, _ = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
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

    # 🔹 Campos extras para Nota Fiscal
    chave_acesso = models.CharField(max_length=44, blank=True, null=True)
    icms = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ipi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pis = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cofins = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None

    @property
    def total(self):
        """Calcula o valor total do pedido"""
        return sum(item.subtotal for item in self.itempedido_set.all())

    @property
    def total_impostos(self):
        """Soma de todos os impostos"""
        return self.icms + self.ipi + self.pis + self.cofins

    @property
    def total_com_impostos(self):
        """Valor final com impostos"""
        return self.total + self.total_impostos

    @property
    def pagamentos(self):
        """Lista de todos os pagamentos realizados"""
        return self.pagamento_set.all()

    @property
    def total_pago(self):
        """Calcula o total de todos os pagamentos do pedido"""
        return sum(pagamento.valor for pagamento in self.pagamentos)

    @property
    def debito(self):
        """Calcula o débito (quanto falta pagar)"""
        return max(self.total - self.total_pago, 0)

    def gerar_chave_acesso(self):
        """Gera uma chave de acesso de 44 dígitos"""
        self.chave_acesso = ''.join(random.choices(string.digits, k=44))

    def calcular_impostos(self):
        """Calcula impostos com base no total do pedido"""
        self.icms = self.total * Decimal('0.18')   # 18% ICMS
        self.ipi = self.total * Decimal('0.04')    # 4% IPI
        self.pis = self.total * Decimal('0.0165')  # 1,65% PIS
        self.cofins = self.total * Decimal('0.076') # 7,6% COFINS

    def save(self, *args, **kwargs):
        # Gera chave de acesso se não existir
        if not self.chave_acesso:
            self.gerar_chave_acesso()
        # Só calcula impostos se já tiver PK (pedido salvo) e itens
        if self.pk:
            self.calcular_impostos()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        """Calcula o valor total deste item"""
        return self.qtde * self.preco

    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"


class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4

    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)

    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None
