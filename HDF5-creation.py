#!/usr/bin/env python
# coding: utf-8

# In[3]:


import h5py as h5
import pylab as pl
import os
import time
import json


# In[66]:


class HDF5:
    '''This is a class for creating HDF5 files'''
    
    def f_creation(self, HDF5fname, grpname, struct_name, dfname, averages, Vpp):
        ''' 
            This is a function to create an HDF5 file.
            The data is organized into groups which in
            my case corresponds to a particular type of
            measurement (over here this are MOKE MH loops).
            
            Other groups should be created for other types of
            measurement data for this sample.
            
        '''
        with h5.File(HDF5fname, 'w') as f:
    
            g = f.create_group(grpname)
            
            if grpname == 'MH_loops':
                
                g_metadata = {'Date': time.time(),
                            'User': 'Guru',
                            'Axes':['Time', 'X field', 'Y field', 
                                    'Kerr signal', 'Ref', 'Processed'],
                            'Units':['s', 'A/m', 'A/m', 
                                     'V', 'V', 'V']},
                m = g.create_dataset('metadata', data=json.dumps(g_metadata))
    
                dsquare = g.create_dataset(struct_name,
                        data=pl.loadtxt(dfname, skiprows=3))
    
                dsquare.attrs['averages'] = averages
                dsquare.attrs['Vpp'] = Vpp
            
    def f_readout(self, HDF5fname, grpname, struct_name, query):
        '''
            This is a function to read in an HDF5 file for
            processing data. Note that (especially if the data
            is large), then data processing may need to be done
            with the HDF5 file open
        
        '''
        with h5.File(HDF5fname, 'r') as f:
    
            if query == 'data':
            
                return f[grpname+'/'+struct_name][:]
            
            elif query == 'metadata':
                
                return json.loads(f[grpname+'/metadata'][()])[0]


# In[74]:


x = HDF5()
x.f_creation(HDF5fname = 'IBM_bi_ring_S1.hdf5',
             grpname = 'MH_loops',
             struct_name = 'Square_marker',
             dfname = 'IBM-S1-square-marker-v1-corrected.dat',
             averages = 256, Vpp = 8)

d = x.f_readout(HDF5fname = 'IBM_bi_ring_S1.hdf5',
             grpname = 'MH_loops',
             struct_name = 'Square_marker',
             query = 'data')

print(d.shape)

m = x.f_readout(HDF5fname = 'IBM_bi_ring_S1.hdf5',
             grpname = 'MH_loops',
             struct_name = 'Square_marker',
             query = 'metadata')

print(m.keys())


# In[ ]:




