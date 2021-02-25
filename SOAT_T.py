# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 08:31:20 2021

@author: EFERNANDEZ
"""
import streamlit as st
import pandas as pd
from PIL import Image

############ titulo ###########


st.set_page_config(page_title= "SOAT Crecer Seguros",layout="wide")

image = Image.open('logo.PNG')

st.sidebar.image(image, width = 300)




ruta = 'Tarifario SOAT 202102.xlsx'
t_digital = pd.read_excel(ruta,sheet_name= "TD_Crecer_M",header = 7, index_col =[0,1],engine ='openpyxl' )
t_fisico = pd.read_excel(ruta,sheet_name= "TF_Crecer_M",header = 7, index_col =[0,1] ,engine ='openpyxl')

#,engine ='openpyxl'

uso = list(t_digital.index.unique(0))



departamento = list(t_digital.columns)
departamento = departamento[2:]

st.title(""" Tarifario SOAT """)

 
st.sidebar.header('Parametros')


def main():

   
  
   
    fi_uso = st.sidebar.multiselect("Seleccione el USO", uso,uso)
    
    if not  fi_uso:
        st.error("Seleccione al menos un USO")
    
    else:
        clase =  list(t_digital.loc[fi_uso].index.unique(1))
        
        fi_clase = st.sidebar.multiselect("Seleccione la CLASE",clase ,clase)
        
        fi_departamento = st.sidebar.multiselect("Seleccione la DEPARTAMENTO", departamento, departamento[:6])
        
    
    
        
        fi_departamento.insert(0,"DESCRIPCION")
        
        st.subheader('DIGITAL')
        #st.write(""" DIGITAL """)  
        
        bd = t_digital[t_digital.index.isin(fi_uso, level=0)]
        bd = bd[bd.index.isin(fi_clase, level=1)]
        
        st.dataframe(bd[fi_departamento], width=1200, height=600)
     
            
        st.subheader('FISICO') 
        
        bf = t_fisico[t_fisico.index.isin(fi_uso, level=0)]
        bf = bf[bf.index.isin(fi_clase, level=1)]
        
        st.dataframe( bf[fi_departamento], width=1200, height=600)
    
        st.markdown('---')
        
        st.markdown(""" **Riesgo /1** : Daewoo Tico, Daewoo Matiz, Suzuki Maruti, Hyundai Stellar, Hyundai i10, Hyundai EON,
                    Suzuki Alto, Suzuki Celerio, Chevroler Spark, Chevrolet Aveo, Chevrolet Sail, Toyota Starlet, Reanult Logan, 
                    Toyota Yaris, Toyota Corolla, Kia Picanto y todos los modelos no disponibles en el catalogo vigente. """)    
      
        st.markdown(""" **Riesgo /2** : Toyota Caldina, Toyota Sprinter, Toyota Probox, Toyota Succeed,
                    Nissan AD, Nissan AD Van, Nissan AD Wagon, Nissan Wingroad, Nissan Avenir, Mazda Familia,
                    Mitsubishi Libero y todos los modelos no disponibles en el catalogo vigente. """)    

        st.markdown(""" **Riesgo /3** : Toyota Hiace, Toyota Town Ace, Toyota Lite Ace, Toyota Regius,
                    Hyundai H1, Hyundai Starex, Hyundai Grace. Nissan Vanette, Nissan Homy, Nissan Urvan,
                    JAC Refine, Volkwagen Transporte. """)    

        st.markdown(""" **Riesgo /4** :  Hyundai Porter, Hyundai H100, Hyundai HD65, Hyundai HD72, Mitsubishi Canter,
                    Toyota Dina, Toyota Toyoace, Nissan Atlas, Kia Frontier, Kia K, Daihatsu Delta 
                    y todos los modelos no disponibles en el catalogo vigente """)    
        
        st.markdown(""" ** No Riesgo /5**: Ducati, Harley Davidson, BMW, Triumph, Vespa, KTM """) 
        
        st.markdown(""" **Riesgo /6** : las marcas y modelos Hyundai H100, Kia K2700 y  Chevrolet N300 Work. 
                    Estas son consideradas Baranda o No Baranda """)  
main()        