from app.services.reporte_gerencia_service import ReporteGerenciaService
from app.services.reporte_impulse_service import ReporteImpulseService
from app.services.reporte_promesas_service import ReportePromesasService


class FakeReporteRepository:
    def obtener_alerta_promesas_pago(self):
        return [
            {
                "dni": "12345678",
                "telefono": "999888777",
                "nombre_asesor": "Ana",
                "monto_pago": 100,
                "fecha_pago": "2026-07-18",
                "tipificacion_homologada": "PROMESA DE PAGO",
                "observacion": "Pagará por la tarde",
                "nivel_alerta": "VENCE HOY",
            }
        ]

    def obtener_reporte_impulse(self, *args):
        return [
            {
                "fecha_gestion": "2026-07-18 10:00:00",
                "dni": "12345678",
                "telefono": "999888777",
                "status_homologado": "DIRECTO",
                "tipificacion_homologada": "PROMESA DE PAGO",
                "nombre_asesor": "Ana",
            }
        ]

    def obtener_reporte_gerencia_asesores(self, *args):
        return [
            {
                "fecha": "2026-07-18",
                "nombre_asesor": "Ana",
                "total_gestiones": 10,
                "contactos_directos": 4,
                "contactos_indirectos": 2,
                "no_contactos": 4,
                "total_promesas": 3,
                "monto_prometido": 500,
                "clientes_unicos": 8,
            },
            {
                "fecha": "2026-07-18",
                "nombre_asesor": "Luis",
                "total_gestiones": 7,
                "contactos_directos": 2,
                "contactos_indirectos": 1,
                "no_contactos": 4,
                "total_promesas": 1,
                "monto_prometido": 100,
                "clientes_unicos": 6,
            },
        ]


def test_reporte_promesas_incluye_alerta_y_observacion():
    servicio = ReportePromesasService(FakeReporteRepository())
    html = servicio.generar_html(servicio.obtener_datos())
    assert "Alerta de promesas de pago" in html
    assert "VENCE HOY" in html
    assert "Pagará por la tarde" in html


def test_reporte_impulse_incluye_totales_y_detalle():
    servicio = ReporteImpulseService(FakeReporteRepository())
    html = servicio.generar_html(servicio.obtener_datos())
    assert "Reporte de gestiones realizadas - Impulse" in html
    assert "Clientes únicos: 1" in html
    assert "12345678" in html


def test_reporte_gerencia_calcula_ranking_diario():
    servicio = ReporteGerenciaService(FakeReporteRepository())
    datos = servicio.obtener_datos()
    assert [fila["ranking_diario"] for fila in datos] == [1, 2]
    assert "Reporte gerencial" in servicio.generar_html(datos)
