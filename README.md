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

### 2. [Most Dangerous MDR Case Analysis Program](/MostDangerousMDR.ipynb)

This program is similar to the first program. But instead of plotting on and tracking all the genotypes, this program specifically targets at the two most dangerous genotypes:

- Encoding `TYY--Y2*`: this genotype has the highest resistance to AQ, and is also resistant to DHA-PPQ
- Encoding `KNFNFY2*`: this genotype has the highest resistance to LM, and is also resistant to DHA-PPQ

### 3. [Mutation Pair Analysis Program](/MutationPairAnalysis.ipynb)

In my fork of the simulation, there is a branch called "eric_new_reporter", where an additional file called "mut_arrival.txt" is generated apart from the other two output files. This file is comma-separated and contains info about all the mutation events occurred during the simulation, in the form of "time, from_id, to_id". This python program  takes in this file and returns a series of visuals for further analysis.

## About archives

This program could not be developed without my Summer Internship at Boni Lab of Penn State's CIDD. All the testing codes and notebooks (May-Aug 2019) are archived in the folder for references. A separate data-visualization web app is also under development.
