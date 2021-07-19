from altair.vegalite.v4.schema.core import DataFormat
from numpy.core.numeric import NaN
from numpy.lib.function_base import place
import streamlit as st
from google.cloud import firestore
import json
import pandas as pd
import itertools
import numpy as np

import importlib

mod = importlib.import_module('posts_page')

a = mod.app()
s = a
print(s)
def returnUsername():
    return s
# t = mod.returnRes()
# st.write(t)

# def temp1():
#         return 8

# result = mod.pyt()
# print('final: ',result)


# st.title('Home')

# st.write('This is the `home page` of this multi-page app.')

# st.write('In this app, we will be building a simple classification model using the Iris dataset.')
# hashtag_filter = st.sidebar.multiselect(
# 'Select hashtag',
# options=['1','3'])
