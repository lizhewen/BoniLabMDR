# blood slide prevalence plot
from .plot_basics import *  # import packages

# Saved for MSC TV
#fig_size = (6,3)
fig_size = (15,8)

def _bsp_plot(df, locator=60):
  fig, ax = plt.subplots(figsize=fig_size)
  ax.grid(True, alpha=0.3)

  df['bsp_in_popu'] = df['blood_slide_prev'] * 50000 / 100
  df['time_in_yrs'] = df['current_time'] / (12*31)
  ax.plot(df['time_in_yrs'], df['bsp_in_popu'])
  
  # ticker for mpld3
  #ticklocs = range(0, 20*locator+1, locator)
  #axislim = -5,605
  #plt.xticks(ticklocs)
  #plt.xlim(*axislim)

  ax.set_xlabel('years')
  ax.set_ylabel('blood slide prevalence (persons)')
  return mpld3.fig_to_html(fig)

def _multi_bsp_plot(df1, df2, locator=60):
  #fig, ax = plt.subplots(figsize=fig_size)
  fig = plt.figure(figsize=fig_size)
  
  # Plot for Cyc
  ax1 = fig.add_subplot(211)
  ax1.grid(True, alpha=0.3)
  df1['bsp_in_popu'] = df1['blood_slide_prev'] * 50000 / 100
  df1['time_in_yrs'] = df1['current_time'] / (12*31)
  ax1.plot(df1['time_in_yrs'], df1['bsp_in_popu'])
  ax1.set_ylabel('blood slide prevalence (persons)')
  ax1.set_title('Simple Cycling Strategy')

  # Plot for Adptive Cyc
  ax2 = fig.add_subplot(212)
  ax2.grid(True, alpha=0.3)
  df2['bsp_in_popu'] = df2['blood_slide_prev'] * 50000 / 100
  df2['time_in_yrs'] = df2['current_time'] / (12*31)
  ax2.plot(df2['time_in_yrs'], df2['bsp_in_popu'])
  ax2.set_xlabel('years')
  ax2.set_ylabel('blood slide prevalence (persons)')
  ax2.set_title('Adaptive Cycling Strategy')

  return mpld3.fig_to_html(fig)

def _geno_plot(df):
  fig, ax = plt.subplots(figsize=fig_size)
  #fig, ax = plt.subplots()
  ax.grid(True, alpha=0.3)

  df['time_in_yrs'] = df['current_time'] / (12*31)
  ax.plot(df['time_in_yrs'], df.iloc[:,0:151].filter(regex='.....C1.', axis=1).sum(axis=1), label='*C1.(wild)')
  ax.plot(df['time_in_yrs'], df.iloc[:,0:151].filter(regex='.....C2.', axis=1).sum(axis=1), label='*C2.(PPQ)')
  ax.plot(df['time_in_yrs'], df.iloc[:,0:151].filter(regex='.....Y1.', axis=1).sum(axis=1), label='*Y1.(Artim.)')
  ax.plot(df['time_in_yrs'], df.iloc[:,0:151].filter(regex='.....Y2.', axis=1).sum(axis=1), label='*Y2.(double)')
  ax.plot(df['time_in_yrs'], df.iloc[:,0:151].filter(regex='TY......', axis=1).sum(axis=1), label='TY*(AQ)')
  ax.plot(df['time_in_yrs'], df.iloc[:,0:151].filter(regex='KN......', axis=1).sum(axis=1), label='KN*(Lum)')
  ax.set_xlabel('years')
  ax.set_ylabel('genotype freq')
  line_collections, labels = ax.get_legend_handles_labels() # return lines and labels
  interactive_legend = plugins.InteractiveLegendPlugin(line_collections, labels, alpha_unsel=0, alpha_over=1.5, start_visible=True)
  plugins.connect(fig, interactive_legend)
  return mpld3.fig_to_html(fig)

def _multi_geno_plot(df1, df2):
  fig, ax = plt.subplots(figsize=fig_size)
  #fig, ax = plt.subplots()
  ax.grid(True, alpha=0.3)

  # Plot for Cyc
  ax1 = fig.add_subplot(211)
  df1['time_in_yrs'] = df1['current_time'] / (12*31)
  ax1.plot(df1['time_in_yrs'], df1.iloc[:,0:151].filter(regex='.....C1.', axis=1).sum(axis=1), label='*C1.(wild)')
  ax1.plot(df1['time_in_yrs'], df1.iloc[:,0:151].filter(regex='.....C2.', axis=1).sum(axis=1), label='*C2.(PPQ)')
  ax1.plot(df1['time_in_yrs'], df1.iloc[:,0:151].filter(regex='.....Y1.', axis=1).sum(axis=1), label='*Y1.(Artim.)')
  ax1.plot(df1['time_in_yrs'], df1.iloc[:,0:151].filter(regex='.....Y2.', axis=1).sum(axis=1), label='*Y2.(double)')
  ax1.plot(df1['time_in_yrs'], df1.iloc[:,0:151].filter(regex='TY......', axis=1).sum(axis=1), label='TY*(AQ)')
  ax1.plot(df1['time_in_yrs'], df1.iloc[:,0:151].filter(regex='KN......', axis=1).sum(axis=1), label='KN*(Lum)')
  #ax1.set_xlabel('years')
  ax1.set_ylabel('genotype freq')
  ax1.set_title('Simple Cycling Strategy')

  # Plot for Adaptive Cycling
  ax2 = fig.add_subplot(212)
  df2['time_in_yrs'] = df2['current_time'] / (12*31)
  ax2.plot(df2['time_in_yrs'], df2.iloc[:,0:151].filter(regex='.....C1.', axis=1).sum(axis=1), label='*C1.(wild)')
  ax2.plot(df2['time_in_yrs'], df2.iloc[:,0:151].filter(regex='.....C2.', axis=1).sum(axis=1), label='*C2.(PPQ)')
  ax2.plot(df2['time_in_yrs'], df2.iloc[:,0:151].filter(regex='.....Y1.', axis=1).sum(axis=1), label='*Y1.(Artim.)')
  ax2.plot(df2['time_in_yrs'], df2.iloc[:,0:151].filter(regex='.....Y2.', axis=1).sum(axis=1), label='*Y2.(double)')
  ax2.plot(df2['time_in_yrs'], df2.iloc[:,0:151].filter(regex='TY......', axis=1).sum(axis=1), label='TY*(AQ)')
  ax2.plot(df2['time_in_yrs'], df2.iloc[:,0:151].filter(regex='KN......', axis=1).sum(axis=1), label='KN*(Lum)')
  ax2.set_xlabel('years')
  ax2.set_ylabel('genotype freq')
  ax2.set_title('Adaptive Cycling Strategy')

  line_collections, labels = ax1.get_legend_handles_labels() # return lines and labels
  interactive_legend = plugins.InteractiveLegendPlugin(line_collections, labels, alpha_unsel=0, alpha_over=1.5, start_visible=True)
  plugins.connect(fig, interactive_legend)
  return mpld3.fig_to_html(fig)

def _auc_plot(df, choice='.....Y2.', years=30):

  import base64
  from io import BytesIO

  # scale func to show x-axis in years
  scale_x = 365
  ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))

  fig, ax = plt.subplots(figsize=(13,5))
  ax.grid(True, alpha=0.3)

  df['new_bsp'] = df['blood_slide_prev'] * df.iloc[:,0:151].filter(regex='.....Y2.', axis=1).sum(axis=1) * 50000 / 100
  ax.plot(df['current_time'], df['new_bsp'])
  ax.fill_between(df['current_time'], df['new_bsp'], where=(df['current_time']<=years*365), alpha=0.25)
  ax.xaxis.set_major_locator(ticker.MultipleLocator(1825)) # 5-year mark
  ax.xaxis.set_major_formatter(ticks_x)
  ax.set_xlabel('years')
  ax.set_ylabel('blood slide prev from selected genotypes (persons)')

  # Save it to a temporary buffer.  
  buf = BytesIO()
  fig.savefig(buf, format="png")
  # Embed the result in the html output.
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  return f"<img src='data:image/png;base64,{data}'/>"

def _area_calc(df, yr):
  return np.trapz(df.iloc[:yr*12,-1])

def _multi_cyc_plot(df1, df2, df3, df4):
  import base64
  from io import BytesIO

  # scale func to show x-axis in years
  scale_x = 12
  ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))

  fig = plt.figure(figsize=fig_size)
  ax1 = fig.add_subplot(221)
  # sum up total num of parasites in the silumation
  tot_para1 = df1.iloc[:,22:150].sum(axis=1)
  # grouped comparisons for DHA-PPQ resistance
  ax1.plot(df1.iloc[:,0:151].filter(regex='.....C1.', axis=1).sum(axis=1)/tot_para1, 'c', label='*C1.(wild)')
  ax1.plot(df1.iloc[:,0:151].filter(regex='.....C2.', axis=1).sum(axis=1)/tot_para1, 'm', label='*C2.(PPQ)')
  ax1.plot(df1.iloc[:,0:151].filter(regex='.....Y1.', axis=1).sum(axis=1)/tot_para1, 'y', label='*Y1.(Artim.)')
  ax1.plot(df1.iloc[:,0:151].filter(regex='.....Y2.', axis=1).sum(axis=1)/tot_para1, 'r', label='*Y2.(double)')
  ax1.plot(df1.iloc[:,0:151].filter(regex='TY......', axis=1).sum(axis=1)/tot_para1, 'b', label='TY*(AQ)')
  ax1.plot(df1.iloc[:,0:151].filter(regex='KN......', axis=1).sum(axis=1)/tot_para1, 'g', label='KN*(Lum)')
  # format x-axis
  ax1.xaxis.set_major_locator(ticker.MultipleLocator(12*2))
  ax1.xaxis.set_major_formatter(ticks_x)
  ax1.set_xlabel('years')
  ax1.set_ylabel('parasite freq')
  ax1.set_title('2-yr')

  ax2 = fig.add_subplot(222)
  tot_para2 = df2.iloc[:,22:150].sum(axis=1)
  # grouped comparisons for DHA-PPQ resistance
  ax2.plot(df2.iloc[:,0:151].filter(regex='.....C1.', axis=1).sum(axis=1)/tot_para2, 'c')
  ax2.plot(df2.iloc[:,0:151].filter(regex='.....C2.', axis=1).sum(axis=1)/tot_para2, 'm')
  ax2.plot(df2.iloc[:,0:151].filter(regex='.....Y1.', axis=1).sum(axis=1)/tot_para2, 'y')
  ax2.plot(df2.iloc[:,0:151].filter(regex='.....Y2.', axis=1).sum(axis=1)/tot_para2, 'r')
  ax2.plot(df2.iloc[:,0:151].filter(regex='TY......', axis=1).sum(axis=1)/tot_para2, 'b')
  ax2.plot(df2.iloc[:,0:151].filter(regex='KN......', axis=1).sum(axis=1)/tot_para2, 'g')
  # format x-axis
  majors2 = [10,13,16,19,22,25,28,31,34,37,40,43,46,49]
  ax2.xaxis.set_major_locator(ticker.FixedLocator([i*12 for i in majors2])) # 3-yr rotation
  ax2.xaxis.set_major_formatter(ticks_x)
  ax2.set_xlabel('years')
  ax2.set_ylabel('parasite freq')
  ax2.set_title('3-yr')

  ax3 = fig.add_subplot(223)
  tot_para3 = df3.iloc[:,22:150].sum(axis=1)
  # grouped comparisons for DHA-PPQ resistance
  ax3.plot(df3.iloc[:,0:151].filter(regex='.....C1.', axis=1).sum(axis=1)/tot_para3, 'c')
  ax3.plot(df3.iloc[:,0:151].filter(regex='.....C2.', axis=1).sum(axis=1)/tot_para3, 'm')
  ax3.plot(df3.iloc[:,0:151].filter(regex='.....Y1.', axis=1).sum(axis=1)/tot_para3, 'y')
  ax3.plot(df3.iloc[:,0:151].filter(regex='.....Y2.', axis=1).sum(axis=1)/tot_para3, 'r')
  ax3.plot(df3.iloc[:,0:151].filter(regex='TY......', axis=1).sum(axis=1)/tot_para3, 'b')
  ax3.plot(df3.iloc[:,0:151].filter(regex='KN......', axis=1).sum(axis=1)/tot_para3, 'g')
  # format x-axis
  ax3.xaxis.set_major_locator(ticker.MultipleLocator(12*5))
  ax3.xaxis.set_major_formatter(ticks_x)
  ax3.set_xlabel('years')
  ax3.set_ylabel('parasite freq')
  ax3.set_title('5-yr')

  ax4 = fig.add_subplot(224)
  tot_para4 = df4.iloc[:,22:150].sum(axis=1)
  # grouped comparisons for DHA-PPQ resistance
  ax4.plot(df4.iloc[:,0:151].filter(regex='.....C1.', axis=1).sum(axis=1)/tot_para4, 'c')
  ax4.plot(df4.iloc[:,0:151].filter(regex='.....C2.', axis=1).sum(axis=1)/tot_para4, 'm')
  ax4.plot(df4.iloc[:,0:151].filter(regex='.....Y1.', axis=1).sum(axis=1)/tot_para4, 'y')
  ax4.plot(df4.iloc[:,0:151].filter(regex='.....Y2.', axis=1).sum(axis=1)/tot_para4, 'r')
  ax4.plot(df4.iloc[:,0:151].filter(regex='TY......', axis=1).sum(axis=1)/tot_para4, 'b')
  ax4.plot(df4.iloc[:,0:151].filter(regex='KN......', axis=1).sum(axis=1)/tot_para4, 'g')
  # format x-axis
  majors = [10,17,24,31,38,45]
  ax4.xaxis.set_major_locator(ticker.FixedLocator([i*12 for i in majors])) # 7-yr rotation
  ax4.xaxis.set_major_formatter(ticks_x)
  ax4.set_xlabel('years')
  ax4.set_ylabel('parasite freq')
  ax4.set_title('7-yr')

  fig.legend()

  # Save it to a temporary buffer.  
  buf = BytesIO()
  fig.savefig(buf, format="png")
  # Embed the result in the html output.
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  return f"<img src='data:image/png;base64,{data}'/>"