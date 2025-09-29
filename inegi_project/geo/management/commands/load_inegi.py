from django.core.management.base import BaseCommand
import requests
from geo.models import Estado, Municipio, Localidad, Asentamiento
from django.db import transaction
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Command(BaseCommand):
    help = "Carga TODOS los datos de INEGI (Estados, Municipios, Localidades y Asentamientos)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("=== Iniciando carga de datos desde INEGI ==="))
        try:
            with transaction.atomic():
                self.cargar_estados()
                self.stdout.write(self.style.SUCCESS("✔ Estados cargados."))

                self.cargar_municipios()
                self.stdout.write(self.style.SUCCESS("✔ Municipios cargados."))

                self.cargar_localidades()
                self.stdout.write(self.style.SUCCESS("✔ Localidades cargadas."))

                self.cargar_asentamientos()
                self.stdout.write(self.style.SUCCESS("✔ Asentamientos cargados."))

            self.stdout.write(self.style.SUCCESS("=== Carga finalizada exitosamente ==="))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante la carga: {e}"))

    # ------------------------
    # Cargar Estados
    # ------------------------
    def cargar_estados(self):
        url = "https://gaia.inegi.org.mx/wscatgeo/mgee"
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            data = response.json()
            if "datos" in data:
                estados = [
                    Estado(id=estado["cve_agee"].zfill(2), nombre=estado["nom_agee"])
                    for estado in data["datos"]
                ]
                Estado.objects.bulk_create(estados, ignore_conflicts=True)
                self.stdout.write(self.style.NOTICE(f"✔ Se cargaron {len(estados)} estados."))
        else:
            raise Exception(f"No se pudo obtener estados: {response.status_code}")

    # ------------------------
    # Cargar Municipios
    # ------------------------
    def cargar_municipios(self):
        total_mun = 0
        for estado in Estado.objects.all():
            url = f"https://gaia.inegi.org.mx/wscatgeo/mgem/{estado.id}"
            response = requests.get(url, verify=False)
            self.stdout.write(self.style.NOTICE(f"Consultando municipios: {url}"))

            if response.status_code == 200:
                data = response.json()
                if "datos" in data:
                    municipios = [
                        Municipio(
                            id=f"{estado.id}{mun['cve_agem'].zfill(3)}",
                            cve_agem=mun["cve_agem"].zfill(3),
                            nombre=mun["nom_agem"],
                            estado=estado
                        )
                        for mun in data["datos"]
                    ]
                    Municipio.objects.bulk_create(municipios, ignore_conflicts=True)
                    total_mun += len(municipios)
                    self.stdout.write(f"✔ {estado.nombre}: {len(municipios)} municipios cargados")
                else:
                    self.stdout.write(self.style.WARNING(f"⚠ Sin datos de municipios para {estado.id}: {data}"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Error {response.status_code} en {url}"))
        self.stdout.write(self.style.NOTICE(f"✔ Total de municipios cargados: {total_mun}"))

    # ------------------------
    # Cargar Localidades
    # ------------------------
    def cargar_localidades(self):
        total_loc = 0
        municipios = Municipio.objects.all()
        for idx, municipio in enumerate(municipios, start=1):
            clave = f"{municipio.estado.id}{municipio.cve_agem}"
            url = f"https://gaia.inegi.org.mx/wscatgeo/mgel/{clave}"
            response = requests.get(url, verify=False)

            self.stdout.write(self.style.NOTICE(f"Consultando localidades: {url}"))

            if response.status_code == 200:
                data = response.json()
                if "datos" in data and data["datos"]:
                    localidades = [
                        Localidad(
                            id=f"{clave}{loc['cve_loc'].zfill(4)}",
                            cve_loc=loc["cve_loc"].zfill(4),
                            nombre=loc["nom_loc"],
                            municipio=municipio
                        )
                        for loc in data["datos"]
                    ]
                    Localidad.objects.bulk_create(localidades, ignore_conflicts=True)
                    total_loc += len(localidades)
                    self.stdout.write(f"✔ Municipio {municipio.id}: {len(localidades)} localidades")
                else:
                    self.stdout.write(self.style.WARNING(
                        f"⚠ Sin datos para municipio {municipio.id}. Respuesta: {data}"
                    ))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Error {response.status_code} en {url}"))

            if idx % 20 == 0:
                self.stdout.write(self.style.NOTICE(f"Progreso localidades: {idx}/{len(municipios)} municipios"))
        self.stdout.write(self.style.NOTICE(f"✔ Total de localidades cargadas: {total_loc}"))

    # ------------------------
    # Cargar Asentamientos
    # ------------------------
    def cargar_asentamientos(self):
        total_asen = 0
        localidades = Localidad.objects.all()
        for idx, localidad in enumerate(localidades, start=1):
            clave = f"{localidad.municipio.estado.id}{localidad.municipio.cve_agem}{localidad.cve_loc}"
            url = f"https://gaia.inegi.org.mx/wscatgeo/mzea/{clave}"
            response = requests.get(url, verify=False)

            self.stdout.write(self.style.NOTICE(f"Consultando asentamientos: {url}"))

            if response.status_code == 200:
                data = response.json()
                if "datos" in data and data["datos"]:
                    asentamientos = [
                        Asentamiento(
                            id=f"{clave}{asent['cve_asen'].zfill(4)}",
                            cve_asen=asent["cve_asen"].zfill(4),
                            nombre=asent["nom_asen"],
                            localidad=localidad
                        )
                        for asent in data["datos"]
                    ]
                    Asentamiento.objects.bulk_create(asentamientos, ignore_conflicts=True)
                    total_asen += len(asentamientos)
                    self.stdout.write(f"✔ Localidad {localidad.id}: {len(asentamientos)} asentamientos")
                else:
                    self.stdout.write(self.style.WARNING(
                        f"⚠ Sin datos para localidad {localidad.id}. Respuesta: {data}"
                    ))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Error {response.status_code} en {url}"))

            if idx % 200 == 0:
                self.stdout.write(self.style.NOTICE(f"Progreso asentamientos: {idx}/{len(localidades)} localidades"))
        self.stdout.write(self.style.NOTICE(f"✔ Total de asentamientos cargados: {total_asen}"))
