import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import keras
import json
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from .core.data_processor import DataLoader
from .core.model import Model
from .core.gdata import gdata
from .core.pygdata import pygdata
from ..models import Company

def plot_results(predicted_data, true_data):   # predicted_data与true_data：同长度一维数组
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()

# predicted_data每个元素的长度必须为prediction_len
def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
	# 填充预测列表，使其在图表中移动到正确的开始位置
    for i, data in enumerate(predicted_data):    # data为一维数组，长度为prediction_len。predicted_data：二维数组，每个元素为list
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')    # padding + data：list拼接操作
        plt.legend()
    plt.show()

def get_parent_dir():   # 当前文件的父目录绝对路径
    return os.path.dirname(__file__)

def get_config_path():  # config.json的绝对路径
    root_dir = get_parent_dir()
    return os.path.join(root_dir, "config.json")

def get_data_path():  # data目录的绝对路径
    root_dir = get_parent_dir()
    return os.path.join(root_dir, "data")    

def isGood(stock_code):  # 按当时的good_models,现直接用saved_models
    if os.path.exists(os.path.join(get_parent_dir(),os.path.join('saved_models', stock_code + ".h5"))):
        return True
    else:
        return False

def pytrain_model(stock_code, predict=False):
    pygdata(get_data_path(),stock_code)

# 只用于训练模型，但同时可根据参数进行模型的评估
def train_model(stock_code, predict=False):  # 训练指定股票代码的模型
    '''
    训练并保存模型，同时根据测试数据对模型进行评估（绘图方式）
    '''
    gdata(get_data_path(),stock_code)
    configs = json.load(open(get_config_path(), 'r'))
    if not os.path.exists(os.path.join(get_parent_dir(),configs['model']['save_dir'])):
        os.makedirs(os.path.join(get_parent_dir(),configs['model']['save_dir']))  # 创建保存模型的目录

    split = configs['data']['train_test_split']
    if not predict:
        split = 1  # 若不评估模型准确度，则将全部历史数据用于训练

    data = DataLoader(  # 从本地加载训练和测试数据
        os.path.join(get_parent_dir(),os.path.join('data', stock_code + ".csv")),  # configs['data']['filename']
        split,
        configs['data']['columns']  # 选择某些列的数据进行训练
    )

    model = Model()
    
    if os.path.exists(os.path.join(get_parent_dir(),os.path.join('saved_models', stock_code + ".h5"))):
        x, y = data.get_train_data(
	        seq_len = configs['data']['sequence_length'],
	        normalise = configs['data']['normalise']
        )
        keras.backend.clear_session()
        model.load_model(os.path.join(get_parent_dir(),os.path.join('saved_models', stock_code + ".h5")))
        # 记忆训练
        model.train(
            x,
            y,
            epochs = configs['training']['epochs'],
            batch_size = configs['training']['batch_size'],
            save_dir=os.path.join(get_parent_dir(),configs['model']['save_dir']),
            save_name=stock_code
        )
    
    else:
        model.build_model(configs)  # 根据配置文件新建模型
        # 训练模型：
        # 记忆外生成训练
        steps_per_epoch = math.ceil(
            (data.len_train - configs['data']['sequence_length']) / configs['training']['batch_size'])
        model.train_generator(
            data_gen=data.generate_train_batch(
                seq_len=configs['data']['sequence_length'],
                batch_size=configs['training']['batch_size'],
                normalise=configs['data']['normalise']
            ),
            epochs=configs['training']['epochs'],
            batch_size=configs['training']['batch_size'],
            steps_per_epoch=steps_per_epoch,
            save_dir=os.path.join(get_parent_dir(),configs['model']['save_dir']),
            save_name=stock_code
        )

    # 预测
    if predict:
        x_test, y_test = data.get_test_data(
            seq_len=configs['data']['sequence_length'],
            normalise=configs['data']['normalise']
        )
       
        predictions = model.predict_sequences_multiple(x_test, configs['data']['sequence_length'],
                                                       configs['data']['sequence_length'])
        # plot_results_multiple(predictions, y_test, configs['data']['sequence_length'])
        print("训练：\n", predictions)


# 对指定公司的股票进行预测
def prediction(stock_code, good, pre_len=30, real=True, plot=False):
    '''
    使用保存的模型，对输入数据进行预测
    '''
    config_path = get_config_path()
    configs = json.load(open(config_path, 'r'))
    data = DataLoader(
        os.path.join(get_data_path(), stock_code + ".csv"),  # configs['data']['filename']
        configs['data']['train_test_split'],
        configs['data']['columns']
    )
    
    file_path = os.path.join(get_parent_dir(),os.path.join("saved_models",stock_code + ".h5"))
    if good == 'on':
        file_path = os.path.join(get_parent_dir(),os.path.join("saved_models",stock_code + ".h5"))  # 按当时的good_models,现直接用saved_models
    model = Model()
    keras.backend.clear_session()
    model.load_model(file_path)  # 根据配置文件新建模型

    # predict_length = configs['data']['sequence_length']   # 预测长度
    predict_length = pre_len
    if real:  # 用最近一个窗口的数据进行预测，没有对比数据
        win_position = -1
    else:  # 用指定位置的一个窗口数据进行预测，有对比真实数据（用于绘图对比）
        win_position = -configs['data']['sequence_length']

    x_test, y_test = data.get_test_data(
        seq_len=configs['data']['sequence_length'],
        normalise=False
    )

    x_test = x_test[win_position]
    x_test = x_test[np.newaxis, :, :]
    if not real:
        y_test_real = y_test[win_position:win_position + predict_length]

    base = x_test[0][0][0]
    print("base value:\n", base)

    x_test, y_test = data.get_test_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )
    x_test = x_test[win_position]
    x_test = x_test[np.newaxis, :, :]

    predictions = model.predict_1_win_sequence(x_test, configs['data']['sequence_length'], predict_length)
    # 反归一化
    predictions_array = np.array(predictions)
    predictions_array = base * (1 + predictions_array)
    predictions = predictions_array.tolist()

    print("预测数据:\n", predictions)
    if not real:
        print("真实数据：\n", y_test_real)

    # plot_results_multiple(predictions, y_test, predict_length)
    if plot:
        if real:
            plot_results(predictions, [])
        else:
            plot_results(predictions, y_test_real)

    return format_predictions(predictions)

def format_predictions(predictions):    # 给预测数据添加对应日期
    date_predict = []
    cur = datetime.now()
    cur += timedelta(days=1)
    counter = 0

    while counter < len(predictions):
        if cur.isoweekday()  == 6:
            cur = cur + timedelta(days=2)
        if cur.isoweekday()  == 7:
            cur = cur + timedelta(days=1)
        date_predict.append([cur.strftime("%Y-%m-%d"),predictions[counter]])
        cur = cur + timedelta(days=1)
        counter += 1

    return date_predict

# 二维数组：[[data,value],[...]]
def get_hist_data(stock_code, good, recent_day=30):  # 获取某股票，指定天数的历史close数据,包含日期
    if good == 'on':
        gdata(get_data_path(),stock_code)
    root_dir = get_parent_dir()
    file_path = os.path.join(root_dir, "data/" + stock_code + ".csv")
    cols = ['Date', 'Close']
    data_frame = pd.read_csv(file_path)
    close_data = data_frame.get(cols).values[-recent_day:]
    print(close_data)
    return close_data.tolist()

def train_all_stock():
    companies = Company.objects.all().order_by('stock_code')
    for row in companies:
        train_model(row.stock_code)

    return 0

def predict_all_stock(pre_len=10):
    companies = Company.objects.all().order_by('stock_code')
    predict_list = []
    for row in companies:
        predict_list.append(prediction(stock_code=row.stock_code, real=True, pre_len=pre_len))

    return predict_list

if __name__ == '__main__':
    predict_all_stock()