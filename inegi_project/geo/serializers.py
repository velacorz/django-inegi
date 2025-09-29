from rest_framework import serializers
from .models import Estado, Municipio, Localidad, Asentamiento


class AsentamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asentamiento
        fields = ["id", "cve_asen", "nombre"]


class LocalidadSerializer(serializers.ModelSerializer):
    asentamientos = AsentamientoSerializer(many=True, source="asentamiento_set")

    class Meta:
        model = Localidad
        fields = ["id", "cve_loc", "nombre", "asentamientos"]


class MunicipioSerializer(serializers.ModelSerializer):
    localidades = LocalidadSerializer(many=True, source="localidad_set")

    class Meta:
        model = Municipio
        fields = ["id", "cve_agem", "nombre", "localidades"]


class EstadoSerializer(serializers.ModelSerializer):
    municipios = MunicipioSerializer(many=True, source="municipio_set")

    class Meta:
        model = Estado
        fields = ["id", "nombre", "municipios"]
