import codecs
import csv
import io

import PyPDF2 as PyPDF2
import pandas as pd

import tabula
from tablib import Dataset

from django.http.response import HttpResponse
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from xlrd.timemachine import xrange

from users.models import CustomUser, Person
from users.serializers import CustomTokenObtainPairSerializer, UploadFileSerializer

import xlwt

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


class CustomTokenObtainPairView(TokenObtainPairView):

    def get_serializer_class(self):
        if 'phone' in self.request.data:
            return CustomTokenObtainPairSerializer
        return TokenObtainPairSerializer


class UploadFileView(CreateAPIView):
    serializer_class = UploadFileSerializer

    def post(self, request):

        upload_file = request.FILES['import_file']
        if str(upload_file).split('.')[-1] == 'csv':
            data = csv.DictReader(codecs.iterdecode(upload_file, 'utf-8'), delimiter=',', quotechar='"')
            for row in data:
                _, created = CustomUser.objects.get_or_create(
                    email=row['First Name'],
                    password=row['Last Name'],
                )

        elif str(upload_file).split('.')[-1] == 'xls':
            print(upload_file)
            dataset = Dataset()
            import_data = dataset.load(upload_file.read(), format='xls')
            for data in import_data:
                _, created = CustomUser.objects.get_or_create(
                    email=data['First Name'],
                    password=data['Last Name'],
                )

        # elif str(upload_file).split('.')[-1] == 'pdf':
        #     import PyPDF2
        #     # print(upload_file, type(upload_file))
        #     # fileReader = PyPDF2.PdfFileReader(upload_file)
        #     # for page in range(fileReader.numPages):
        #     #     print(fileReader.getPage(page).extractText().split('\n'), '-------')
        #     table = tabula.read_pdf(upload_file)
        #     print(table)
        #     for column in table:
        #         _, created = CustomUser.objects.get_or_create(
        #             first_name=column['First Name'],
        #             last_name=column['Last Name'],
        #         )
        # return HttpResponse("Completed", content_type="text/plain")


def export_csv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Email', 'Phone', 'Password'])

    for user in CustomUser.objects.all().values_list('email', 'phone', 'password'):
        writer.writerow(user)

    response['Content-Disposition'] = 'attachment; filename="person.csv"'
    return response


def export_pdf(request):
    persons = Person.objects.all()

    html_string = render_to_string('pdf.html', {'persons': persons})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=persons.pdf'
    response['Content-Transfer-Encoding'] = 'utf-8'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Persons')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['First Name', 'Last Name']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = CustomUser.objects.all().values_list('first_name', 'last_name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response