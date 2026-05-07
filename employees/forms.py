from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "full_name",
            "employee_id",
            "company_name",
            "company_address",
            "department",
            "phone",
            "email",
            "joining_date",
            "status",
            "employee_photo",
        ]
        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
            "company_address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["employee_id"].disabled = True
            self.fields["employee_id"].help_text = "Employee ID is permanent because QR codes use it in the verification URL."
        base_classes = (
            "w-full rounded-lg border border-cyan-400/20 bg-slate-950/70 px-4 py-3 "
            "text-slate-100 outline-none transition placeholder:text-slate-500 "
            "focus:border-cyan-300 focus:ring-2 focus:ring-cyan-400/30"
        )
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", base_classes)
