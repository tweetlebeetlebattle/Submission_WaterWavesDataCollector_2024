class SharedService:
    def __init__(self):
        from service.service_gif import MeteoGifService
        from service.service_GSio import GSioService
        from service.service_HTML import MeteoHTMLService
        from service.service_utils import ServiceUtils
        self.serv_HTML = MeteoGifService()
        self.serv_GSio = GSioService()
        self.serv_gif = MeteoHTMLService()
        self.serv_utils = ServiceUtils()