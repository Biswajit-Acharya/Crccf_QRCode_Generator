from io import BytesIO

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models


class Employee(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    full_name = models.CharField(max_length=150)
    employee_id = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=150)
    company_address = models.TextField()
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    joining_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    employee_photo = models.ImageField(upload_to="employee_photos/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"

    @property
    def verification_path(self):
        return f"/employee/verify/{self.employee_id}/"

    @property
    def verification_url(self):
        return f"{settings.SITE_URL}{self.verification_path}"

    def save(self, *args, **kwargs):
        qr_file_name = f"{self.employee_id}.png"
        if not self.qr_code or self.qr_code.name != f"qr_codes/{qr_file_name}":
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(self.verification_url)
            qr.make(fit=True)
            image = qr.make_image(fill_color="#00f5ff", back_color="#020617").convert("RGB")
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            self.qr_code.save(qr_file_name, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)
