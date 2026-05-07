from django.contrib import admin
from django.utils.html import format_html

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "employee_id", "company_name", "department", "status", "updated_at")
    list_filter = ("status", "department", "company_name")
    search_fields = ("full_name", "employee_id", "email", "phone", "department")
    readonly_fields = ("qr_preview", "created_at", "updated_at")
    fieldsets = (
        ("Employee Details", {"fields": ("full_name", "employee_id", "department", "joining_date", "status")}),
        ("Company", {"fields": ("company_name", "company_address")}),
        ("Contact", {"fields": ("phone", "email")}),
        ("Media", {"fields": ("employee_photo", "qr_preview", "qr_code")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="180" height="180" style="border-radius: 12px;" />', obj.qr_code.url)
        return "QR code will be generated after saving."

    qr_preview.short_description = "QR Preview"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj and "employee_id" not in readonly_fields:
            readonly_fields.append("employee_id")
        return readonly_fields
