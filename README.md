# Volcano Plotter for RNA Seq data by Mongan, Rutland & Jeyapalan Group

![A_detailed_and_vibrant_landscape-sized_image_of_a_volcano_plot](https://github.com/Rodhanp/RNA_Seq_Volcano_Plotter_Mongan_Rutland_Jeyapalan_Group/assets/71846548/c28fd06d-7d86-43bd-830c-25daa7ac2658)

This repository contains the link to the executable file for the Volcano Plot Application. See the latest release to download the .exe file.

## Description

The Volcano Plot Application is a tool designed to help visualize and analyze data in the form of a volcano plot. It is useful for identifying changes in large data sets, particularly in fields such as genomics and proteomics.

## Installation

To use the application, simply download the `Volcano_Plot_App_05062024.exe` file from the repository and run it on your Windows machine.

## User Guide for Volcano Plot Generator

### Introduction

The Volcano Plot Generator is a desktop application designed for visualising biological data through volcano plots, which are useful for identifying statistically significant gene expressions in biological studies. This application allows users to upload their data, specify parameters for analysis, and generate visual representations of their results.

### System Requirements

- Operating System: Windows
- Required: No additional installations or Python required; all necessary components are embedded in the executable.

### Installation

1. Download the executable file for your operating system.
2. Place the executable in a desired directory.
3. Double-click the file to run the application.

### Preparing Your Data

Your input data should be in a CSV (Comma-Separated Values) format with at least the following columns:
- `gene`: The identifier for the gene. **IF YOU DON'T HAVE GENE NAMES COLUMN, LEAVE IT BLANK AND THE SCRIPT WILL GENERATE A PLOT WITHOUT GENE LABELS.**
- `log2FoldChange`: Logarithmic fold change of gene expression. **ENSURE THE COLUMN HAS THE SAME HEADING.**
- `pvalue`: The p-value associated with the gene expression test.
- `padj` (optional): Adjusted p-value, if available.

**IF ANY DATA IS MISSING, or is NA, na, NaN or '0', THE SCRIPT WILL STILL WORK, IT WILL GIVE YOU A NOTIFICATION ABOUT MISSING DATA AND GIVE YOU OPTION TO DROP ROWS or SET A DEFAULT VALUE (which you can add) FOR MISSING ROWS.**
**IF YOU HAVE INSERTED BLANK ROWS (For e.g., to divide the significant values, it will drop the rows, so don't worry about that)**
**IF THERE ARE MISSING VALUES FOR P-VALUE OR PADJ, IT WILL PROMPT YOU THE OPTION TO REPLACE ALL THE MISSING VALUES WITH THE LOWEST P-VALUE OR PADJ VALUE IN YOUR SPREADSHEET**

### Starting the Application

Upon launching the application, you will see a main window divided into two panels: the input panel on the left and the plot display panel on the right.

#### Input Panel

- **Invert log2FoldChange Values**: If you check this box, the data in the log2FoldChange column will be multiplied by -1 to invert it. You can use this if you wish to change how the data is plot-compared to control or treated. If you uncheck the box, you will have to re-select the data to get a new plot.
- **Significance Metric**: Select either "p-value" or "adjusted p-value" to set the criteria for statistical significance.
- **Select Data**: Click this button to upload your CSV file.
- **Significant Threshold**: Enter a numerical threshold for significance (e.g., 0.05 for p-value).
- **Downregulated in Treated (positive value if analysis is compared to control) Threshold**: Enter the threshold for considering genes as significantly downregulated.
- **Upregulated in Treated (negative value if analysis is compared to control) Threshold**: Enter the threshold for considering genes as significantly upregulated.
- **Number of Genes to Highlight**: Enter the number of top significant genes you wish to highlight in the plot.
- **Plot Title**: Customise the title of the volcano plot.
- **X Axis Title and Y Axis Title**: Customise the labels for the X and Y axes.
- **Font Size**: Set the font size for annotations in the plot.
- **DPI for Saving Plot**: Set the DPI (dots per inch) for saving high-resolution images of your plots.
- **Highlight Genes**: Enter specific gene names to highlight them in the plot, separated by commas or spaces.
- **Update Plot**: Click to refresh the plot with the current settings. **YOU WILL HAVE TO CLICK THIS EVERYTIME YOU MAKE ANY CHANGES TO USER INPUTS.**
- **Save Plot**: Save the generated plot to a file format of your choice.

### Generating and Viewing Plots

Once your data is loaded and parameters set:
1. Click **Update Plot** to visualise the data. The plot will appear in the right panel.
2. Adjust parameters as needed and click **Update Plot** again to refine the plot.

### Saving Your Plot

- After generating the plot, click **Save Plot**.
- Choose your desired format and location to save the image file.

### Tips and Troubleshooting

- Ensure the CSV file is formatted correctly with required columns.
- If errors occur, check for missing data or incorrect data types in the input file.

### Closing the Application

- Simply close the window to exit the application.

## Features

- Easy-to-use interface
- Supports large data sets
- Customizable plot parameters
- Export plots as images

## Requirements

- Windows OS
