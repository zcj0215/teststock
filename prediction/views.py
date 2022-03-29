from django.shortcuts import render, redirect
from .lstm_prediction import *

from django.views.generic import ListView
from astocks.models import StockList
# from django.http import HttpResponse

class StockListView(ListView):
    model = StockList
    context_object_name = 'stocks'
    template_name = 'prediction/index.html'


# --------------- MAIN WEB PAGES -----------------------------
def redirect_root(request):
    return redirect('/prediction/pred')

def index(request):
	return render(request, 'prediction/index.html') 

def pred(request):
    return render(request, 'prediction/prediction.html')

def contact(request):
	return render(request, 'prediction/contact.html')

def search(request, se, stock_symbol):
	import json
	predicted_result_df = lstm_prediction(se, stock_symbol)
	return render(request, 'prediction/search.html', {"predicted_result_df": predicted_result_df})








""" from django.shortcuts import render

# Create your views here.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM



# 将一维数据创建为时间序列数据集的功能
def new_dataset(dataset, step_size):
	data_X, data_Y = [], []
	for i in range(len(dataset)-step_size-1):
		a = dataset[i:(i+step_size), 0]
		data_X.append(a)
		data_Y.append(dataset[i + step_size, 0])
	return np.array(data_X), np.array(data_Y)

# 此函数可用于从任何一维数组创建时间序列数据集	

def predict():
    # 可重复性
    np.random.seed(7) 
    # IMPORTING DATASET 
    dataset = pd.read_csv('apple_share_price.csv', usecols=[1,2,3,4])
    dataset = dataset.reindex(index = dataset.index[::-1]) """