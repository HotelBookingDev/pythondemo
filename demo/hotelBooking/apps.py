from django.apps import AppConfig


class HotelbookingConfig(AppConfig):
    app_label = 'hotelBooking'
    name = 'hotelBooking'

    def ready(self):
        import hotelBooking.signals.handlers
