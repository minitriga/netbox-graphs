from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from netbox_graphs.models import Graph
from rest_framework import generics, permissions, serializers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from utilities.api import ContentTypeField, ModelViewSet


class RenderedGraphSerializer(serializers.ModelSerializer):
    embed_url = serializers.SerializerMethodField(read_only=True)
    embed_link = serializers.SerializerMethodField(read_only=True)
    type = ContentTypeField(read_only=True)

    class Meta:
        model = Graph
        fields = ["id", "type", "weight", "name", "embed_url", "embed_link"]

    def get_embed_url(self, obj):
        return obj.embed_url(self.context["graphed_object"])

    def get_embed_link(self, obj):
        return obj.embed_link(self.context["graphed_object"])


class GraphViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def retrieve(self, request, model=None, pk=None, format=None):
        model_test = ContentType.objects.get(model=model)
        queryset = Graph.objects.restrict(request.user).filter(type__model=model)
        item = get_object_or_404(model_test.model_class(), pk=pk)
        serializer = RenderedGraphSerializer(queryset, many=True, context={"graphed_object": item})
        # queryset = Graph.objects.restrict(request.user).filter(type__model='vminterface')
        # serializer = RenderedGraphSerializer(queryset, many=True, context={'graphed_object': vminterface})
        return Response(serializer.data)
