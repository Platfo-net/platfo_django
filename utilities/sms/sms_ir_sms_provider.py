import logging

from django.conf import settings

from sms_ir import SmsIr


class SmsIrSender:
    def __init__(self, receiver, template_id=None, plain_text=None):
        self._sms_ir = SmsIr(api_key=settings.SMS_IR_API_KEY)
        self._receiver = receiver
        self._template_id = template_id
        self._parameters = [{'name': 'CODE', 'value': str(plain_text)}]
        self._plain_text = plain_text

    def send_verify_sms(self, fail_silently=True):
        try:
            if not self._receiver:
                raise ValueError('Receiver of sms must be specified')
            self._sms_ir.send_verify_code(number=self._receiver,
                                          template_id=self._template_id,
                                          parameters=self._parameters)
        except Exception as e:
            logging.exception('Could not send sms', extra={
                'MESSAGE': str(e),
            })
            if not fail_silently:
                raise

    def send_plain_text_sms(self, fail_silently=True):
        try:
            if not self._receiver:
                raise ValueError('Receiver of sms must be specified')
            self._sms_ir.send_sms(number=self._receiver,
                                  message=self._plain_text)
        except Exception as e:
            logging.exception('Could not send sms', extra={
                'TEXT': self._plain_text,
                'MESSAGE': str(e),
            })
            if not fail_silently:
                raise
