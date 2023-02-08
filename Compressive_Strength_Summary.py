#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import os
from util.streamlit_configs import Page_layout
import pdfplumber, re, os, openpyxl, subprocess
from openpyxl.styles import Font, Alignment, Border, Side
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from fpdf import FPDF
from itertools import zip_longest
pd.options.mode.chained_assignment = None  # default='warn'

from util.concrete_test_class import concrete_test
from util.excel_class import xlsx
from util.pdf_class import PDF


# <!------ Page Configs ------>
st.set_page_config(
        page_title='Compressive Strengths',
        layout="wide",
        page_icon='👨‍🔬',
        initial_sidebar_state="collapsed")
        
app = Page_layout(title='Concrete Compressive Strengths Test Summary',
                   default_session_key_values={},
                   hide_streamlit_footer=True,
                   custom_footer='Developed by <a href="https://linkedin.com/in/rpakishore" target="_blank">Arun Kishore</a>',
                   remove_padding_from_sides=True)
app.set_pagelayout()

st.file_uploader(label="Upload Test PDF", type=["pdf"], accept_multiple_files=True, key="Uploaded_files")

if st.session_state.Uploaded_files:
        files = st.session_state.Uploaded_files
        parsed_data = []
        combine = {
                'W-1': ['W-1 180', 'W1-150', 'W-1 (200)', 'W-1(32MPA)', 'W1'],
                'W-2': ['W2', 'W-2-PEA'],
                'W-3': ['W3'],
                'W-4': ['W4'],
                'W-5': ['W5'],
                'W-6': ['W6', 'W-6 PEA', 'W-6(56)', 'W-6(32MPA)'],
                'W-7': ['W-72']
                }

        total_files = len(files)
        for idx, file in enumerate(files):
                with open(file.name, 'wb') as f:
                        f.write(file.getvalue())

                data = concrete_test(file.name)
                data.combine_sheets(combine)
                parsed_data.append(data)
                st.progress((idx+1)/total_files)

        sheets = {}
        for item in parsed_data:
                if not item.extracted_data['Mix Number'] in sheets.keys():
                        sheets[item.extracted_data['Mix Number']] = item

        st.write("Following are the list of sheets that will be currently produced")
        st.write(list(sheets.keys()))

        combine = {
        'W-1': ['W-1 180', 'W1-150', 'W-1 (200)', 'W-1(32MPA)', 'W1'],
        'W-2': ['W2', 'W-2-PEA', 'W2 (165)'],
        'W-3': ['W3'],
        'W-4': ['W4'],
        'W-5': ['W5'],
        'W-6': ['W6', 'W-6 PEA', 'W-6(56)', 'W-6(32MPA)'],
        'W-7': ['W-72']
        }
        for file in parsed_data:
                file.combine_sheets(combine)
        
        specified = {}
        for sheet in sheets.keys():
                col1, col2, col3, col4 = st.columns(4)
                for _ in range(2):
                        col1.write("")
                col1.write(sheet)
                strength = col2.number_input(label="Target Str.", min_value=0, step=5)
                days = col3.number_input(label="Target Str. Days", min_value=0, step=5)
                Label = col4.text_input(label="Label")
                specified[sheet] = [strength, days, Label]

#Update the sample data in sheets dict to point to corrent strength item
for sheet in sheets.keys():
    for item in parsed_data:
        data = item.extracted_data
        if data['Mix Number'] == sheet:
            item.extracted_data['Specified Strength'] = specified[sheet][0]
            item.extracted_data['Specified Strength Days'] = specified[sheet][1]
            sheets[sheet] = item


xl_file  = 'report_summary.xlsx'
xl = xlsx(xl_file)
for sheet in sheets.keys():
        if sheet == None:
                continue
ws, current_row = xl.create_data_sheet(sheet, sheets[sheet].extracted_data)

sets = {}

for item in parsed_data:
        if item.extracted_data['Mix Number'] != sheet or item.extracted_data['Set Num'] == None:
                continue
        set_num = int(item.extracted_data['Set Num'])
        report_date = item.extracted_data['Report Date']
        if not set_num in sets.keys():
                sets[set_num] = item
        elif len(item.extracted_data['Test Data'].dropna()) > len(sets[set_num].extracted_data['Test Data'].dropna()):
                sets[set_num] = item

for set_key in sorted(sets.keys()):
        current_row = xl.write_set_data(ws, sets[set_key].extracted_data, current_row+1)

sheets[sheet].figure = xl.plot_sheet(sets, sheet + '.png')
xl.save()
