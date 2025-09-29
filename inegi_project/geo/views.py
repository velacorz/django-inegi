from rest_framework import generics
from .models import Estado
from .serializers import EstadoSerializer


class EstadoListView(generics.ListAPIView):
    """
    Endpoint que devuelve la jerarquía completa:
    Estado → Municipios → Localidades → Asentamientos
    Permite filtrar con parámetros GET:
      ?estado=01
      ?municipio=01001
      ?localidad=010010001
      ?asentamiento=0100100010001
    """
    serializer_class = EstadoSerializer

    def get_queryset(self):
        qs = Estado.objects.all().prefetch_related(
            "municipio_set__localidad_set__asentamiento_set"
        )

        estado_id = self.request.query_params.get("estado")
        municipio_id = self.request.query_params.get("municipio")
        localidad_id = self.request.query_params.get("localidad")
        asentamiento_id = self.request.query_params.get("asentamiento")

        if estado_id:
            qs = qs.filter(id=estado_id)
        if municipio_id:
            qs = qs.filter(municipio__id=municipio_id)
        if localidad_id:
            qs = qs.filter(municipio__localidad__id=localidad_id)
        if asentamiento_id:
            qs = qs.filter(municipio__localidad__asentamiento__id=asentamiento_id)

        return qs.distinct()
