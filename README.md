# Multiple-Drug-Resistance Categorization & Case-Count Report Program

###### Author: Eric Zhewen Li<br/>Boni Lab, Center for Infectious Disease Dynamics, Penn State Huck Institutes of the Life Sciences. [mol.ax](http://mol.ax)<br/>Contact: eric@zhewenli.com<br>&copy; 2020. Under MIT License. All Rights Reserved.

This repo contains all the Jupyter Notebook files showing the outcome measure calculation functions for the Multiple-Drug-Resistance (MDR) Analysis.

## Introduction

The main program, called `BoniLabMDR.ipynb`, contains a series of functions that parses, processes, and analyzes the output file from Boni Lab's stochastic Malaria simulation models. The program also provides a series of visualizations to intuitively show the emergence of drug-resistance for Malaria.

The main program takes in the monthly reported output file from Boni Lab's Individual-Based-Microsimulation (GitHub Repo [Here](https://github.com/maciekboni/PSU-CIDD-Malaria-Simulation/)). The file is  tab-separated and in `txt` format. Currently this Python program only supports single-location scenarios - output files from [this fork](https://github.com/lizhewen/PSU-CIDD-Malaria-Simulation) of the simulation. This program intends to analyze and create visuals for the simulation, including MDR analysis for the Multiple-Firstline-Therapy (MFT).

The program is open-sourced under MIT License. There is much freedom with MIT License, but you must include the original license here and properly cite this as your source.

## How to use the program

### 1. [MDR Categorization & Case-Count Report Program](/BoniLabMDR.ipynb)

The program, written in Python, is available and presented by Jupyter Notebook and hence in `ipynb` format. You can either download the file and run it locally, or you can use [Google Colab](https://colab.research.google.com) (recommended) to open and run, by using its GitHub import function.

When you open the program, go to the "Result Assembling - Start Here" section, where it shows a sample scenario of the program usage prepared by me. If you would like to run the program using your own file, you need to first run all the functions defined in the "Function defs" section, uploading your file if you are using Google Colab, and change the parameter to your filepath. Then you can use the program and get results by calling the assembling function with corresponding plot option as parameter.

#### Plots and Options:

In the assembly (main) function, the `plot` parameter controls which plots to be returned. There are four types and they are:

1. `plot='bsp'`: This option returns blood slide prevalence plot, with 'Years' on x-axis and 'blood slide prevalence' (percentage of population) on y-axis.

2. MDR plots:

   These two options return a series of genotype frequency plots, from each ACT (drugget)'s perspectives. For example, if DHA-PPQ->AS-AQ->AL Cycling is used, three subplots will be generated, from the perspectives of DHA-PPQ (Artemisinin and PPQ), AS-AQ, AL, respectively.

   The legend is also normalized to correspond to the danger level of each genotype group:

   | Resistance Strength | Drug Efficacy | Legend Color            |
   | ------------------- | ------------- | ----------------------- |
   | 0-0                 | [90,∞)      | \#8DFD0F, green         |
   |                     | [80,90)     | \#3497FF, blue          |
   | 1-1                 |               | \#FAD996, light orange  |
   | 1-2                 | [70,80)     | \#FFAB00, medium orange |
   | 1-3                 |               | \#C76400, dark orange   |
   | 2-1                 | [60,70)     | \#F09187, light red     |
   | 2-2                 |               | \#FF1A00, medium red    |
   | 2-3                 | [0,60)      | \#A91606, dark red      |
   | 2-4                 |               | \#000000, black         |

   1. `plot='mdr1'`: This option summarizes / categorizes by each genotype's drug resistance. This options uses `resistant_strength_calc` function and the resistance is formatted as `a-b`, where `a` being  how many drugs the genotype is resistant to, and `b` being how many mutation events occurred with the genotype. Refer to the function def for more info.

   2. `plot='mdr2'`: This option summarizes by each genotype's drug efficacy.

   3. `plot='mdca'`: This option targets specifically the two most-dangerous genotypes in the simulation:
     - Encoding `TYY**Y2*`: this genotype has the highest resistance to AQ, and is also resistant to DHA-PPQ
       This includes `TYY--Y2x/X` and `TYYYYY2x/X` - they both have 0.735 efficacy under ASAQ (0.633 under AQ) and 0.415 efficacy under DHA-PPQ
     - Encoding `KNFNFY2x/X`: this genotype has the highest resistance to LM (0.422 efficacy), and is also resistant to DHA-PPQ (0.415 efficacy)

### 2. [Mutation Pair Analysis Program](/MutationPairAnalysis.ipynb)

In my fork of the simulation, there is a branch called "eric_new_reporter", where an additional file called "mut_arrival.txt" is generated apart from the other two output files. This file is comma-separated and contains info about all the mutation events occurred during the simulation, in the form of "time, from_id, to_id". This python program  takes in this file and returns a series of visuals for further analysis.

### 3. [Genotype Risk Analysis Program](/GenotypeRiskAnalysis.ipynb)

This program targets at one or more genotype of your selection, estimate a portion of the blood slide prevalence, i.e. how many people are infected by this genotype(s), and then plot a diagram. By specifying start- and end-year, the program shades the specified area under the curve, and then use `numpy.trapz` to calculate the area.

## About archives

This program could not be developed without my Summer Internship at Boni Lab of Penn State's CIDD. All the testing codes and notebooks (May-Aug 2019) are archived in the folder for references. A separate data-visualization web app is also under development.

## Future Development Area

Due to time constraint, there are several improvements could be implemented. One thing is that the parser function is now shared across two Jupyter notebooks and currently it's implemented by simply copy-and-pasting. In the future, functions should be extracted to python `.py` files and stored in Google Drive or S3 Bucket. The notebooks should be made for pure visualization purposes and import those functions as they need.
