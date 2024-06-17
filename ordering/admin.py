from django.contrib import admin
from .models import Order, OrderItem
import openpyxl
from django.http import HttpResponse
import csv
# Register your models here.


def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Orders.csv'

    writer = csv.writer(response)

    columns = ['ID', 'Name', 'Phone', 'Address', 'Postal Code',
               'Province', 'City', 'Paid', 'Created']
    writer.writerow(columns)

    for order in queryset:
        created = str(order.created.replace(tzinfo=None))
        writer.writerow(
            [order.id, order.name, order.phone, order.address, order.postal_code,
             order.province, order.city, order.paid, created]
        )
    return response


export_csv.short_description = 'Export to CSV'


def export_excel(modeladmin, request, queryser):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Orders.xlsx'

    work_book = openpyxl.Workbook()
    work_sheet = work_book.active
    work_sheet.title = 'Orders'

    columns = ['ID', 'Name', 'Phone', 'Address', 'Postal Code',
               'Province', 'City', 'Paid', 'Created']
    work_sheet.append(columns)

    for order in queryser:
        created = str(order.created.replace(tzinfo=None))
        work_sheet.append(
            [order.id, order.name, order.phone, order.address, order.postal_code,
             order.province, order.city, order.paid, created]
        )
    work_book.save(response)
    return response


export_excel.short_description = 'Export to Excel'


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'postal_code', 'province', 'city',
                    'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_excel, export_csv]
