# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 20:14:56 2020

@author: hunte
"""
import glob
import pandas as pd
import plotly.graph_objects as go

class DataSet():
    def __init__(self,set_name,path):
        self.set_name = set_name
        self.path = path
        self.files = []
        self.frames = []
        self.big_data = []
        self.fig = go.Figure()
        self.num_plots = 0
        self.num_figs = 0
        
        self.build()

    def build(self):
        self.fig.update_layout(title=self.set_name)
        print('Searching for files...')
        # Populate self.files with paths of all .csv files in path directory
        for file in glob.glob(self.path + "\\*.csv"):
            self.files.append(file)
        print('Found ', str(len(self.files)), 'files!\n')
        
        print('Reading File Data...')
        # Read all files in self.files to dataframes in self.frames after
        # dropping first two rows of zeros
        for i in range(len(self.files)):
            curr_frame = pd.read_csv(self.files[i])
            curr_frame = curr_frame.drop([0,1])
            self.frames.append(curr_frame)
        print('Reading complete!\n')
        
        print('Combining file data...')
        # Concatenate all dataframes in self.frames into a big frame in self.bigData
        self.big_data = pd.concat(self.frames)
        # Sort by reference time
        self.big_data = self.big_data.sort_values(' Reference_time1')
        # Reset frame index values
        self.big_data = self.big_data.reset_index(drop=True)
        print('Data combination complete!\n')
        
    def add_plot(self,axis1,axis2,color):
        self.num_plots+=1
        print('Adding plot'+ axis2 + ' vs.' + axis1 + ' as plot '+ str(self.num_plots) +'...')
        # Create line plot of axis1 vs axis 2
        self.fig.add_trace(
            go.Scattergl(
                x = self.big_data[axis1],
                y = self.big_data[axis2],
                mode = 'lines',
                name = axis2,
                line=dict(color=color),
                showlegend=True
            )
        )
        print('Done!\n')
        
    def show(self):
        print('Showing plots...')
        # Show current figure
        self.fig.show(renderer='png')
        print('Done!\n')
        
    def export_figure(self,file):
        print('Exporting figure to HTML...')
        self.fig.write_html(file,
                            include_plotlyjs='cdn',
                            include_mathjax='cdn')
        print('Done!\n')
        
    def clear_fig(self):
        print('Clearing figure...')
        self.num_plots=0
        self.fig.data=[]
        print('Done!\n')
        
    def export_bigdata(self):
        print('Exporting bigdata file...')
        # Output self.big_data to a .csv in a zip folder in cwd
        compression_opts = dict(method='zip',
                                archive_name='big_data.csv')  
        self.big_data.to_csv(self.set_name+'.zip', index=False,compression=compression_opts)
        print('Output complete!\n')
        
if __name__ == '__main__':
   path = "C:\\Users\\hunte\\OneDrive - BYU\\Documents\\Github\\Power-Plot\\power_data\\2020_Power_Data\\8_6"
   new_data = DataSet('8-6 Etch',path)
   new_data.add_plot(' Reference_time1', ' Reference Power','red')
   new_data.export_figure('8-6 Reference Power.html')
   new_data.clear_fig()
   new_data.add_plot(' Confocal_time',' Confocal Power','blue')
   new_data.export_figure('8-6 Confocal Power.html')
   