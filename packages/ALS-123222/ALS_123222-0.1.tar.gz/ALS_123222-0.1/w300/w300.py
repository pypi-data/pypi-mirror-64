#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np


# In[ ]:


class outlier_detection(object):
    def __init__(self):
        self.lower_bound = None
        self.upper_bound = None
    def iqr(self, df, field, iqr_factor=3):
        data_list = df[[str(field)]]
        quartile_1, quartile_3 = np.percentile(data_list, [25, 75])
        iqr_value = quartile_3 - quartile_1
        lower_bound = quartile_1 - (iqr_value * iqr_factor)
        upper_bound = quartile_3 + (iqr_value * iqr_factor)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        return(lower_bound,upper_bound)


# In[1]:


get_ipython().system('jupyter nbconvert --to script w300.ipynb')


# In[ ]:




