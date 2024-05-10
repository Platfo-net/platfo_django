from django.utils.translation import gettext_lazy as _

from utilities.enums import ModelEnum


class CurrencyChoices(ModelEnum):
    IRT = "IRT", _("IRT")


class OrderStatusChoices(ModelEnum):
    UNPAID = "UNPAID", _("Unpaid")
    PAYMENT_CHECK = "PAYMENT_CHECK", _("PaymentCheck")
    ACCEPTED = "ACCEPTED", _("Accepted")
    PREPARATION = "PREPARATION", _("Preparation")
    SENT = "SENT", _("Sent")
    DECLINED = "DECLINED", _("Declined")
    PAYMENT_DECLINED = "PAYMENT_DECLINED", _("PaymentDeclined")
