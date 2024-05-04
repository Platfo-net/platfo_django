# import logging
#
# from celery.app import shared_task
#
# from utilities.sms.choices import SmsProviderName
# from utilities.sms.kave_negar_sms_sender import KaveNegarSmsSender
# from utilities.sms.sun_way_sms_sender import SunWaySmsSender
#
#
# @shared_task(rate_limit='30/s')
# def send_sms_task(receiver, template, template_args):
#     logging.info('Sending SMS', extra={'RECEIVER': receiver, 'TEMPLATE': template, })
#     if config.SMS_PROVIDER == SmsProviderName.KAVENEGAR:
#         KaveNegarSmsSender(receiver, template, template_args).send(fail_silently=False)
#     else:
#         SunWaySmsSender(receiver, template_name=template,
#                         template_args=template_args).send_single_message_to_single_number()
#
#
# @shared_task(rate_limit='30/s')
# def send_plain_text_sms_task(receiver, plain_text, sender=None):
#     logging.info('Sending SMS', extra={'RECEIVER': receiver, 'TEXT': plain_text, })
#
#     if config.SMS_PROVIDER == SmsProviderName.KAVENEGAR:
#         KaveNegarSmsSender(receiver, plain_text=plain_text,
#                            sender=sender).send_plain_text(fail_silently=False)
#     else:
#         SunWaySmsSender(receiver, plain_text=plain_text,
#                         sender=sender).send_single_message_to_single_number()
#
#
# @shared_task(rate_limit='30/s')
# def send_otp_sms_task(receiver, plain_text, sender=None):
#     logging.info('Sending SMS', extra={'RECEIVER': receiver, 'TEXT': plain_text, })
#
#     if config.SMS_OTP_PROVIDER == SmsProviderName.KAVENEGAR:
#         KaveNegarSmsSender(receiver, plain_text=plain_text,
#                            sender=sender).send_plain_text(fail_silently=False)
#     else:
#         SunWaySmsSender(receiver, plain_text=plain_text,
#                         sender=sender).send_single_message_to_single_number()
