from django.template.loader import render_to_string
from django.conf import settings


CAMPOS_ENCABEZADOS = (
    ("clave_proveedor", "str"),
    ("no_siniestro", "str"),
    ("orden_pago", "str"),
)


def generar_addenda(diccionario):
    return render_to_string("cfdi/addendas/multiasistencia.xml", diccionario)
