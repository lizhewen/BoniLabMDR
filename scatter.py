from plot_helper import xaxis_label_ticker
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def mutpair_scatter_plot(df, drugsets, efficacydf, strategy, 
                          year_label=5, plot_w=20, plot_h=15,
                          xlabel='Year', ylabel='Drug Efficacy & Genotype', 
                          title='Mutation Pair Arrival Time Scatter Plot'):

  xlocator = year_label*365  
  subplotnum = len(drugsets)
  ticks_x = xaxis_label_ticker()
  plt.rcParams['figure.figsize'] = [plot_w, plot_h*subplotnum]
  fig, axes = plt.subplots(nrows=subplotnum, ncols=1)
  fig.patch.set_facecolor('white')
  fig.suptitle('%s - %s Strategy' % (title, strategy), y=0.92, fontweight='bold')
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

  # Looping thru all therapy and draw subplot
  for (ax, drugset) in zip(axes.flatten(), drugsets):
    #annotate_place = df.iloc[:,:-4].max().max()
    efficacy_dict = efficacydf[drugset].to_dict()
    temp = df.copy()
    temp['color'] = 'blue'
    # filter out most dangerous triple
    mdt_filter = temp.to.str.contains('^(TYY..Y2.)|(KNFNFY2.)$', regex= True, na=False)
    temp.loc[mdt_filter, 'color'] = 'orange'

    temp['eff'] = temp['to'].replace(efficacy_dict).astype(str)
    temp['eff'] = temp['eff'].str[:5]
    temp['eff_to'] = temp['eff'] + ' ' + temp['to']
    temp = temp.sort_values(by=['eff_to'])    
    ax.scatter(temp['time'], temp['eff_to'], color=temp['color'])

    ax.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
    ax.xaxis.set_major_formatter(ticks_x)
    ax.set(title='(w.r.t. %s)' % drugset)

    # # Code for Annotation on plot
    # ax.text(4.5*365, annotate_place+0.03, 'Burn-in')
    # if strategy == 'Cycling':
    #   ax.text(11.5*365, annotate_place+0.03, 'DHA-PPQ')
    #   ax.text(16.5*365, annotate_place+0.03, 'AS-AQ')
    #   ax.text(22.5*365, annotate_place+0.03, 'AL')
    #   ax.text(26.5*365, annotate_place+0.03, 'DHA-PPQ')
    # ax.set_ylim(top=annotate_place+0.1)
    # # End Annotation
    ax.grid()

def mutpair_period_count(year_range_by_period, df, regex=''):
  ans = ''
  for interval in year_range_by_period:
    # dafult: no filter
    if regex == '':
      count = df.loc[(df['time']>interval[0]*365) & (df['time']<=interval[1]*365)].shape[0]
    else:
      count = df.loc[(df['time']>interval[0]*365) & (df['time']<=interval[1]*365) & (df.to.str.contains(regex, regex= True, na=False))].shape[0]
    ans += '%s,\n' % count
  return ans
  