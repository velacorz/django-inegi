from django.db import models


class Estado(models.Model):
    id = models.CharField(max_length=2, primary_key=True)  # cve_agee
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    id = models.CharField(max_length=5, primary_key=True)  # estado.id + cve_agem
    cve_agem = models.CharField(max_length=3)  # clave oficial INEGI
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.estado.nombre}"


class Localidad(models.Model):
    id = models.CharField(max_length=9, primary_key=True)  # estado.id + cve_agem + cve_loc
    cve_loc = models.CharField(max_length=4)  # clave oficial INEGI
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.municipio.nombre}"


class Asentamiento(models.Model):
    id = models.CharField(max_length=13, primary_key=True)  # estado+mun+loc+asen
    cve_asen = models.CharField(max_length=4)
    nombre = models.CharField(max_length=100)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.localidad.nombre}"
