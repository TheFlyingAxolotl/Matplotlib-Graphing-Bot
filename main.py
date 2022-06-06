import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

directory = {
  'pie'    :   'piechart'            ,
  'bar'    :   'simple bar graph'    ,
  'group'  :   'grouped-bar graph'   ,
  'scatter':   'scatterplot'         ,
  'line'   :   'linegraph'           ,
  'histo'  :   'histogram'           ,
  'stack'  :   'stacked histogram'
}

#hit 'run' when you are ready to graph
plt.figure(dpi=1200)
with open('data.txt') as r_data:
  r_data = r_data.readlines()
  p_data = [x.strip() for x in r_data]

sns.set(font_scale=0.8)
graph_type = p_data[0][12:]
data_type = p_data[1][11:]
num_x = int(p_data[3][6:])
x_data = [(p_data[x]) for x in range(4, 4+num_x)]  
num_y = int(p_data[4+num_x][6:])
y_data = [float(p_data[x]) for x in range(5+num_x, 5+num_x+num_y)]
num_color = int(p_data[6+num_x+num_y][18:])
colors = [p_data[x] for x in range(7+num_x+num_y, 7+num_x+num_y+num_color)]
x_label = p_data[8+num_x+num_y+num_color][9:]
y_label = p_data[9+num_x+num_y+num_color][9:]
title = p_data[10+num_x+num_y+num_color][7:]

with open('settings.txt') as settings:
  settings = settings.readlines()
  settings = [x.strip() for x in settings]

if (graph_type == 'pie'):
  shadow = settings[1][7:]
  gap = settings[2][4:]
  print('X_data: Variable names\nY_data: Values\n')
elif (graph_type == 'bar'):
  position = settings[5][10:]
  average_line = settings[6][9:]
  annotations = settings[7][13:]
  print('X_data: Variable names\nY_data: Values\n')
elif (graph_type == 'group'):
  width = float(settings[10][6:])
  edgecolor = settings[11][11:]
  alpha = float(settings[12][6:])
  num_var = int(input('Enter the number of variables: '))
  num_group = int(input('Enter the number of groups: '))
  values = []
  num_extra = int(p_data[13+num_x+num_y+num_color][11:])
  extra_data = [p_data[x] for x in range(14+num_x+num_y+num_color, 14+num_x+num_y+num_color+num_extra)]
  print('X_data: Variable names\nY_data: Values (in order of variables)\nExtra_data: Group names\n')
elif (graph_type == 'histo'):
  edgecolor = settings[15][11:]
  average_line = settings[17][9:]
  alpha = float(settings[16][6:])
  histtype = settings[18][10:]
  bins = int(input('Enter the number of bins: '))
  num_var = int(input('Enter the number of variables: '))
  data = []
  print('X_data: Variable names\nY_data: Values (in order of variables)\n')
elif(graph_type == 'line'):
  num_var = int(input('Enter the number of variables: '))
  point, data = [], []
  num_labels = int(p_data[13+num_x+num_y+num_color][12:])
  labels = [p_data[x] for x in range(14+num_x+num_y+num_color, 14+num_x+num_y+num_color+num_labels)]
  average_line = settings[21][9:]
  print('X_data: Data-Points (in order of variables)\nY_data: Values (in order of variables)\nExtra_data: Variable names\n')
elif(graph_type == 'scatter'):
  num_var = int(input('Enter the number of variables: '))
  point, data = [], []
  num_labels = int(p_data[13+num_x+num_y+num_color][12:])
  labels = [p_data[x] for x in range(14+num_x+num_y+num_color, 14+num_x+num_y+num_color+num_labels)]
  size = int(settings[24][5:])
  markertype = settings[25][8:] 
  edgecolor = settings[26][11:]
  bestfit = settings[27][13:]
  print('X_data: Data-Points (in order of variables)\nY_data: Values (in order of variables)\nExtra_data: Variable names\n')
  def best_fit(point, data):
    xbar = sum(point)/len(point)
    ybar = sum(data)/len(data)
    n = len(data)
    numer = sum([xi*yi for xi,yi in zip(point, data)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in point]) - n * xbar**2
    b = float(numer / denum)
    a = float(ybar - b * xbar)
    return a, b
grid = settings[29][6:]
print('All data entered should be on different lines')
enter = input('Hit enter when you are ready: ')

if graph_type == 'pie':
  fig = plt.figure(figsize=(5, 4))
  plt.pie(y_data, labels=x_data, colors=colors,
  autopct='%1.1f%%', shadow=shadow, startangle=90)
  plt.axis('equal')

elif graph_type =='bar':
  fig = plt.figure(figsize=(7,7))
  pos = np.arange(len(x_data))
  bars = y_data
  average = sum(bars)/len(x_data)
  if position == 'horizontal':
    plt.xlabel(x_label)
    plt.barh(pos, bars, align='center', alpha=0.70, color=colors)
    plt.yticks(pos, x_data)
    if (average_line == 'on'):
      plt.axvline(average, label='average', linestyle='--', color='darkblue')
  elif position == 'vertical':
    plt.ylabel(y_label)
    plt.bar(pos, bars, align='center', alpha=0.70, color=colors, )
    plt.xticks(pos, x_data, rotation = 0)
    if (average_line == 'on'):
      plt.axhline(average, label='average', linestyle='--', color='darkblue')
  if (annotations == 'on'):
    for a, b, c in zip(pos, bars): 
      if (b < 10):
        plt.text(float(a)-0.06, float(b)+c+0.25, str(b))
      else:
        plt.text(float(a)-0.105, float(b)+c+0.25, str(b))
    
elif graph_type == 'group':
  fig = plt.figure(figsize=(6, 4))
  for i in range(num_var):
    for x in range(num_group):
      if (i==0):
        values.append((y_data[x]))
      else: 
        values.append((y_data[x+num_group*i]))
    label, color = x_data[i], colors[i]
    positions = np.arange(len(values))
    positional = [x + width*i for x in positions]
    plt.bar(positional, values, color=color, width=width, edgecolor=edgecolor, label=label, alpha=alpha)
    length = len(values)
    values.clear()

  plt.ylabel(y_label)
  plt.title(title)
  plt.xticks([r + width for r in range(length)], extra_data)

elif (graph_type == 'histo'):
  fig = plt.figure(1, figsize=(7,4))
  for x in range(num_var):
    for i in range(len(y_data)//num_var*x, len(y_data)//num_var*(x+1)):
      data.append(y_data[i])
    color = colors[x]



    #gotta fix this one day
    label = ['english', 'classical', 'no']
    
    plt.hist(data, bins, histtype=histtype, alpha=alpha, align='mid', color=color,label=label[x], edgecolor=edgecolor)
    if (average_line == 'on'):
      mean_data = sum(data)/len(data)
      plt.axvline(mean_data, color=color, linestyle='--', linewidth=1)
    data.clear()

  plt.ylim(0,7)
  plt.ylabel(y_label)

elif (graph_type == 'line'):
  fig = plt.figure(figsize=(8.5, 6))
  for i in range(num_var):
    for x in range(len(x_data)//num_var*i, len(x_data)//num_var*(i+1)):
      if (x_data[x].isnumeric()):
        point.append(int(x_data[x]))
        data.append(y_data[x])
    average = sum(data)/len(point)
    color = colors[i]
    label = labels[i]
    plt.plot(point, data, label=label, color=color, linewidth=3, alpha = 0.5)
    if (average_line == 'on'):
      plt.axhline(average, linestyle='--', color=color)
    point.pop(0)
    data.pop(0)
    point.clear()
    data.clear()
    
  plt.ylabel(y_label)
  plt.xlabel(x_label)

elif graph_type == 'scatter':
  fig = plt.figure(figsize=(6, 4))
  for i in range(num_var):
    for x in range(len(x_data)//num_var*i, len(x_data)//num_var*(i+1)):
      point.append(int(x_data[x])) 
      data.append(y_data[x])     
    color = colors[i]
    label = labels[i]
    plt.scatter(point, data, s=size, color=color, edgecolors=edgecolor, label=label, marker=markertype)
    a, b = best_fit(point, data)
    yfit = [a + b * xi for xi in point]
    #plt.plot(point, yfit, color='darkgray')
    point.clear()
    data.clear()
  
  plt.xlabel(x_label)
  plt.ylabel(y_label)

if (grid == 'on'):
  plt.grid(color='black', linestyle='-', linewidth=0.2)
plt.legend()
plt.title(title, fontweight = "bold")


plt.show()
fig.savefig('result.png')
plt.tight_layout()