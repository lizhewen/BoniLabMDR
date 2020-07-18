import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from plot_helper import xaxis_label_ticker, coloring_legend

def bsp_plot(df, year_label=5, xlabel='Years', ylabel='Percentage of Population', 
              plot_w=12, plot_h=6, 
              title='Blood Slide Prevalence Plot'):
  # Blood Slide Prevalence Trend Plot
  # This function takes in the parsed dataframe `df`, 
  #   and returns the plot of Blood Slide Prevalence (population count) against time (years).
  # Input:
  #   `df` - parsed dataframe to be plotted on
  #   `year_label` - how many years to be each labeled on x-axis

  xlocator = year_label*365
  plt.rcParams['figure.figsize'] = [plot_w, plot_h]
  fig, ax1 = plt.subplots()
  fig.patch.set_facecolor('white')
  ticks_x = xaxis_label_ticker()

  ax1.plot(df['current_time'], df['blood_slide_prev'])
  ax1.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax1.xaxis.set_major_formatter(ticks_x)
  ax1.set_xlabel(xlabel)
  ax1.set_ylabel(ylabel)
  ax1.set_title(title)

  plt.grid()

def mdtrg_plot(df, year_label=5, type1=['TYY--Y2.','TYYYYY2.'], type2='KNF--Y2.', 
              xlabel='Years', ylabel='Genotype Frequency', plot_w=12, plot_h=10, 
              suptitle='Evolution Trends of Most-Dangerous Triple-Resistant Genotypes'):
  # Most Dangerous Triple-Resistant Genotype Evolution Trend Plot
  # This program takes in parsed dataframe object and plots 
  # evolution trends for the most-dangerous triple-resistant genotypes.

  xlocator = year_label*365  
  plt.rcParams['figure.figsize'] = [plot_w, plot_h]
  fig = plt.figure()
  fig.patch.set_facecolor('white')
  fig.suptitle(suptitle, y=0.92, fontweight='bold')
  ticks_x = xaxis_label_ticker()

  ax1 = plt.subplot(2, 1, 1)
  for subtype1 in type1:
    ax1.plot(df['current_time'], df.filter(regex=subtype1, axis=1).sum(axis=1), label=subtype1)
  ax1.set_xlabel(xlabel)
  ax1.set_ylabel(ylabel)
  ax1.set_title('AQ + DHA-PPQ')
  ax1.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax1.xaxis.set_major_formatter(ticks_x)
  ax1.grid()
  ax1.legend()

  ax2 = plt.subplot(2, 1, 2)
  ax2.plot(df['current_time'], df.filter(regex=type2, axis=1).sum(axis=1))
  ax2.set_xlabel(xlabel)
  ax2.set_ylabel(ylabel)
  ax2.set_title('LM + DHA-PPQ, i.e. %s' % type2)
  ax2.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax2.xaxis.set_major_formatter(ticks_x)
  ax2.grid()

def mdr_get_plot(df_list, totaldrugname, strategy, option, 
                 year_label=5, xlabel='Years', 
                 ylabel='Genotype Frequency', 
                 title='Evolution of Single- and Multi-Drug-Resistant Types', 
                 plot_w=13, plot_h=4):
  # MDR Genotype Evolution Trend Plot

  xlocator = year_label*365  
  subplotnum = len(df_list)
  ticks_x = xaxis_label_ticker()
  plt.rcParams['figure.figsize'] = [plot_w, plot_h*subplotnum]
  fig, axes = plt.subplots(nrows=subplotnum, ncols=1)
  fig.patch.set_facecolor('white')
  fig.suptitle('%s - %s Strategy' % (title, strategy), y=0.92, fontweight='bold')
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

  # Looping thru all therapy and draw subplot
  for (ax, df, drugname) in zip(axes.flatten(), df_list, totaldrugname):
    annotate_place = df.iloc[:,:-4].max().max()
    col_names = list(df.columns)
    mdr_cases = col_names[:-4] # Last four columns are not about MDR
    mdr_cases.reverse() # reverse to plot most-dangerous type latest
    # Loop thru each MDR case
    for mdr_case in mdr_cases:
      ax.plot(df['current_time'], df[mdr_case], label=mdr_case, color=coloring_legend(mdr_case,option))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
    ax.xaxis.set_major_formatter(ticks_x)
    ax.set(title='(w.r.t. %s)' % drugname)

    # Code for Annotation on plot
    ax.text(4.5*365, annotate_place+0.03, 'Burn-in')
    if strategy == 'Cycling':
      ax.text(11.5*365, annotate_place+0.03, 'DHA-PPQ')
      ax.text(16.5*365, annotate_place+0.03, 'AS-AQ')
      ax.text(22.5*365, annotate_place+0.03, 'AL')
      ax.text(26.5*365, annotate_place+0.03, 'DHA-PPQ')
    ax.set_ylim(top=annotate_place+0.1)
    # End Annotation

    ax.legend(loc='upper center', bbox_to_anchor=(1.1, 0.8), shadow=True, ncol=1)
    ax.grid()

def risk_auc_plot(df, startyear, endyear, burnin_year=10, 
                  title='Genotype Risk from Area Under Curve', 
                  genopattern='TYY..Y2.', xlabel='Year', 
                  ylabel='Number of Individuals Infected', 
                  plot_w=12, plot_h=6, year_label=5):
  # Plot Area-Under-Curve to show Genotype Risk
  # Note: `startyear` and `endyear` number should exclude burn-in phase

  ylabel='Number of Individuals Infected by %s' % genopattern
  fig, ax = plt.subplots()
  fig.patch.set_facecolor('white')
  plt.rcParams['figure.figsize'] = [plot_w, plot_h]
  ticks_x = xaxis_label_ticker()
  xlocator = year_label*365

  # estimate bsp (people infected) by specific genotype(s)
  df['bsp_portion'] = df['blood_slide_prev'] * df.filter(regex=genopattern, axis=1).sum(axis=1)
  df['people'] = df['population'] * df['bsp_portion'] / 100
  # df time counts burn-in phase
  startyear += burnin_year
  endyear += burnin_year

  # Calculate area under curve
  yaxis = df.loc[(startyear*365<df['current_time']) & (df['current_time']<=endyear*365)]['people'].values
  xaxis = df.loc[(startyear*365<df['current_time']) & (df['current_time']<endyear*365)]['current_time'].values
  area = np.trapz(yaxis, x=xaxis)
  textyear = (startyear + endyear) / 2

  ax.plot(df['current_time'], df['people'])
  # Shade the area-under-curve
  ax.fill_between(df['current_time'], df['people'], 
                  where=((startyear*365<df['current_time']) & (df['current_time']<=endyear*365)), 
                  alpha=0.25)
  
  ax.text(textyear*365, 0.1, 'Area = %s' % area)

  ax.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax.xaxis.set_major_formatter(ticks_x)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  ax.grid()

  plt.show()
