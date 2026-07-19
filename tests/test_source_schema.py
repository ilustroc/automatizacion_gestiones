from app.repositories.source_schema_repository import SourceSchemaRepository


class FakeDb:
    class Config:
        name = "escarperu_software"

    config = Config()

    def ejecutar_consulta(self, sql, parametros=None):
        if sql.startswith("SHOW COLUMNS"):
            return [{"Field": "id"}, {"Field": "fecha_gestion"}, {"Field": "dni"}]
        return []


def test_diagnostico_identifica_columnas_faltantes_con_nombre_preciso():
    faltantes = SourceSchemaRepository(FakeDb()).columnas_faltantes_gestiones()
    assert "telefono" in faltantes
    assert "updated_at" in faltantes
    assert "id" not in faltantes
