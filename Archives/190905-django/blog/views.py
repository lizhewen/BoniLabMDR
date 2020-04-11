from django.shortcuts import render
from .plot_basics import *

from blog.forms import AucForm

filepath = 'blog/files/monthly_data_0.txt'

def home(request):
    return render(request, 'blog/home.html')

def plot_bsp(request):
	from .plot_helper import _bsp_plot
	df = pd.read_csv(filepath, sep='\t')
	html_fig = _bsp_plot(df)
	return render(request, "blog/bsp-plot.html", {'div_figure' : html_fig})

def plot_geno(request):
	from .plot_helper import _geno_plot
	df = pd.read_csv(filepath, sep='\t')
	html_fig = _geno_plot(df)
	return render(request, "blog/geno-plot.html", {'div_figure' : html_fig})

# def plot_auc(request):
# 	from .plot_helper import _auc_plot, _area_calc
# 	form = AucForm()
# 	df = pd.read_csv(filepath, sep='\t')
# 	html_fig = _auc_plot(df)
# 	area = _area_calc(df, 30)
# 	return render(request, "blog/auc-plot.html", {'form': form, 'text': 30, 'div_figure' : html_fig, 'area' : area})

def plot_auc(request, yearChosen='30'):
	from .plot_helper import _auc_plot, _area_calc
	form = AucForm()
	# form = AucForm(request.POST.copy())
	# if form.is_valid():
	# 	yearChosen = form.get('Year') # prevent SQL injection
		#print("get year chose")
	#print("continue")
	df = pd.read_csv(filepath, sep='\t')
	#html_fig = _auc_plot(df, choice=choiceText, years=yearText)
	html_fig = _auc_plot(df, years=int(yearChosen))
	area = _area_calc(df, int(yearChosen))
	args = {'form': form, 'text': yearChosen, 'div_figure' : html_fig, 'area' : area}
	return render(request, "blog/auc-plot.html", args)

# Note -- Saved for testing GET & POST
# def replot_auc(request, yearChosen='30'):
# 	from .plot_helper import _auc_plot, _area_calc
# 	yearChosen = request.POST['Year']
# 	df = pd.read_csv(filepath, sep='\t')
# 	#html_fig = _auc_plot(df, choice=choiceText, years=yearText)
# 	html_fig2 = _auc_plot(df, years=int(yearChosen))
# 	area = _area_calc(df, int(yearChosen))
# 	args = {'form': form, 'text': yearChosen, 'div_figure' : html_fig2, 'area' : area}
# 	return render(request, "blog/auc-plot.html", args)

def multi_plot_bsp(request):
	from .plot_helper import _multi_bsp_plot
	df1 = pd.read_csv('Cyc2.txt', sep='\t')
	df2 = pd.read_csv('adapCyc.txt', sep='\t')
	html_fig = _multi_bsp_plot(df1,df2)
	return render(request, "blog/bsp-plot.html", {'div_figure' : html_fig})

def multi_plot_geno(request):
	from .plot_helper import _multi_geno_plot
	df1 = pd.read_csv('Cyc2.txt', sep='\t')
	df2 = pd.read_csv('adapCyc.txt', sep='\t')
	html_fig = _multi_geno_plot(df1,df2)
	return render(request, "blog/bsp-plot.html", {'div_figure' : html_fig})

def multi_plot_cyc(request):
	from .plot_helper import _multi_cyc_plot

	df1 = pd.read_csv('2yr.txt', sep='\t') # 2-yr
	df2 = pd.read_csv('3yr.txt', sep='\t') # 3-yr
	df3 = pd.read_csv('5yr.txt', sep='\t') # 5-yr
	df4 = pd.read_csv('7yr.txt', sep='\t') # 7-yr

	html_fig = _multi_cyc_plot(df1,df2,df3,df4)
	return render(request, "blog/bsp-plot.html", {'div_figure' : html_fig})