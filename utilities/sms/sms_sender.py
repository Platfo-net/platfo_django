import logging


class SmsReceiver:
    def receive_sms(self, template_id=None, template_name=None, plain_text=None):
        raise NotImplementedError('To be implemented by subclasses')


def is_receiver_valid(receiver, template_id=None, template_name=None, plain_text=None):
    if (not (receiver.startswith('+989') and len(receiver) == 13)
            and not (receiver.startswith('09') and len(receiver) == 11)):
        logging.warning(
            'Invalid phone number', extra={
                'RECEIVER': receiver,
                'TEMPLATE_ID': template_id,
                'TEMPLATE_NAME': template_name,
                'PLAIN_TEXT': plain_text,
            })
        return False
    return True


def send(receiver: str, template_id: int = None, template_name: str = None, plain_text: str = None):
    from notification.models import SmsNotification

    if not is_receiver_valid(receiver, template_name, plain_text):
        return

    sms_object = SmsNotification(receiver=receiver, template_id=template_id, template_name=template_name,
                                 plain_text=plain_text)

    sms_object.save()
    sms_object.send()
    return sms_object
