import pandas
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import pylab
from sklearn.linear_model import LinearRegression

from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.api import Holt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

colors = ['black', 'blue', 'red', 'green', 'yellow', 'orange']

def f(x, data_min):
    return np.log(x + np.abs(data_min) + 1)

def f_inv(x, data_min):
    return np.exp(x) - np.abs(data_min) - 1

df = pandas.read_csv('data.txt', sep=" ", comment='#', header=None, usecols=range(1,3), names=['x', 'original'])

# Moving average
mas = [10, 30, 50]
fig, axes = plt.subplots(3, 1, figsize=(20,10))
fig.canvas.manager.set_window_title('MA')
fig.tight_layout(pad=5.0)
for i, ma in enumerate(mas):
    df[f'MA-{ma}'] = df['original'].rolling(ma).mean()
    df[f'original - MA-{ma}'] = df['original'] - df[f'MA-{ma}']
    df.plot(x='x', y=['original', f'MA-{ma}', f'original - MA-{ma}'], kind='line', ax=axes[i])
    axes[i].set_title(f'Moving average with window {ma}', fontweight='bold')

plt.savefig('ma.png')

# Centered moving average
cmas = [10, 30, 50]
fig, axes = plt.subplots(3, 1, figsize=(20,10))
fig.canvas.manager.set_window_title('CMA')
fig.tight_layout(pad=5.0)
for i, cma in enumerate(cmas):
    df[f'CMA-{cma}'] = df['original'].rolling(cma, center=True).mean()
    df[f'original - CMA-{cma}'] = df['original'] - df[f'CMA-{cma}']
    df.plot(x='x', y=['original', f'CMA-{cma}', f'original - CMA-{cma}'], kind='line', ax=axes[i])
    axes[i].set_title(f'Centered average with window {cma}', fontweight='bold')

plt.savefig('cma.png')

# Double moving average
dmas = [(10, 20), (30, 30), (50, 40)]
fig, axes = plt.subplots(3, 1, figsize=(20,10))
fig.canvas.manager.set_window_title('DMA')
fig.tight_layout(pad=5.0)
for i, (dma_alpha, dma_beta) in enumerate(dmas):
    df[f'DMA-{dma_alpha}-{dma_beta}'] = df['original'].rolling(dma_alpha).mean().rolling(dma_beta).mean()
    df[f'original - DMA-{dma_alpha}-{dma_beta}'] = df['original'] - df[f'DMA-{dma_alpha}-{dma_beta}']
    df.plot(x='x', y=['original', f'DMA-{dma_alpha}-{dma_beta}', f'original - DMA-{dma_alpha}-{dma_beta}'], kind='line', ax=axes[i])
    axes[i].set_title(f'Double average with first window {dma_alpha} and second window {dma_beta}', fontweight='bold')

plt.savefig('dma.png')

# Linear regression
X = df['x'].values.reshape(-1,1)

data = df['original'].values
data_min = data.min()
transformed_data = f(data,data_min).reshape(-1,1)

lr_model = LinearRegression()
lr_model.fit(X, transformed_data)

df['LR'] = f_inv(lr_model.predict(X), data_min)
df['original - LR'] = df['original'] - df['LR']

df.plot(x='x', y=['original', 'LR', 'original - LR'], kind='line', figsize=(20,10))
plt.title('Linear regression', fontweight='bold')
fig = pylab.gcf()
fig.canvas.manager.set_window_title('Linear regression')

plt.savefig('lr.png')

# Exponential smoothing
es_alphas = [0.2, 0.6, 'estimated']

fig = plt.figure('Exponential smoothing', figsize=(20,10))
plt.title('Exponential smoothing', fontweight='bold')
(line, ) = plt.plot(df['original'], color=colors[0])
legend = {'lines': [line], 'names': ['original']}
for i, es_alpha in enumerate(es_alphas):

    if es_alpha == 'estimated':
        es_model = SimpleExpSmoothing(df['original'], initialization_method=es_alpha)
        es_fit = es_model.fit()
        es_forecast = es_fit.forecast(51).rename(r'$\alpha=%s$' % es_fit.model.params['smoothing_level'])
    else:
        es_model = SimpleExpSmoothing(df['original'], initialization_method='heuristic')
        es_fit = es_model.fit(smoothing_level=es_alpha, optimized=False)
        es_forecast = es_fit.forecast(51).rename(r'$\alpha=%s$' % es_alpha)

    plt.plot(es_fit.fittedvalues, color=colors[i+1])
    (line, ) = plt.plot(es_forecast, color=colors[i+1])
    legend['lines'].append(line)
    legend['names'].append(es_forecast.name)

plt.legend(legend['lines'],legend['names'])

plt.savefig('es.png')

# Double exponential smoothing
des_params = [(0.6, 0.2), (0.6, 0.6), (0.8, 0.4)]

fig = plt.figure('Double exponential smoothing', figsize=(20,10))
plt.title('Double exponential smoothing', fontweight='bold')
(line, ) = plt.plot(df['original'], color=colors[0])
legend = {'lines': [line], 'names': ['original']}
for i, (des_alpha, des_beta) in enumerate(des_params):
    des_model = Holt(df['original'] + np.abs(data_min) + 1, exponential=True, initialization_method='estimated')
    des_fit = des_model.fit(smoothing_level=des_alpha, smoothing_trend=des_beta)
    des_forecast = des_fit.forecast(51).rename(r'$\alpha=%s \beta=%s$' % (des_alpha, des_beta))

    plt.plot(des_fit.fittedvalues - np.abs(data_min) - 1, color=colors[i+1])
    (line, ) = plt.plot(des_forecast - np.abs(data_min) - 1, color=colors[i+1])
    legend['lines'].append(line)
    legend['names'].append(des_forecast.name)

plt.legend(legend['lines'],legend['names'])

plt.savefig('des.png')

# Triple exponential smoothing
tes_params = [(0.6, 0.6, 0.2, 'mul', 'add', 2), (0.6, 0.6, 0.7, 'add', 'add', 2), (0.8, 0.4, 0.4, 'mul', 'mul', 4)]

fig = plt.figure('Triple exponential smoothing', figsize=(20,10))
plt.title('Triple exponential smoothing', fontweight='bold')
(line, ) = plt.plot(df['original'], color=colors[0])
legend = {'lines': [line], 'names': ['original']}
for i, (tes_alpha, tes_beta, tes_gamma, trend, seasonal, periods) in enumerate(tes_params):
    tes_model = ExponentialSmoothing(df['original'] + np.abs(data_min) + 1, trend=trend, seasonal=seasonal, seasonal_periods=periods, initialization_method='estimated')
    tes_fit = tes_model.fit(smoothing_level=tes_alpha, smoothing_trend=tes_beta, smoothing_seasonal=tes_gamma)
    tes_forecast = tes_fit.forecast(51).rename(r'$\alpha=%s \beta=%s \gamma=%s$ trend=%s seasonal=%s seasonal_periods=%s' % (tes_alpha, tes_beta, tes_gamma, trend, seasonal, periods))

    plt.plot(tes_fit.fittedvalues - np.abs(data_min) - 1, color=colors[i+1])
    (line, ) = plt.plot(tes_forecast - np.abs(data_min) - 1, color=colors[i+1])
    legend['lines'].append(line)
    legend['names'].append(tes_forecast.name)

plt.legend(legend['lines'],legend['names'])

plt.savefig('tes.png')

plt.show()