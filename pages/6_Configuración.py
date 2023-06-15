import numpy as np
import pandas as pd
import configparser
from math import ceil
import streamlit as st

st.set_page_config(page_title='FilmQAp', layout="wide")

st.title('Configuración')

config = configparser.ConfigParser(default_section=None)
configfile='config/filmQAp.config'
config.read(configfile)

numcols = 4
sections = config.sections()
numsections = len(sections)
numrows = ceil(numsections/numcols)

col1, col2, col3, col4 = st.columns(numcols)
cols = [col1, col2, col3, col4]

asec = np.empty(numrows*numcols, dtype=object)
for i in range(numsections):
    asec[i] = sections[i]

asec = asec.reshape(numrows, numcols)

for row in range(numrows):
    for col, section in zip(cols, asec[row, ...]):
        with col:
            if section:
                st.header(section)
                with st.form(section):
                    for key in config[section]:
                        config[section][key] = st.text_input(key, value=config[section][key])
                    submitted = st.form_submit_button(label='Actualizar', help='Modificar la configuración actual')
                    if submitted:
                        with open(configfile, 'w') as cfgfile:
                            config.write(cfgfile)

with st.sidebar:
    def scannerUpdate():
        st.write(scanner)

    scanner = st.selectbox('Digitalizador', ['Microtek 1000XL', 'EPSON 10000XL'], help='Seleccionar el digitalizador utilizado', on_change=scannerUpdate)
    calfilename = st.file_uploader('Dosis de calibración:', help='Seleccionar el archivo de texto exportado del planificador.')

    if calfilename is not None:
        # Leer el fichero DICOM
        calfdf = pd.read_csv(calfilename, header=8, sep='\s+', names=['cm', 'cGy'])
        calfdf.cGy = calfdf.cGy / 100
        calfdf.rename({'cGy' : 'Gy'}, axis=1, inplace=True)

        calfdf

        calfdf.rename({'cm' : 'z', 'Gy' : 'D'}, axis=1, inplace=True)

        calfdf.to_excel('config/TestCal.xlsx')
