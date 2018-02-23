#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 19:18:48 2017

@author: mattsears
"""

import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull


def getVisualIntakesOnly(data):
    return data[data['category'] == 'Visual Intake']


def getAOIsOnly(data, aois):
    return data[data['aoi'].isin(aois)]


def convertTypes(data):
    for c in ['ind', 'x', 'y']:
        data[c] = pd.to_numeric(data[c])
        
    return data


def fixIndices(data):
    #TODO come back to this later and handle indices better,
    #but just throw out the badIndices for now
    
    global badIndices  # delete line after testing

    if(data.groupby(data['ind']).nunique()['x'].max() > 1):
        indCount = data.groupby(data['ind']).nunique()['x']
        badIndices = indCount[indCount > 1]
        data = data[~data['ind'].isin(badIndices.index)] # remove the bad indices
        
        data = data.sort_values(['aoi', 'rtime'])
        
    return data


def getSingleIndices(data):
    data = data.drop_duplicates('ind')
    
    return data


def getCleandata(file, aois):
    data = pd.read_table(file, sep = ',', header = 0,
                             usecols = [0, *range(2, 7)],
                             names = ['rtime', 'category', 'ind', 'x', 'y',
                                      'aoi'])
    
    data = getVisualIntakesOnly(data)
    data = getAOIsOnly(data, aois)
    data = convertTypes(data)
    
    data = fixIndices(data)
    data = getSingleIndices(data)
    
    data.reset_index(inplace = True, drop = True)
    
    return data


def getSlices(data, colName, gap):
    global cuts
    cuts = data[data[colName] > gap].index.values.tolist()
    
    start = 0
    slices = []
    
    for end in cuts:
        end = end - data.index[0]
        slices.append(data[start:end])
        start = end
    slices.append(data[start:])
        
    return slices


def removeTooShortViewings(slices, minTime):
    remove = []
    
    for i, s in enumerate(slices):
        sliceDur = s.iloc[-1].rtime - s.iloc[0].rtime
        
        if(sliceDur < minTime):
            remove.append(i)
            
    remove = remove[::-1]
    
    for i in remove:
        del slices[i]
        
    return slices


def getAOIViewings(data, aoi, gap, minTime):
    data = data[data['aoi'] == aoi]
    
    slices = getSlices(data, 'duration', gap)
    viewings = removeTooShortViewings(slices, minTime)
    
    return viewings


def setViewings(data, aoi, gap, minTime):
    global viewings
    global viewing
    viewings = getAOIViewings(data, aoi, gap, minTime)
    
    for vi, viewing in enumerate(viewings):
        # Set viewing number
        viewingNum = vi + 1
        viewing['viewing'] = viewingNum
        
        viewing['newDuration'] = viewing['rtime'].diff()
        
        viewing = viewing[['newDuration', 'viewing']]
        
        data.update(viewing)
    
    return data
    

def preProcessFiles(files, periods, aois, viewingGap = 5000,
                 viewingMinTime = 10000):
    
    global data        # delete line after testing
    global viewings    # delete line after testing
    global allData     # delete line after testing
    
    allData = pd.DataFrame()
    
    for pi, period in enumerate(periods):
        ### PERIOD ################################################## PERIOD ###
        
        for fi, file in enumerate(files):
            ### FILE ################################################## FILE ###
            print()
            print('File: ' + file)
            
            data = getCleandata(file, aois)
            
            data['file'] = file
            data['period'] = period
            
            data['duration'] = data['rtime'].diff()
            
            data['viewing'] = np.nan
            
            cols = ['period', 'file', 'aoi', 'viewing', 'ind', 'rtime', 'x', 'y', 'duration']
            
            data = data[cols]
            
            data['newDuration'] = np.nan
            
            for ai, aoi in enumerate(aois):
                ### AOI ################################################ AOI ###                
                data = setViewings(data, aoi, viewingGap, viewingMinTime)
                
                data['duration'] = data['newDuration']
                
                viewingCount = len(data[data['aoi'] == aoi].groupby('viewing'))
                
                for vi in range(1, viewingCount + 1):
                    ### VIEWING #################################### VIEWING ###                    
                    print('Period: ' + str(period) + '    AOI: ' + str(aoi) +
                          '    Viewing: ' + str(vi))
                    
                    viewing = data[(data['aoi'] == aoi) & (data['viewing'] == vi)]
            
            del data['newDuration']
                            
            data = data[~data['viewing'].isnull()]
            
            allData = allData.append(data)
            
    return allData


def getHulls(data):
    # TODO split-apply-combine
    #pick back up here!!!
    return data


def makeConvexHullAnimations(files, periods, aois, viewingGap = 5000,
                 viewingMinTime = 10000, appendResults = True):
    
    global oldResults  # delete line after testing
    global data        # delete line after testing
    
    data = preProcessFiles(files, periods, aois, viewingGap = 5000,
                 viewingMinTime = 10000)
    
    data = getHulls(data)
    oldResults = pd.read_excel('./results/results.xlsx')
    
#    allData = pd.DataFrame()
                
                
                
                
                    
# =============================================================================
# TESTING
# =============================================================================


files = ['./BeGaze Data/Raw Data/Participant 01.txt',
         './BeGaze Data/Raw Data/Participant 02.txt',
         './BeGaze Data/Raw Data/Participant 03.txt',]

# =============================================================================
# files = ['./BeGaze Data/Raw Data/Participant 01.txt',
#          './BeGaze Data/Raw Data/Participant 02.txt',
#          './BeGaze Data/Raw Data/Participant 03.txt',
#          './BeGaze Data/Raw Data/Participant 04.txt',
#          './BeGaze Data/Raw Data/Participant 05.txt',
#          './BeGaze Data/Raw Data/Participant 06.txt',
#          './BeGaze Data/Raw Data/Participant 07.txt',
#          './BeGaze Data/Raw Data/Participant 08.txt',
#          './BeGaze Data/Raw Data/Participant 09.txt',
#          './BeGaze Data/Raw Data/Participant 10.txt',
#  ]
# =============================================================================

#aois = ['Spool 1', 'Spool 2']
aois = ['Spool 1', 'Spool 2', 'Spool 3', 'Spool 4', 'Spool 5', 'Spool 6', 'Spool 7', 'Spool 8', 'Spool 9', 'Spool 10']
periods = [3000, 5000]

file = './BeGaze Data/Raw Data/Participant 01.txt'
period = 3000
aoi = 'Spool 1'
viewingGap = gap = 5000
viewingMinTime = minTime = 10000
vi = 0


makeConvexHullAnimations(files, periods, aois)            

