from rest_framework.serializers import ModelSerializer
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer
from comentarios.api.serializers import ComentarioSerializer
from rest_framework.fields import SerializerMethodField

from core.models import PontoTuristico, DocIdentificacao
from comentarios.models import Comentario
from enderecos.models import Endereco

class DocIdentificacaoSerializer(ModelSerializer):
    class Meta:
        model = DocIdentificacao
        fields = '__all__'

class PontoTuristicoSerializer(ModelSerializer):
    atracoes = AtracaoSerializer(many=True, read_only=True)
    endereco = EnderecoSerializer()
    comentarios = ComentarioSerializer(many=True)
    doc_identificacao = DocIdentificacaoSerializer()
    
    descricao_completa = SerializerMethodField()
    

    class Meta:
        model = PontoTuristico
        fields = (
            'id', 'nome', 'descricao', 'aprovado', 'foto',
            'atracoes', 'comentarios', 'avaliacoes', 'endereco',
            'descricao_completa', 'descricao_completa2', 'doc_identificacao'
        )
        read_only_fields = ['avaliacoes']

    def cria_comentarios(self, comentarios, ponto):
        for comentario in comentarios:
            comment = Comentario.objects.create(**comentario)
            ponto.comentarios.add(comment)

    def create(self, validated_data):
        comentarios = validated_data['comentarios']
        del validated_data['comentarios']

        endereco = validated_data['endereco']
        del validated_data['endereco']

        doc = validated_data['doc_identificacao']
        del validated_data['doc_identificacao']
        doci = DocIdentificacao.objects.create(**doc)

        ponto = PontoTuristico.objects.create(**validated_data)
        self.cria_comentarios(comentarios, ponto)

        end = Endereco.objects.create(**endereco)
        
        ponto.endereco = end
        ponto.doc_identificacao = doci
        ponto.save()

        return ponto
        
    def get_descricao_completa(self, obj):
        return '%s - %s' % (obj.nome, obj.descricao)