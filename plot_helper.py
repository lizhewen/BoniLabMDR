import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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

  headline = "current_time\tsclock_to_time\tyear\tmonth\tday\tseasonal_fac\ttreated_p_5-\ttreated_p_5+\tpopulation\tsep\tEIR_loc_yr\tsep\tblood_slide_prev\tbsp_2_10\tbsp_0_5\tsep\tmonthly_new_inf\tsep\tmon_treatment\tsep\tmon_clinical_ep\tsep\tKNY--C1x\tKNY--C1X\tKNY--C2x\tKNY--C2X\tKNY--Y1x\tKNY--Y1X\tKNY--Y2x\tKNY--Y2X\tKYY--C1x\tKYY--C1X\tKYY--C2x\tKYY--C2X\tKYY--Y1x\tKYY--Y1X\tKYY--Y2x\tKYY--Y2X\tKNF--C1x\tKNF--C1X\tKNF--C2x\tKNF--C2X\tKNF--Y1x\tKNF--Y1X\tKNF--Y2x\tKNF--Y2X\tKYF--C1x\tKYF--C1X\tKYF--C2x\tKYF--C2X\tKYF--Y1x\tKYF--Y1X\tKYF--Y2x\tKYF--Y2X\tKNYNYC1x\tKNYNYC1X\tKNYNYC2x\tKNYNYC2X\tKNYNYY1x\tKNYNYY1X\tKNYNYY2x\tKNYNYY2X\tKYYYYC1x\tKYYYYC1X\tKYYYYC2x\tKYYYYC2X\tKYYYYY1x\tKYYYYY1X\tKYYYYY2x\tKYYYYY2X\tKNFNFC1x\tKNFNFC1X\tKNFNFC2x\tKNFNFC2X\tKNFNFY1x\tKNFNFY1X\tKNFNFY2x\tKNFNFY2X\tKYFYFC1x\tKYFYFC1X\tKYFYFC2x\tKYFYFC2X\tKYFYFY1x\tKYFYFY1X\tKYFYFY2x\tKYFYFY2X\tTNY--C1x\tTNY--C1X\tTNY--C2x\tTNY--C2X\tTNY--Y1x\tTNY--Y1X\tTNY--Y2x\tTNY--Y2X\tTYY--C1x\tTYY--C1X\tTYY--C2x\tTYY--C2X\tTYY--Y1x\tTYY--Y1X\tTYY--Y2x\tTYY--Y2X\tTNF--C1x\tTNF--C1X\tTNF--C2x\tTNF--C2X\tTNF--Y1x\tTNF--Y1X\tTNF--Y2x\tTNF--Y2X\tTYF--C1x\tTYF--C1X\tTYF--C2x\tTYF--C2X\tTYF--Y1x\tTYF--Y1X\tTYF--Y2x\tTYF--Y2X\tTNYNYC1x\tTNYNYC1X\tTNYNYC2x\tTNYNYC2X\tTNYNYY1x\tTNYNYY1X\tTNYNYY2x\tTNYNYY2X\tTYYYYC1x\tTYYYYC1X\tTYYYYC2x\tTYYYYC2X\tTYYYYY1x\tTYYYYY1X\tTYYYYY2x\tTYYYYY2X\tTNFNFC1x\tTNFNFC1X\tTNFNFC2x\tTNFNFC2X\tTNFNFY1x\tTNFNFY1X\tTNFNFY2x\tTNFNFY2X\tTYFYFC1x\tTYFYFC1X\tTYFYFC2x\tTYFYFC2X\tTYFYFY1x\tTYFYFY1X\tTYFYFY2x\tTYFYFY2X\tsep\tKNY--C1x\tKNY--C1X\tKNY--C2x\tKNY--C2X\tKNY--Y1x\tKNY--Y1X\tKNY--Y2x\tKNY--Y2X\tKYY--C1x\tKYY--C1X\tKYY--C2x\tKYY--C2X\tKYY--Y1x\tKYY--Y1X\tKYY--Y2x\tKYY--Y2X\tKNF--C1x\tKNF--C1X\tKNF--C2x\tKNF--C2X\tKNF--Y1x\tKNF--Y1X\tKNF--Y2x\tKNF--Y2X\tKYF--C1x\tKYF--C1X\tKYF--C2x\tKYF--C2X\tKYF--Y1x\tKYF--Y1X\tKYF--Y2x\tKYF--Y2X\tKNYNYC1x\tKNYNYC1X\tKNYNYC2x\tKNYNYC2X\tKNYNYY1x\tKNYNYY1X\tKNYNYY2x\tKNYNYY2X\tKYYYYC1x\tKYYYYC1X\tKYYYYC2x\tKYYYYC2X\tKYYYYY1x\tKYYYYY1X\tKYYYYY2x\tKYYYYY2X\tKNFNFC1x\tKNFNFC1X\tKNFNFC2x\tKNFNFC2X\tKNFNFY1x\tKNFNFY1X\tKNFNFY2x\tKNFNFY2X\tKYFYFC1x\tKYFYFC1X\tKYFYFC2x\tKYFYFC2X\tKYFYFY1x\tKYFYFY1X\tKYFYFY2x\tKYFYFY2X\tTNY--C1x\tTNY--C1X\tTNY--C2x\tTNY--C2X\tTNY--Y1x\tTNY--Y1X\tTNY--Y2x\tTNY--Y2X\tTYY--C1x\tTYY--C1X\tTYY--C2x\tTYY--C2X\tTYY--Y1x\tTYY--Y1X\tTYY--Y2x\tTYY--Y2X\tTNF--C1x\tTNF--C1X\tTNF--C2x\tTNF--C2X\tTNF--Y1x\tTNF--Y1X\tTNF--Y2x\tTNF--Y2X\tTYF--C1x\tTYF--C1X\tTYF--C2x\tTYF--C2X\tTYF--Y1x\tTYF--Y1X\tTYF--Y2x\tTYF--Y2X\tTNYNYC1x\tTNYNYC1X\tTNYNYC2x\tTNYNYC2X\tTNYNYY1x\tTNYNYY1X\tTNYNYY2x\tTNYNYY2X\tTYYYYC1x\tTYYYYC1X\tTYYYYC2x\tTYYYYC2X\tTYYYYY1x\tTYYYYY1X\tTYYYYY2x\tTYYYYY2X\tTNFNFC1x\tTNFNFC1X\tTNFNFC2x\tTNFNFC2X\tTNFNFY1x\tTNFNFY1X\tTNFNFY2x\tTNFNFY2X\tTYFYFC1x\tTYFYFC1X\tTYFYFC2x\tTYFYFC2X\tTYFYFY1x\tTYFYFY1X\tTYFYFY2x\tTYFYFY2X\tsep\t\t"

  # define name of temporary dummy file
  dummy_file = file_name[:-4] + '_parsed.txt'
  # open original file in read mode and dummy file in write mode
  with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
    # Write given line to the dummy file
    write_obj.write(headline + '\n')
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
  encodingdb = ['KNY--C1x', 'KNY--C1X', 'KNY--C2x', 'KNY--C2X', 'KNY--Y1x', 
                'KNY--Y1X', 'KNY--Y2x', 'KNY--Y2X', 'KYY--C1x', 'KYY--C1X', 
                'KYY--C2x', 'KYY--C2X', 'KYY--Y1x', 'KYY--Y1X', 'KYY--Y2x', 
                'KYY--Y2X', 'KNF--C1x', 'KNF--C1X', 'KNF--C2x', 'KNF--C2X', 
                'KNF--Y1x', 'KNF--Y1X', 'KNF--Y2x', 'KNF--Y2X', 'KYF--C1x', 
                'KYF--C1X', 'KYF--C2x', 'KYF--C2X', 'KYF--Y1x', 'KYF--Y1X', 
                'KYF--Y2x', 'KYF--Y2X', 'KNYNYC1x', 'KNYNYC1X', 'KNYNYC2x', 
                'KNYNYC2X', 'KNYNYY1x', 'KNYNYY1X', 'KNYNYY2x', 'KNYNYY2X', 
                'KYYYYC1x', 'KYYYYC1X', 'KYYYYC2x', 'KYYYYC2X', 'KYYYYY1x', 
                'KYYYYY1X', 'KYYYYY2x', 'KYYYYY2X', 'KNFNFC1x', 'KNFNFC1X', 
                'KNFNFC2x', 'KNFNFC2X', 'KNFNFY1x', 'KNFNFY1X', 'KNFNFY2x', 
                'KNFNFY2X', 'KYFYFC1x', 'KYFYFC1X', 'KYFYFC2x', 'KYFYFC2X', 
                'KYFYFY1x', 'KYFYFY1X', 'KYFYFY2x', 'KYFYFY2X', 'TNY--C1x', 
                'TNY--C1X', 'TNY--C2x', 'TNY--C2X', 'TNY--Y1x', 'TNY--Y1X', 
                'TNY--Y2x', 'TNY--Y2X', 'TYY--C1x', 'TYY--C1X', 'TYY--C2x', 
                'TYY--C2X', 'TYY--Y1x', 'TYY--Y1X', 'TYY--Y2x', 'TYY--Y2X', 
                'TNF--C1x', 'TNF--C1X', 'TNF--C2x', 'TNF--C2X', 'TNF--Y1x', 
                'TNF--Y1X', 'TNF--Y2x', 'TNF--Y2X', 'TYF--C1x', 'TYF--C1X', 
                'TYF--C2x', 'TYF--C2X', 'TYF--Y1x', 'TYF--Y1X', 'TYF--Y2x', 
                'TYF--Y2X', 'TNYNYC1x', 'TNYNYC1X', 'TNYNYC2x', 'TNYNYC2X', 
                'TNYNYY1x', 'TNYNYY1X', 'TNYNYY2x', 'TNYNYY2X', 'TYYYYC1x', 
                'TYYYYC1X', 'TYYYYC2x', 'TYYYYC2X', 'TYYYYY1x', 'TYYYYY1X', 
                'TYYYYY2x', 'TYYYYY2X', 'TNFNFC1x', 'TNFNFC1X', 'TNFNFC2x', 
                'TNFNFC2X', 'TNFNFY1x', 'TNFNFY1X', 'TNFNFY2x', 'TNFNFY2X', 
                'TYFYFC1x', 'TYFYFC1X', 'TYFYFC2x', 'TYFYFC2X', 'TYFYFY1x', 
                'TYFYFY1X', 'TYFYFY2x', 'TYFYFY2X']
  replacedict = {}

  # prepare dictionary based on resistance strength
  if option==1:
    for genotype in encodingdb:
      replacedict[genotype] = resistant_strength_calc(genotype, drugset)
  # prepare dictionary based on drug efficacy
  elif option==2:
    efficacydf = pd.read_csv('https://github.com/lizhewen/BoniLabMDR/raw/master/ef2020.csv')
    efficacydf = efficacydf.set_index('Shortname').iloc[:,1:]
    for genotype in encodingdb:
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


