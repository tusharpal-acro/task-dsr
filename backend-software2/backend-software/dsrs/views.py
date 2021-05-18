# # from dsrs import script
# from rest_framework import viewsets
# # from django.http import HttpResponse
# # import json
# from dsrs.script import *
# from . import models, serializers


# class DSRViewSet(viewsets.ModelViewSet):
#     queryset = models.DSR.objects.all()
#     serializer_class = serializers.DSRSerializer


# from dsrs import script
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from rest_framework import viewsets
from django.http import HttpResponse
from django.shortcuts import render,redirect
# import json
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView,RetrieveAPIView
import django
# from datetime import date
# from dsrs.script import get_partss
try:
    # import pdb;pdb.set_trace()
    from dsrs.script import *

except Exception as e:
    print('script will not run until the migration first migrate then run again')
from django.core import serializers as ser
from . import models, serializers


class DSRViewSet(viewsets.ModelViewSet):
    queryset = models.DSR.objects.all()
    serializer_class = serializers.DSRSerializer


class DSRListAPIView(ListAPIView):
    queryset=models.DSR.objects.all()
    serializer_class=serializers.DSRSerializer

class DSRRetrieveAPIView(RetrieveAPIView):
    queryset=models.DSR.objects.all()
    serializer_class=serializers.DSRSerializer
    lookup_field='id'

def RESOURCEView(request,number):
    # import pdb; pdb.set_trace()
    ter=request.GET.get('ter',None)
    p_s=request.GET.get('p_s',None)
    p_e=request.GET.get('p_e',None)
    no_of_resource=models.Resource.objects.all()
    no_of_resource=len(no_of_resource)
    percentile=int((no_of_resource*number)/100)
    if ter!=None and p_s!=None and p_e!=None:
        qs=models.Resource.objects.filter(dsr_key__territory__code_2=ter,dsr_key__period_start__startswith=p_s,dsr_key__period_end__startswith=p_e).order_by('-revenue')[:percentile]
    else:
        qs=models.Resource.objects.all().order_by('-revenue')[:percentile]

    qs_json = ser.serialize('json', qs)
    return HttpResponse(qs_json, content_type='application/json')
    
def delete_dsr_res(id, file_name):
    name_parts = get_parts(file_name)

    dsrs_obj = models.DSR.objects.filter(period_end = name_parts['period_end'], period_start = name_parts['period_start'], currency__code = name_parts['currency'], territory__code_2 = name_parts['territory'])
    dsrs_obj.delete()
    res_obj=models.Resource.objects.filter(dsrs__contains = id)
    res_obj.delete()

def list(request):
    file_dir=models.File_dir.objects.all()
    return render(request,'dsrs/file_dir_list.html',{'file_dir':file_dir})

def deleted(request,id):
    file_dir = models.File_dir.objects.get(id=id)
    file_name = file_dir.file_name 
    delete_dsr_res(id, file_name)
    file_dir.delete()
    return redirect('/list')