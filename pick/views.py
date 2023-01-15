from django.shortcuts import render

# Create your views here.
import os
from astocks.models import Stocksz,Stockszc,Stocksh,Stockshk,Stockbj
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse

def readfile(mfn):
    '''
    以“只读”⽅式打开⽂件，读取文件所有行(直到结束符 EOF)
    :param mfn: 文件路经与文件名
    :return: 返回列表数据类型
    '''
    fp=open(mfn,'r',encoding='gbk')
    wls = fp.readlines()     #readlines把文本文件按行分割，并产生一个以每一行文本为一个元素的列表
    fp.close()
    return wls

def turnover(code,flag,data):
    if flag == 'SZ':
        if code[:2] == '30':  
            try:
                stock = get_object_or_404(Stockszc, code=code,date=data[0])
                stock.turnover = float(data[1])
                stock.save()
            except Http404:
                pass
        else:
            try:
                stock = get_object_or_404(Stocksz, code=code,date=data[0])
                stock.turnover = float(data[1])
                stock.save()
            except Http404:
                pass
    elif flag == 'SH':
        if code[:2] == '68':  
            try:
                stock = get_object_or_404(Stockshk, code=code,date=data[0])
                stock.turnover = float(data[1])
                stock.save()
            except Http404:
                pass
        else:     
            try:
                stock = get_object_or_404(Stocksh, code=code,date=data[0])
                stock.turnover = float(data[1])
                stock.save()
            except Http404:
                pass
    elif flag == 'BJ':
            try:
                stock = get_object_or_404(Stockbj, code=code,date=data[0])
                stock.turnover = float(data[1])
                stock.save()
            except Http404:
                pass

def home(request):
    return HttpResponse('选股！')            

def query(request):
    path =  os.path.dirname(__file__)
    filename = path+"\\Table.txt"
    fl = [];
    fl = readfile(filename)

    data_temp = []
    data_list = []
    for item in fl:
        if item[0:3] != '时间' and item[0:1] != '':
            if len(item) > 10:
                data_temp = item.split('\t')
                data_list.append([data_temp[0][0:10],data_temp[1]])


    for data in data_list:
        turnover('002305','SZ',data)

    return HttpResponse('执行完毕！')