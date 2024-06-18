# Instructions to run the Volcano Plot Generator script

# Prerequisites:
# 1. Python 3.x installed on your system.
# 2. Required libraries installed. You can install them using the following commands:
#    ```
#    pip install pyqt5 pandas matplotlib numpy adjustText
#    ```

# How to run the script:
# 1. Save this script to a file, for example, `volcano_plot.py`.
# 2. Open a terminal or command prompt.
# 3. Navigate to the directory where `volcano_plot.py` is saved.
# 4. Run the script using the command:
#    ```
#    python volcano_plot.py
#    ```

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QFileDialog, QMessageBox, QInputDialog, QCheckBox)
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from adjustText import adjust_text
import re
from PyQt5.QtWidgets import QComboBox


class VolcanoPlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Volcano Plot Generator'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 600
        self.initUI()
        self.significance_metric = 'pvalue'  # Default to p-value
        self.invert_log2fold_change = True  # Default is to invert


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Main widget and layout
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        mainLayout = QHBoxLayout()  # Horizontal layout for the whole window
        self.widget.setLayout(mainLayout)

        # Left panel for inputs
        inputLayout = QVBoxLayout()
        mainLayout.addLayout(inputLayout, 1)  # Adding input layout to the main layout

        # Checkbox for inverting log2FoldChange values
        self.invert_checkbox = QCheckBox("Invert log2FoldChange Values")
        self.invert_checkbox.setChecked(True)  # Default checked state
        self.invert_checkbox.stateChanged.connect(self.change_invert_state)
        inputLayout.addWidget(self.invert_checkbox)

        # Adding widgets to the input layout
        # Dropdown for selecting significance metric
        inputLayout.addWidget(QLabel('Significance Metric:'))
        self.metric_selector = QComboBox()
        self.metric_selector.addItems(['p-value', 'adjusted p-value'])
        self.metric_selector.currentIndexChanged.connect(self.change_metric)
        inputLayout.addWidget(self.metric_selector)

        inputLayout.addWidget(QPushButton('Select Data', clicked=self.load_data))
        inputLayout.addWidget(QLabel('Significant Threshold:'))
        self.significant_threshold_entry = QLineEdit('0.05')
        inputLayout.addWidget(self.significant_threshold_entry)

        inputLayout.addWidget(QLabel('Downregulated in Treated (positive value) Threshold:'))
        self.upregulated_threshold_entry = QLineEdit('0.5866')
        inputLayout.addWidget(self.upregulated_threshold_entry)

        inputLayout.addWidget(QLabel('Upregulated in Treated (negative value) Threshold:'))
        self.downregulated_threshold_entry = QLineEdit('-0.5855')
        inputLayout.addWidget(self.downregulated_threshold_entry)

        inputLayout.addWidget(QLabel('Number of Genes to Highlight:'))
        self.number_of_genes_entry = QLineEdit('10')
        inputLayout.addWidget(self.number_of_genes_entry)

        inputLayout.addWidget(QLabel('Plot Title:'))
        self.title_entry = QLineEdit('Volcano Plot')
        inputLayout.addWidget(self.title_entry)

        inputLayout.addWidget(QLabel('X Axis Title:'))
        self.x_axis_title_entry = QLineEdit('Fold Change (Log2)')  # Default value
        inputLayout.addWidget(self.x_axis_title_entry)

        inputLayout.addWidget(QLabel('Y Axis Title:'))
        self.y_axis_title_entry = QLineEdit('Significance (-Log10)')  # Default value
        inputLayout.addWidget(self.y_axis_title_entry)

        inputLayout.addWidget(QLabel('Font Size:'))
        self.font_size_entry = QLineEdit('9')
        inputLayout.addWidget(self.font_size_entry)

        inputLayout.addWidget(QLabel('DPI for Saving Plot:'))
        self.dpi_entry = QLineEdit('300')  # Default DPI value
        inputLayout.addWidget(self.dpi_entry)

        inputLayout.addWidget(QLabel('Highlight Genes (comma or space-separated):'))
        self.gene_names_entry = QLineEdit()
        inputLayout.addWidget(self.gene_names_entry)

        inputLayout.addWidget(QPushButton('Update Plot', clicked=self.update_plot))
        inputLayout.addWidget(QPushButton('Save Plot', clicked=self.save_plot))

        # Right panel for graph
        graphLayout = QVBoxLayout()
        mainLayout.addLayout(graphLayout, 3)  # Graph layout takes more space

        # Matplotlib canvas
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvas(self.fig)
        graphLayout.addWidget(self.canvas)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', QtCore.QDir.homePath(), 'CSV Files (*.csv)')
        if file_path:
            # Load the data from the file
            try:
                self.df = pd.read_csv(file_path, na_values=['NA', 'na'])
            except Exception as e:
                QMessageBox.critical(self, 'Load Error', f'An error occurred while loading the file: {e}')
                return  # Exit the function if loading fails

            # Successfully loaded, now process the dataframe
            self.df.dropna(how='all', inplace=True)
            
            if self.df[self.significance_metric].isnull().any() or (self.df[self.significance_metric] == 0).any():
                self.handle_missing_data()

            if self.invert_log2fold_change:
                self.df['log2FoldChange'] *= -1

            self.update_plot()
        else:
            # File dialog was cancelled or no file was selected
            QMessageBox.information(self, 'No File', 'No file was selected.')

    def change_invert_state(self, state):
        # Update the invert state based on the checkbox
        self.invert_log2fold_change = (state == QtCore.Qt.Checked)

    def handle_missing_data(self):
        if (self.df[self.significance_metric] == 0).any():
            min_nonzero_value = self.df[self.df[self.significance_metric] > 0][self.significance_metric].min()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setWindowTitle('Handle Zero P-values')
            msg.setText(f"Atleast one data entry has value '0' in the column for {self.significance_metric}. Would you like to replace them with the lowest non-zero {self.significance_metric} value ({min_nonzero_value})?")
            replace_button = msg.addButton('Replace', QMessageBox.AcceptRole)
            remove_button = msg.addButton('Remove Points', QMessageBox.RejectRole)
            cancel_button = msg.addButton('Cancel', QMessageBox.RejectRole)
            msg.setDefaultButton(cancel_button)

            response = msg.exec_()

            if msg.clickedButton() == replace_button:
                self.df[self.significance_metric].replace(0, min_nonzero_value, inplace=True)
            elif msg.clickedButton() == remove_button:
                self.df = self.df[self.df[self.significance_metric] != 0]
            else:
                return  # Do nothing if cancel is selected

        if self.df[self.significance_metric].isnull().any():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setWindowTitle('Handle Missing Data')
            msg.setText("The data contains NaN values in critical columns. How would you like to handle it?")
            remove_button = msg.addButton('Remove Points', QMessageBox.AcceptRole)
            fill_button = msg.addButton('Fill with Default Value', QMessageBox.AcceptRole)
            cancel_button = msg.addButton('Cancel', QMessageBox.RejectRole)
            msg.setDefaultButton(cancel_button)

            response = msg.exec_()

            if msg.clickedButton() == remove_button:
                # Removing NaN values by direct assignment
                self.df = self.df.dropna(subset=[self.significance_metric])
            elif msg.clickedButton() == fill_button:
                value, ok = QInputDialog.getDouble(self, 'Enter Fill Value', 'Enter the value to use for filling missing values:', min=0.0, decimals=4)
                if ok:
                    # Apply the fill operation by direct assignment
                    self.df[self.significance_metric] = self.df[self.significance_metric].fillna(value)

    def change_metric(self, index):
        # Update the significance metric based on the user's choice
        self.significance_metric = 'pvalue' if index == 0 else 'padj'

    def save_plot(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save File", 
            "", 
            "PNG Files (*.png);;PDF Files (*.pdf);;TIFF Files (*.tiff);;JPG Files (*.jpg);;SVG Files (*.svg);;All Files (*)", 
            options=options
        )
        if file_path:
            dpi = int(self.dpi_entry.text())  # Get the DPI value from the entry
            self.fig.savefig(file_path, dpi=dpi)

    def update_plot(self):
        if hasattr(self, 'df') and self.df is not None:
            self.ax.clear()  # Clearing the plot for the update

            # Extract parameters from the GUI
            significant_threshold = float(self.significant_threshold_entry.text())
            log2FoldChange_upregulated_threshold = float(self.upregulated_threshold_entry.text())
            log2FoldChange_downregulated_threshold = float(self.downregulated_threshold_entry.text())
            number_of_genes = int(self.number_of_genes_entry.text())
            plot_title = self.title_entry.text()
            x_axis_title = self.x_axis_title_entry.text()
            y_axis_title = self.y_axis_title_entry.text()
            font_size = float(self.font_size_entry.text())
            metric = self.significance_metric

            # Check if the 'gene' column exists
            gene_column_exists = 'gene' in self.df.columns

            # Process data depending on the selected metric
            self.df['neg_log10_value'] = -np.log10(self.df[metric])

           
            # Highlighting and plotting logic using 'metric'
            sig_genes = self.df[(self.df[self.significance_metric] < significant_threshold)]

            # Highlight based on log2FoldChange thresholds
            # Plotting logic
            
            sig_up = sig_genes[sig_genes['log2FoldChange'] > log2FoldChange_upregulated_threshold]
            sig_down = sig_genes[sig_genes['log2FoldChange'] < log2FoldChange_downregulated_threshold]
            non_sig = self.df[(self.df[self.significance_metric] >= significant_threshold) |
                              ((self.df['log2FoldChange'] <= log2FoldChange_upregulated_threshold) &
                               (self.df['log2FoldChange'] >= log2FoldChange_downregulated_threshold))]

            # Scatter plot
            self.ax.scatter(non_sig['log2FoldChange'], non_sig['neg_log10_value'], color='grey', alpha=0.5, label='Non-significant')
            self.ax.scatter(sig_up['log2FoldChange'], sig_up['neg_log10_value'], color='red', label='Upregulated')
            self.ax.scatter(sig_down['log2FoldChange'], sig_down['neg_log10_value'], color='blue', label='Downregulated')

            # Highlighting top N significant genes
            texts = []
            if gene_column_exists:
                # Preparing to highlight top genes by sorting
                top_genes = self.df.sort_values(by=[self.significance_metric, 'log2FoldChange'], ascending=[True, False]).head(number_of_genes)
                for _, row in top_genes.iterrows():
                    color = 'red' if row['log2FoldChange'] > log2FoldChange_upregulated_threshold else 'blue'
                    text = self.ax.text(row['log2FoldChange'], row['neg_log10_value'], row['gene'], ha='right', va='bottom', fontsize=font_size)
                    texts.append(text)

                # Highlighting specific genes entered by the user
                highlight_genes = [gene_name.strip() for gene_name in re.split('[, ]+', self.gene_names_entry.text()) if gene_name]
                for gene_name in highlight_genes:
                    gene_data = self.df[self.df['gene'] == gene_name]
                    if not gene_data.empty:
                        for _, row in gene_data.iterrows():
                            color = 'red' if row[self.significance_metric] < significant_threshold and row['log2FoldChange'] > log2FoldChange_upregulated_threshold else \
                                    'blue' if row[self.significance_metric] < significant_threshold and row['log2FoldChange'] < log2FoldChange_downregulated_threshold else 'grey'
                            self.ax.scatter(row['log2FoldChange'], row['neg_log10_value'], color=color, edgecolor='black', zorder=5)
                            texts.append(self.ax.text(row['log2FoldChange'], row['neg_log10_value'], gene_name, ha='right', va='bottom', fontsize=font_size, zorder=5))

            
            # Call adjust_text once after all text elements are added
            adjust_text(texts, arrowprops=dict(arrowstyle='->', color='black'), ax=self.ax)




            
            # Annotations and aesthetic adjustments
            self.ax.axhline(y=-np.log10(significant_threshold), linestyle='--', color='grey', linewidth=0.7)
            self.ax.axvline(x=log2FoldChange_upregulated_threshold, linestyle='--', color='grey', linewidth=0.7)
            self.ax.axvline(x=log2FoldChange_downregulated_threshold, linestyle='--', color='grey', linewidth=0.7)

            self.ax.set_title(plot_title)
            self.ax.set_xlabel('Fold Change (Log2)')
            self.ax.set_ylabel('Significance (-Log10)')
            self.ax.legend()
            self.ax.set_xlabel(x_axis_title)
            self.ax.set_ylabel(y_axis_title)
           
            if self.canvas:  # If using a GUI toolkit, refresh the canvas to display the updated plot
                self.canvas.draw()
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VolcanoPlotApp()
    ex.show()
    sys.exit(app.exec_())
