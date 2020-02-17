"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kennywoodapi.models import ParkArea

class ParkAreaSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for parks areas

    Arguments:
    serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = ParkArea
        url = serializers.HyperlinkedIdentityField(
            view_name='parkarea',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'theme')

class ParkAreas(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    # GET one
    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            area = ParkArea.objects.get(pk=pk)
            serializer = ParkAreaSerializer(
                area, 
                context={'request': request}
                )
        except Exception as ex:
            return HttpResponseServerError(ex)

    # GET all
    def list(self, request):
        """ Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        areas = ParkArea.objects.all()
        serializer = ParkAreaSerializer(
            areas,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    # POST one
    def create(self, request):
        """Handle POST operations

        Returns:
            Reponse -- JSON serialized ParkArea instance
        """
        newarea = ParkArea()
        newarea = request.data["name"]
        newarea.theme = request.data["theme"]
        newarea.save()

        serializer = ParkAreaSerializer(
            newarea,
            context={'request': request}
        )

        return Response(serializer.data)