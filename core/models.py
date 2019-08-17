from django.db import models

from atracoes.models import Atracao
from comentarios.models import Comentario
from avaliacoes.models import Avaliacao
from enderecos.models import Endereco

class DocIdentificacao(models.Model):
    description = models.CharField(max_length=100)

    def  __str__(self):
        return self.description

class PontoTuristico(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    aprovado = models.BooleanField(default=False)
    atracoes = models.ManyToManyField(Atracao, related_name='atracoes')
    comentarios = models.ManyToManyField(Comentario)
    avaliacoes = models.ManyToManyField(Avaliacao)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, blank=True, null=True)
    foto = models.ImageField(upload_to='pontos_turisticos', blank=True, null=True)
    doc_identificacao = models.OneToOneField(
        DocIdentificacao, on_delete=models.CASCADE, blank=True, null=True
    )

    @property
    def descricao_completa2(self):
        return '%s - %s' % (self.nome, self.endereco)

    def __str__(self):
        return self.nome

