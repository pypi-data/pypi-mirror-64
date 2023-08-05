
class DeferredService:

    _service = None

    def __init__(self, service_ptr, *args, **kwargs):
        self._service_ptr = service_ptr
        self._args = args
        self._kwargs = kwargs
        self._service = None

    def _get(self):

        from .settings import adsocket_settings
        return self._service_ptr(
            driver=adsocket_settings.driver,
            **adsocket_settings.driver_options
        )

    def __getattr__(self, item):
        if not self._service:
            self._service = self._get()
        return getattr(self._service, item)
