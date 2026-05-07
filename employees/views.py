from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm
from .models import Employee


def admin_required(view_func):
    protected_view = login_required(view_func)
    return user_passes_test(lambda user: user.is_staff, login_url="login")(protected_view)


@admin_required
def home(request):
    context = {
        "total_employees": Employee.objects.count(),
        "active_employees": Employee.objects.filter(status=Employee.Status.ACTIVE).count(),
        "inactive_employees": Employee.objects.filter(status=Employee.Status.INACTIVE).count(),
        "recent_employees": Employee.objects.order_by("-created_at")[:5],
    }
    return render(request, "employees/home.html", context)


@admin_required
def employee_list(request):
    employees = Employee.objects.all()
    query = request.GET.get("q", "").strip()
    if query:
        employees = employees.filter(full_name__icontains=query) | employees.filter(employee_id__icontains=query)
    return render(request, "employees/employee_list.html", {"employees": employees, "query": query})


@admin_required
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, "Employee created and QR code generated.")
            return redirect("employees:employee_detail", pk=employee.pk)
    else:
        form = EmployeeForm()
    return render(request, "employees/employee_form.html", {"form": form, "title": "Add Employee"})


@admin_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, "Employee updated. Existing QR URL now shows the latest database data.")
            return redirect("employees:employee_detail", pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, "employees/employee_form.html", {"form": form, "employee": employee, "title": "Edit Employee"})


@admin_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/employee_detail.html", {"employee": employee})


@admin_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted.")
        return redirect("employees:employee_list")
    return render(request, "employees/employee_confirm_delete.html", {"employee": employee})


def verify_employee(request, employee_id):
    employee = Employee.objects.filter(employee_id=employee_id).first()
    return render(request, "employees/verify.html", {"employee": employee})


@admin_required
def download_qr(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if not employee.qr_code:
        raise Http404("QR code not found.")
    response = FileResponse(employee.qr_code.open("rb"), as_attachment=True, filename=f"{employee.employee_id}-qr.png")
    return response
