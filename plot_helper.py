import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from constant import HEADLINE, ENCODINGDB

def xaxis_label_ticker(scale_x=365, burnin_year=10):
  # Ticker function that labels x-axis in years
  #   and reflect burn-in phase of the simulation
  # Input:
  #   `scale_x` - how many days in a year, default=365
  #   `burnin_year` - how long is the burn-in phase in years, default=10
  # Return:
  #   A ticker function that labels the first day after burn-in as 0 on x-axis

  return (ticker.FuncFormatter(lambda x, pos: '{0:g}'.format((x-burnin_year*365)/scale_x)))

def parse(file_name, interested_col = [0,2,8,12] + list(range(22,150))):
  # `parse` - Parser Function
  # 
  # Input:
  #   `file_name` - path to the txt file to be parsed
  #   `interested_col`, with default - a list of number indicating which columns to tailor for returned dataframe
  # Output:
  #   `df` - validated and tailored dataframe object (pandas required)
  # 
  # This is the parser function that helps adding headings to the txt file,
  #   and then convert the columns in interest to dataframe.
  # The function also checks if the simulation was generated for single location ONLY.
  # Currently all further analysis does not support multiple location scenarios.
  # 
  # Default columns that are selected are:
  #  #0 - Current Time
  #  #2 - Year
  #  #8 - Population
  #  #12 - Blood Slide Prevalence
  #  #22-149 - Parasite Count by Genotypes

  # define name of temporary dummy file
  dummy_file = file_name[:-4] + '_parsed.txt'
  # open original file in read mode and dummy file in write mode
  with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
    # Write given line to the dummy file
    write_obj.write(HEADLINE + '\n')
    # Read lines from original file one by one and append them to the dummy file
    for line in read_obj:
      write_obj.write(line)

  df = pd.read_csv(dummy_file, sep='\t')

  # Check if file is single-location'd
  if len(df.columns) == 282:
    # Return tailored df
    df = df.iloc[:,interested_col]
    return df
  
  # Error if file not single-location'd
  return None

def mutpair_parse(file_name):
  dummy_file = file_name[:-4] + '_parsed.txt'
  # open original file in read mode and dummy file in write mode
  with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
    # Write given line to the dummy file
    write_obj.write('time,from,to' + '\n')
    # Read lines from original file one by one and append them to the dummy file
    for line in read_obj:
      write_obj.write(line)

  df = pd.read_csv(dummy_file, sep=',')
  return df

def resistant_strength_calc(pattern, drugname, option=1):
  # Drug Resistant Strength Calculation Function
  # 
  # Input:
  #   `pattern` takes in malaria geno-type encoding. e.g. 'KNF--C1x'; 
  #   `drugset` takes in a list of drug abbreviations (e.g. 'A', 'PPQ', etc.)
  #   that are interested for the scenario; `option` takes in a number `1` or `2`.
  # Output: 
  #   This function evaluates the Malaria encoding pattern and counts how many drugs (in the set) 
  #   is this genotype resistant to. The function also counts the number of genetic (mutation) events 
  #   happened regarding this genotype.
  # Option:
  #   For option 1, the function returns `drugnum` indicating how many drugs in the set is this pattern 
  #     resistant to, and `eventcount` indicating how many mutation events happened to this genotype; 
  #   For option 2, `drugnum` is the same while `allelecount` breaks down the mutation events to each allel, 
  #     e.g. '11000000' indicates mutations at *K76T* and *N86Y* when using Amodiaquine (AQ).

  if drugname == 'AL':
    drugset = ['A','LM']
  elif drugname == 'AS-AQ':
    drugset = ['A','AQ']
  elif drugname == 'DHA-PPQ':
    drugset = ['A','PPQ']
  elif drugname == 'AS-MQ':
    drugset = ['A','MQ']
  else:
    print("Drug name not found.")
    return None

  drugnum = 0
  allelecount = '00000000'
    
  if 'A' in drugset and pattern[5:6] == 'Y': # Artemisinin Resistant
    drugnum += 1
    allelecount = allelecount[0:5] + '1' + allelecount[6:]
        
  if 'PPQ' in drugset and pattern[6:7] == '2': # PPQ Resistant
    drugnum += 1
    allelecount = allelecount[0:6] + '1' + allelecount[7:]
        
  if 'LM' in drugset and pattern[0:3] != 'TYY': # LM Resistant
    drugnum += 1
    if pattern[0:1] == 'K': # K76T
      allelecount = '1' + allelecount[1:]
    if pattern[1:2] == 'N': # N86Y
      allelecount = allelecount[0:1] + '1' + allelecount[2:]
    if pattern[2:3] == 'F': # Y184F
      allelecount = allelecount[0:2] + '1' + allelecount[3:]
            
  if 'AQ' in drugset and pattern[0:3] != 'KNF': # AQ Resistant
    drugnum += 1
    if pattern[0:1] == 'T': # K76T
      allelecount = '1' + allelecount[1:]
    if pattern[1:2] == 'Y': # N86Y
      allelecount = allelecount[0:1] + '1' + allelecount[2:]
    if pattern[2:3] == 'Y': # Y184F
      allelecount = allelecount[0:2] + '1' + allelecount[3:]
            
  if 'MQ' in drugset: # MQ
    if not (pattern[1:2] == 'Y' and pattern[4:5] == '--'): # If Resistance exists
      drugnum += 1
      if pattern[1:2] == 'N': # N86Y
        allelecount = allelecount[0:1] + '1' + allelecount[2:]
      if pattern[3:5] != '--': # Double Copy N86Y & Y184F
        allelecount = allelecount[0:3] + '1-' + allelecount[5:]
            
  if option == 1:
    eventcount = allelecount.count('1')
    return ("%s-%s" % (drugnum, eventcount))
  return ("%s-%s" % (drugnum, allelecount))

def df_col_replace(original_df, drugset, option):
  # Dataframe Column Name Replace Function
  # 
  # Input: 
  #   `df` - dataframe object to be replaced;
  #   `drugset` - a set of drugs deployed for the simulation and thus we are interested in analyzing.
  # Output:
  #   `df` - parsed dataframe object where genotype encodings have been replaced by their correponding 
  #     drug-resistance-strength, in column names.
  #     The parsed dataframe also groups the columns with the same drug-resistance-strength.
  # Option:
  #   `1` replace column names with drug-mutation indication set 
  #     (e.g. 2-3 meaning 2-drug resistant, with 3-mutation event occured);
  #   `2` replace column name with its corresponding drug efficacy wrt. the current drugset.

  df = original_df.copy(deep=True)
  replacedict = {}

  # prepare dictionary based on resistance strength
  if option==1:
    for genotype in ENCODINGDB:
      replacedict[genotype] = resistant_strength_calc(genotype, drugset)
  # prepare dictionary based on drug efficacy
  elif option==2:
    efficacydf = pd.read_csv('https://github.com/lizhewen/BoniLabMDR/raw/master/ef2020.csv')
    efficacydf = efficacydf.set_index('Shortname').iloc[:,1:]
    for genotype in ENCODINGDB:
      replacedict[genotype] = round(efficacydf.loc[genotype,drugset], 3)
  else:
    print("Option not found.")
    return None

  # Replace Column names with their corresponding MDR Strength   
  df.rename(columns=replacedict,inplace=True)

  # Sum-up the columns sharing the same name and return
  return df.groupby(by=df.columns, axis=1).sum()

def coloring_legend(mdr_case, option):
  # Helper function to give correct legend colors
  #   based on MDR intensity.

  # for drug-mutationEvent format
  if option == 1:
    legend_color = {
      "0-0": "#32CD32", # green for wild type
      "1-1": "#FAD996", # light orange
      "1-2": "#FFAB00", # medium orange
      "1-3": "#C76400", # dark orange
      "2-1": "#F09187", # light red
      "2-2": "#FF1A00", # medium red
      "2-3": "#A91606", # dark red
      "2-4": "k" # black
    }
    return legend_color.get(mdr_case)
  
  # for drug-efficacy format
  elif option == 2:
    percentage = int(mdr_case*100)
    if percentage >= 90:
      return "#32CD32" # [90,∞) - green
    elif percentage >= 80:
      return "#3497FF" # [80,90) - blue
    elif percentage >= 70:
      return "#FFAB00" # [70,80) - medium orange
    elif percentage >= 60:
      return "#F09187" # [60,70) - light red
    else:
      return "#A91606" # [0,60) - dark red


