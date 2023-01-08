import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import math
import numpy as np
import datetime as dt
from numpy import newaxis
from .utils import Timer
from keras.layers import Dense, Activation, Dropout, LSTM
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint

class Model():
	"""用于构建和推断lstm模型的类"""

	def __init__(self):
		self.model = Sequential()

	def load_model(self, filepath):
		'''
		从本地保存的模型参数来加载模型
		filepath: .h5 格式文件
		'''
		print('[Model] 从文件%s加载模型 ' % filepath)
		self.model = load_model(filepath)

	def build_model(self, configs):
		"""
		新建一个模型
		configs:配置文件
		"""
		timer = Timer()
		timer.start()

		for layer in configs['model']['layers']:
			neurons = layer['neurons'] if 'neurons' in layer else None
			dropout_rate = layer['rate'] if 'rate' in layer else None
			activation = layer['activation'] if 'activation' in layer else None
			return_seq = layer['return_seq'] if 'return_seq' in layer else None
			input_timesteps = layer['input_timesteps'] if 'input_timesteps' in layer else None
			input_dim = layer['input_dim'] if 'input_dim' in layer else None

			if layer['type'] == 'dense':
				self.model.add(Dense(neurons, activation=activation))
			if layer['type'] == 'lstm':
				self.model.add(LSTM(neurons, input_shape=(input_timesteps, input_dim), return_sequences=return_seq))
			if layer['type'] == 'dropout':
				self.model.add(Dropout(dropout_rate))

		self.model.compile(loss=configs['model']['loss'], optimizer=configs['model']['optimizer'])

		print('[Model] 模型已编译')
		timer.stop()	#输出构建一个模型耗时

	def train(self, x, y, epochs, batch_size, save_dir,save_name):
		timer = Timer()
		timer.start()
		print('[Model] 正在训练已开始')
		print('[Model] %s epochs, %s batch size' % (epochs, batch_size))
		
		# save_fname = os.path.join(save_dir, '%s-e%s.h5' % (dt.datetime.now().strftime('%d%m%Y-%H%M%S'), str(epochs)))
		save_fname = os.path.join(save_dir, save_name+'.h5')
		callbacks = [
			EarlyStopping(monitor='val_loss', patience=2),
			ModelCheckpoint(filepath=save_fname, monitor='val_loss', save_best_only=True)
		]
		self.model.fit(
			x,
			y,
			epochs=epochs,
			batch_size=batch_size,
			callbacks=callbacks
		)
		self.model.save(save_fname)	#保存训练好的模型

		print('[Model] 训练已完成。模型另存为 %s' % save_fname)
		timer.stop()	#输出训练耗时

	def train_generator(self, data_gen, epochs, batch_size, steps_per_epoch, save_dir,save_name):
		'''
		由data_gen数据产生器来，逐步产生训练数据，而不是一次性将数据读入到内存
		'''
		timer = Timer()
		timer.start()
		print('[Model] 正在训练已开始')
		print('[Model] %s epochs, %s batch size, %s batches per epoch' % (epochs, batch_size, steps_per_epoch))
		
		# save_fname = os.path.join(save_dir, '%s-e%s.h5' % (dt.datetime.now().strftime('%d%m%Y-%H%M%S'), str(epochs)))
		save_fname = os.path.join(save_dir, save_name+'.h5')
		callbacks = [
			ModelCheckpoint(filepath=save_fname, monitor='loss', save_best_only=True)
		]
		self.model.fit_generator(
			data_gen,
			steps_per_epoch=steps_per_epoch,
			epochs=epochs,
			callbacks=callbacks,
			workers=1
		)
		
		print('[Model] 训练已完成。模型另存为 %s' % save_fname)
		timer.stop()

    # data必须是三维数据，即shape:(a,b,c)
	def predict_point_by_point(self, data):
		# 根据最后一个真实数据序列预测每个时间步，实际上每次只预测一步
		print('[Model] 逐点预测...')
		predicted = self.model.predict(data)    # data有多少行就输出多少个预测值,返回的预测值是一个2维数组:(a,1)	a:为data的行数
		predicted = np.reshape(predicted, (predicted.size,)) # 这里将二维数组，变成一维数组
		return predicted    # 返回一维数组，元素个数与data的a相同

    # 对data进行多段预测，每段预测基于一个窗口大小（window_size）的数据，然后输出prediction_len长的预测值（一维数组）
    # 再从上一个窗口移动prediction_len的长度，得到下一个窗口的数据，并基于该数据再预测prediction_len长的预测值
    # 所以prediction_len决定了窗口的移位步数，每次的窗口大小是一样的，所以最后预测的段数 = 窗口个数/预测长度
    # 相当于多次调用predict_1_win_sequence方法
	def predict_sequences_multiple(self, data, window_size, prediction_len):
		# 在将预测向前移动50步之前，预测50步序列
		print('[Model] 预测多个序列...')
		prediction_seqs = []
		for i in range(int(len(data)/prediction_len)):
			curr_frame = data[i*prediction_len]
			predicted = []
			for j in range(prediction_len):
				predicted.append(self.model.predict(curr_frame[newaxis,:,:])[0,0])  # newaxis：增加新轴，使得curr_frame变成(1,x,x)三维数据
				curr_frame = curr_frame[1:]
				curr_frame = np.insert(curr_frame, [window_size-2], predicted[-1], axis=0)
			prediction_seqs.append(predicted)
		return prediction_seqs

    # 输入一个窗口的数据，指定预测的长度，data:依旧是三维数组(1,win_len,fea_len)
    # 返回预测数组
	def predict_sequence_full(self, data, window_size): # window_size：为输入数据的长度
		# 每次将窗口移动1个新预测，在新窗口上重新运行预测
		print('[Model] 预测全序列...')
		curr_frame = data[0]    # 基于data[0]一个窗口的数据，来预测len(data)个输出
		predicted = []
		for i in range(len(data)):
			predicted.append(self.model.predict(curr_frame[newaxis,:,:])[0,0])  # append了一个预测值（标量）
			curr_frame = curr_frame[1:]
			curr_frame = np.insert(curr_frame, [window_size-2], predicted[-1], axis=0)  # 插入位置[window_size-2]:curr_frame的末尾，predicted[-1]：插入值
		return predicted

    # 输入一个窗口的数据，指定预测的长度，data:依旧是三维数组(1,win_len,fea_len)
    # 返回预测数组
	def predict_1_win_sequence(self, data, window_size,predict_length): # window_size：data的窗口大小
		# 每次将窗口移动1个新预测，在新窗口上重新运行预测
		curr_frame = data[0]
		predicted = []
		for i in range(predict_length): # range(len(data))
			predicted.append(self.model.predict(curr_frame[newaxis,:,:])[0,0])  # append了一个预测值（标量）
			curr_frame = curr_frame[1:]
			curr_frame = np.insert(curr_frame, [window_size-2], predicted[-1], axis=0)  # 插入位置[window_size-2]:curr_frame的末尾，predicted[-1]：插入值
		return predicted