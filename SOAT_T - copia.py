# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 08:31:20 2021

@author: EFERNANDEZ
"""
import streamlit as st
import pandas as pd
from PIL import Image



### condiciones de la pagina e importación del logo
st.set_page_config(page_title= "SOAT Crecer Seguros",layout="wide")
image = Image.open('logo.PNG')
st.sidebar.image(image, width = 300)


###### importamos información de los excel
ruta = 'Tarifario SOAT 202102.xlsx'
t_digital = pd.read_excel(ruta,sheet_name= "TD_Crecer_M",header = 7, index_col =[0,1,2],engine ='openpyxl' )
t_fisico = pd.read_excel(ruta,sheet_name= "TF_Crecer_M",header = 7, index_col =[0,1,2] ,engine ='openpyxl')

t_digital["llave"] = t_digital.index.copy()
t_digital.set_index("llave",append= True , inplace = True)
t_fisico["llave"] = t_fisico.index.copy()
t_fisico.set_index("llave",append= True , inplace = True)



###### asignamos las comisiones
b_comision = pd.DataFrame(t_digital["CATEGORIA"].copy())
b_comision["com default"] = 0

b_comision.loc["CARGA","com default"] =14
b_comision.loc["PARTICULAR","com default"] = 14
b_comision.loc["TRANSPORTE URBANO","com default"] = 10

usos_comision = (list(b_comision.index.unique(0)))
b_comision.loc[(usos_comision ,['Vehículo Menor']),"com default"] = 8 # sin importar el uso, la com de VM es 8%


### partimos asumiendo que la comisión calculada es la misma que default
b_comision["com calculada"] = b_comision["com default"].copy()

#comisiones posibles a calcular ( los que se mostraran para seleccionar)

com_pa = list(range(7,21))   #particular
com_tu = list(range(5,16))   #transporte urbano
com_ca = list(range(7,21))   # carga
com_vm = list(range(5,16))   # vehículo menor


#valores de uso y departamento a seleccionar
uso = list(t_digital.index.unique(0))     #La lista unica de usos
departamento = list(t_digital.columns)   #lista de columnas
departamento = departamento[1:]          # excluimos las dos primeeras (categoria y descripción)


st.title(""" Tarifario SOAT """)
st.sidebar.header('Parametros')




def main():

    fi_uso = st.multiselect("Seleccione el USO", uso,uso)
    
    if not  fi_uso:
        st.error("Seleccione al menos un USO")
    
    else:
        clase =  list(t_digital.loc[fi_uso].index.unique(1))
        
        fi_clase = st.multiselect("Seleccione la CLASE",clase ,clase)
        
        fi_departamento = st.multiselect("Seleccione la DEPARTAMENTO", departamento, departamento[:10])                
        
        
        
        
        # asignamos las posibles comisiones
        fi_com_pa = st.sidebar.selectbox("Seleccione comisión PARTICULAR", com_pa, index= 7 )
        fi_com_tu = st.sidebar.selectbox("Seleccione comisión TRANSPORTE URBANO", com_tu, index= 5 )
        fi_com_ca = st.sidebar.selectbox("Seleccione comisión CARGA", com_ca, index= 7 )
        fi_com_vm = st.sidebar.selectbox("Seleccione comisión VEHÍCULO MENOR", com_vm, index= 3 )
        
        
        # introducimos en la base de comisiones
        b_comision.loc["CARGA","com calculada"] = fi_com_ca
        b_comision.loc["PARTICULAR","com calculada"] = fi_com_pa
        b_comision.loc["TRANSPORTE URBANO","com calculada"] =  fi_com_tu
        b_comision.loc[(usos_comision ,['Vehículo Menor']),"com calculada"] = fi_com_vm
        
        
        #calculamos el efecto x comisiones
        b_comision["efecto"] = (100-b_comision["com default"])/(100-b_comision["com calculada"])
        
        #b_comision["efecto"] = 1.5
        t_digital1 = t_digital[departamento].mul(b_comision["efecto"], axis = 0 , level = "llave").round()
        t_fisico1 = t_fisico[departamento].mul(b_comision["efecto"], axis = 0 , level = "llave").round()
        
        
        st.subheader('DIGITAL')
      
        bd =  t_digital1.reset_index(level = "llave" , drop = True) 
        bd = bd[bd.index.isin(fi_uso, level=0)]
        bd = bd[bd.index.isin(fi_clase, level=1)]
        bd = bd.dropna()
        st.dataframe(bd[fi_departamento], width=1600, height=600)
     
            
        st.subheader('FISICO') 
        
        bf =  t_fisico1.reset_index(level = "llave" , drop = True) 
        bf = bf[bf.index.isin(fi_uso, level=0)]
        bf = bf[bf.index.isin(fi_clase, level=1)]
        bf = bf.dropna()
        st.dataframe( bf[fi_departamento], width=1600, height=600)
    
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