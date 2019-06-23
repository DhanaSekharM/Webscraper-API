from django.http import HttpResponse
from fcm_django.models import FCMDevice, Device, FCMDeviceManager


def send_notifications(title, message):
    device = FCMDevice.objects.get(id=1)
    device.send_message(title=title, body=message, data={"test": "test"})
