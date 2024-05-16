from django.contrib import admin

from notification.models import SmsNotification


class SmsNotificationAdmin(admin.ModelAdmin):
    list_display = ['receiver', 'template_name', 'plain_text', 'datetime']
    search_fields = ['receiver', 'template_name', 'plain_text']
    readonly_fields = ['datetime']
    exclude = ['datetime']


admin.site.register(SmsNotification, SmsNotificationAdmin)
