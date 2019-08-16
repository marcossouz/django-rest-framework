from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication
from core.models import PontoTuristico
from .serializers import PontoTuristicoSerializer


class PontoTuristicoViewSet(ModelViewSet):

    serializer_class = PontoTuristicoSerializer
    filter_backends = (SearchFilter,)
    # permission_classes = (IsAuthenticated,)
    # permission_classes = (IsAdminUser,)
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    # permission_classes = (DjangoModelPermissions,) # permissoes pelo django admin
    # authentication_classes = (TokenAuthentication,)
    search_fields = ('nome', 'descricao', 'endereco__linha1')
    lookup_field = 'nome' # precisa ser unique no banco

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        nome = self.request.query_params.get('nome', None)
        descricao = self.request.query_params.get('descricao', None)

        queryset = PontoTuristico.objects.all()
        if id:
            queryset = queryset.filter(pk=id)
        
        if nome:
            queryset = queryset.filter(nome__iexact=nome)
        
        if descricao:
            queryset = queryset.filter(descricao__iexact=descricao)

        # return PontoTuristico.objects.filter(aprovado=True)
        return queryset
    
    def list(self, request, *args, **kwargs):
        # return Response({'Teste':1234})
        return super(PontoTuristicoViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # return Response({'Hello':request.data['nome']})
        return super(PontoTuristicoViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # return Response({'method':'DELETE'})
        return super(PontoTuristicoViewSet, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # return Response({'method':'GET for id'})
        return super(PontoTuristicoViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # return Response({'method':'PUT'})
        return super(PontoTuristicoViewSet, self).update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        # return Response({'method':'PTCH'})
        return super(PontoTuristicoViewSet, self).partial_update(request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def denunciar(self, request, pk=None):
        return Response({'Minha action':'Personalizada', 'request':request.data['teste']})

    @action(methods=['get'], detail=False)
    def teste(self, request):
        return Response({'Action Sem Id': 'OK'})