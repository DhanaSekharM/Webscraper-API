from django.http import HttpResponse
from fcm_django.models import FCMDevice, Device, FCMDeviceManager


def send_notifications():
    device = FCMDevice.objects.get(id=1)
    device.send_message(title="Title", body="Message", data={"test": "test"})
