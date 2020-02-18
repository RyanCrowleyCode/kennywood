"""Attractions for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction

class AttractionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for attractions

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Attraction
        url = serializers.HyperlinkedIdentityField(
            view_name='attraction',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'area')
        depth = 2


class Attractions(ViewSet):

    # GET one
    def retrieve(self, request, pk=None):
        """Handle GET requests for single attraction

        Returns:
            Response -- JSON serialized attraction instance
        """

        try:
            attraction = Attraction.objects.get(pk=pk)
            serializer = AttractionSerializer(
                attraction,
                context={'request': request}
            ) 
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    # GET all
    def list(self, request):
        """Handle GET requests for all attractions

        Returns:
            Response -- JSON serialized list of attractions
        """

        attractions = Attraction.objects.all()

        area = self.request.query_params.get('area', None)
        if area is not None:
            # Double underscore for area__id
            # attractions area id = number
            attractions = attractions.filter(area__id=area)

        serializer = AttractionSerializer(
            attractions,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)