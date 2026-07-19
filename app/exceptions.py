class AutomatizacionError(Exception):
    """Excepcion base controlada del proyecto."""


class ConfiguracionError(AutomatizacionError):
    pass


class SourceDatabaseConnectionError(AutomatizacionError):
    pass


class TargetDatabaseConnectionError(AutomatizacionError):
    pass


class StoredProcedureError(AutomatizacionError):
    pass


class ValidacionGestionError(AutomatizacionError):
    pass


class ReporteError(AutomatizacionError):
    pass


class NotificacionError(AutomatizacionError):
    pass
