from re import A
from django.db.models.query_utils import DeferredAttribute
from numpy.core.getlimits import _fr1
from os import symlink
import pandas as pd
import json
import requests
from datetime import datetime
from .models import *
import currency
# from nh-currency impirt Currency
import pycountry


def get_parts(file_name):
    name_parts = {} 
    parts = (file_name.split('.')[0]).split('_')
    p_s, p_e, c, t = parts[-1].split('-')[0], parts[-1].split('-')[1], parts[-2], parts[-3] 
    datetimeobj = datetime.strptime(p_e,'%Y%m%d')
    name_parts['period_end'] = datetimeobj.strftime('%Y-%m-%d')
    datetimeobj = datetime.strptime(p_s,'%Y%m%d')
    name_parts['period_start'] = datetimeobj.strftime('%Y-%m-%d')
    name_parts['territory'] = t
    name_parts['currency'] = c
    return name_parts

def save_obj(cur_name, cur_symbol, ter_alpha3, ter_alpha2, ter_name, name_parts):
    cur_obj = Currency.objects.create(name = cur_name, symbol = cur_symbol, code = name_parts['currency'])
    ter_obj = Territory.objects.create(name = ter_name, code_2 = ter_alpha2, code_3 = ter_alpha3, local_currency = cur_obj)
    cur_obj.save()
    ter_obj.save()
    dsr_obj = DSR.objects.create(period_start = name_parts['period_start'], period_end = name_parts['period_end'], currency = cur_obj, territory = ter_obj)
    dsr_obj.save()


def get_more_info(name_parts):
    code = name_parts['currency']
    cur_name=currency.name(code)
    cur_symbol=currency.symbol(code)
    code2=name_parts['territory']
    country=pycountry.countries.get(alpha_2=code2)
    ter_alpha2 = country.alpha_2
    ter_alpha3 = country.alpha_3
    ter_name = country.name
    save_obj(cur_name, cur_symbol, ter_alpha3, ter_alpha2, ter_name, name_parts)


def insert (file_name, file_path,count):

    #import pdb; pdb.set_trace()
    name_parts = get_parts(file_name)
    get_more_info(name_parts)  #It will call save object for currecny and territory at the end
    tsv_read = pd.read_csv(file_path, sep='\t')
    tsv_read.fillna(0, inplace = True)
    tsv_read.drop_duplicates(subset=['dsp_id'],inplace=True)

    for i in range(0,len(tsv_read)):
        if (Resource.objects.filter(dsp_id = tsv_read['dsp_id'][i])):
            dsrs_obj = Resource.objects.get(dsp_id=tsv_read['dsp_id'][i])
            dsrs_obj.dsrs = dsrs_obj.dsrs + ' , ' + str(count)
            dsrs_obj.save()
            
        else:
            # import pdb;pdb.set_trace()
            try:
                dsr_instance=DSR.objects.get(id=int(count))
            except:
                dsr_instance=None
            if dsr_instance:
                res_obj = Resource.objects.create(dsr_key=dsr_instance,dsp_id = tsv_read['dsp_id'][i], title = tsv_read['title'][i], artists = tsv_read['artists'][i],
                isrc = tsv_read['isrc'][i], usages = tsv_read['usages'][i], revenue = tsv_read['revenue'][i], dsrs = count)
                res_obj.save()


def main():
    # import pdb;pdb.set_trace()
    File_dir_obj = File_dir.objects.filter(is_read=False)

    if(File_dir_obj):
        for i in range(len(File_dir_obj)):
            count = File_dir_obj[i].id
            # File_dir_obj_read = File_dir.objects.filter(is_read=True)
            # count = len(File_dir_obj_read) + 1
            File_name_obj_i = File_dir.objects.get(id = count)
            file_name = File_name_obj_i.file_name
            file_path=File_name_obj_i.path+file_name
            insert(file_name, file_path, count)
            File_name_obj_i.is_read = True
            File_name_obj_i.save()
            main()             
    else:
        print("All files are being read")

main()