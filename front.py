
import streamlit as st
import pandas as pd
import time 
import base64 

@st.cache_data
def get_base64_of_bin_file(file):
    
    with open(file,"rb") as f:
        data  = f.read()
        
    return base64.b64encode(data).decode()

def set_png_as_page_bg(imagen_bg, imagen_sd):
    bin_str_bg = get_base64_of_bin_file(imagen_bg)
    bin_str_sd = get_base64_of_bin_file(imagen_sd)

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{bin_str_bg}");
    background-size: cover;
    }}
    
    [data-testid="stSidebar"] {{
    background-image: url("data:image/png;base64,{bin_str_sd}");
    background-position: center;
    }}
    </style>
    """
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return



def insert_padreada(Fecha, Faltoso, Víctima, Padreada, Puntos, historico_padreadas):
    
    with st.spinner ( 'Insertando Padreada'):
        time.sleep(2)
        nueva_frase = pd.DataFrame()
        nueva_frase['Fecha']         = [Fecha]
        nueva_frase['Faltoso']         = [Faltoso]
        nueva_frase['Víctima']       = [Víctima]
        nueva_frase['Padreada']      = [Padreada]
        nueva_frase['Puntos']  = [Puntos]
    
        historico_padreadas = pd.concat([historico_padreadas,nueva_frase])
    
        historico_padreadas.to_csv('Padreadas.csv',sep = ',')
        
    st.success ("Padreada insertada en la base de datos con éxito")

    return 

def delete_padreada(historico_padreadas, index):
    
    with st.spinner ( 'Eliminando Padreada'):
        time.sleep(2)
        
        historico_padreadas.drop( index , inplace = True)
        historico_padreadas.to_csv('Padreadas.csv',sep = ',')
        
    
    st.success ("Padreada eliminada de la base de datos con éxito")
    set_stage('Eliminar_Padreada')

    return
    
def modify_padreada(Fecha, Faltoso, Víctima, Padreada, Puntos, historico_padreadas, index):
    
    with st.spinner ( 'Modificando Padreada'):
        time.sleep(2)
        frase_modificada = pd.DataFrame()
        frase_modificada['Fecha']         = [Fecha]
        frase_modificada['Faltoso']         = [Faltoso]
        frase_modificada['Víctima']       = [Víctima]
        frase_modificada['Padreada']      = [Padreada]
        frase_modificada['Puntos']  = [Puntos]
        frase_modificada.index  = [index]
        
        historico_padreadas.loc[index] =  frase_modificada.iloc[0]
        # st.write(frase_modificada)
        
        historico_padreadas.to_csv('Padreadas.csv',sep = ',')
        
        st.success ("Padreada modificada en la base de datos con éxito")
        
    return 

def show_top(historico_padreadas) :
    
    padreador_top = historico_padreadas.groupby(['Faltoso']).sum('Puntos')
    padreado_top = historico_padreadas.groupby(['Víctima']).sum('Puntos')
    
    # padreador_top = padreador_top.to_frame()
    # padreado_top = padreado_top.to_frame()

    padreador_top.reset_index(drop = False, inplace = True)
    padreado_top.reset_index(drop = False, inplace = True)
    
    padreador_top.columns = ['Padreador','Puntos']
    padreado_top.columns = ['Padreado','Puntos']
    
    padreador_top = padreador_top.sort_values(by = 'Puntos', ascending = False).head(5)
    padreado_top = padreado_top.sort_values(by = 'Puntos', ascending = False).head(5)
    faltadas_top = historico_padreadas.sort_values(by = 'Puntos', ascending = False).head(5)

    
    padreador_top['Top'] = [f'{i}º' for i in range(1, padreador_top.shape[0] + 1)]
    padreado_top['Top'] = [f'{i}º' for i in range(1, padreado_top.shape[0] + 1)]
    faltadas_top['Top'] = [f'{i}º' for i in range(1, faltadas_top.shape[0] + 1)]
    faltadas_top.set_index('Top', inplace = True)

    col1, col2 = st.columns([1, 1]) 
    with col1:  
        st.markdown("<h3 style='color:#ffffff;font-weight:bold;font-size:20px;'>TOP 5 PADRES!!</h3>", unsafe_allow_html=True)
        st.dataframe(padreador_top[['Top','Padreador','Puntos']],
                     width = 700,
                     hide_index = True)
    with col2:  
        st.markdown("<h3 style='color:#ffffff;font-weight:bold;font-size:20px;'>TOP 5 PADREADOS!!</h3>", unsafe_allow_html=True)
        st.dataframe(padreado_top[['Top','Padreado','Puntos']],
                     width = 700,
                     hide_index = True)
     
    st.markdown("<h3 style='color:#ffffff;font-weight:bold;font-size:20px;'>TOP 5 PADREADAS!!</h3>", unsafe_allow_html=True)
    st.dataframe(faltadas_top[['Faltoso','Víctima','Padreada','Puntos']], width=1400)
        
    return

def hist_padres(historico_padreadas):
    
    padreadores = historico_padreadas.groupby(['Faltoso']).size()
    padreadores = padreadores.to_frame()
    padreadores.columns = ['Faltadas']
    st.markdown("<h3 style='color:#ffffff;font-weight:bold;font-size:20px;'>HISTOGRAMA DE PADRES!!</h3>", unsafe_allow_html=True)
    st.bar_chart(padreadores, color = "#663399"  )
    
    return

def set_stage(stage):
    
    
    st.session_state.stage = stage
    
    return 
def set_stage_pass(stage, usuario, contraseña):
    
    if usuario =='Notorious_aless99' and contraseña =='Tortuga_4':
    
    
        st.session_state.stage = stage
    else:
        st.error('¡Contraseña Incorrecta!')
    
    return 

def read_historico(ruta_csv):
    
    historico_padreadas = pd.read_csv(ruta_csv, sep  =',')
    historico_padreadas['Fecha'] = pd.to_datetime(historico_padreadas['Fecha']).dt.date
    historico_padreadas.sort_values('Fecha',ascending = False, inplace = True)
    historico_padreadas.reset_index(drop = True, inplace = True)
    
    return historico_padreadas[['Fecha','Faltoso','Víctima','Padreada','Puntos']]

def main(ruta_csv,ruta_imagen_bg,ruta_imagen_sd):
    st.set_page_config(layout="wide")

    st.session_state.historico_padreadas = read_historico(ruta_csv)
    set_png_as_page_bg(ruta_imagen_bg, ruta_imagen_sd)


    st.session_state.lst_gente = [
        'Raul',
        'Edu G',
        'Sejo',
        'Aless',
        'Edu A',
        'Leo',
        'Diego',
        'Pelaez',
        'Jair'
        ]
    with st.sidebar:
    
        st.sidebar.header('¿Qué deseas hacer?')
        st.button('Ver histórico Padreadas', on_click = set_stage, args = ['Historico'])
        st.button( '¡Administrar Padreadas!', on_click = set_stage, args = ['Password'])
    if 'stage' not in st.session_state:
        
        st.session_state.stage = 'Inicio'

    if st.session_state.stage == 'Inicio': 
        
        # st.markdown("<h1 style='color:#4b0082;font-weight:bold;'>¡Bienvenido a PADREADAS DISCORD!</h1>", unsafe_allow_html=True)
        st.title("¡Bienvenido a PADREADAS DISCORD!")

        show_top(st.session_state.historico_padreadas)
        hist_padres(st.session_state.historico_padreadas)

        
    if st.session_state.stage == 'Historico':
        
        st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    
        aux = st.session_state.historico_padreadas.set_index('Fecha')
        # Mostrar el DataFrame
        st.dataframe(aux,
                     width = 1700,
                     height = 759)

        st.button('Inicio', on_click = set_stage, args = ['Inicio'])
        
    if st.session_state.stage == 'Password':
        
        usuario = st.text_input('Usuario :' , value = 'Notorious_aless99')
        contraseña = st.text_input('Contraseña :', type = 'password')
        st.button('Continuar', on_click = set_stage_pass, args =['Administrar Padreadas', usuario,contraseña])
        st.button('Inicio', on_click= set_stage, args = ['Inicio'] )

    if st.session_state.stage == 'Administrar Padreadas':
        
        st.title("Administrador de Padreadas")
        st.markdown("<h2 style='color:#ffffff;font-weight:bold;font-size:28px;'>¿Qué desea hacer su majestad ADMINISTRADOR?</h2>", unsafe_allow_html=True)
        
        st.button( 'Insertar Padreada', on_click= set_stage, args = ['Insertar_Padreada'])
        st.button( 'Eliminar Padreada',      on_click= set_stage, args = ['Eliminar_Padreada'])
        st.button( 'Modificar Padreada',     on_click= set_stage, args = ['Modificar_Padreada'])
        st.button('Inicio', on_click= set_stage, args = ['Inicio'] )


    if st.session_state.stage == 'Insertar_Padreada':
        
        st.title("Insertar Padreadas")
        Faltoso = st.selectbox("Faltoso:", st.session_state.lst_gente)
        Víctima = st.selectbox("Víctima:", st.session_state.lst_gente)
        Padreada = st.text_input("Padreada : ")
        Puntos = st.selectbox('Puntos de la Padreada', [1,2,3,4,5])
        Fecha = st.date_input('Fecha de la Padreada')
        
        st.button('Insertar', on_click = insert_padreada, args= [Fecha,
                        Faltoso,
                        Víctima,
                        Padreada,
                        Puntos,
                        st.session_state.historico_padreadas])

        st.button('Inicio', on_click= set_stage, args = ['Inicio'] )
        
    if st.session_state.stage == 'Modificar_Padreada':
        
        st.dataframe(st.session_state.historico_padreadas,
                     use_container_width = True,
                     height = st.session_state.historico_padreadas.shape[0] * 37,
                     hide_index = False
                     )
        index = st.number_input ( 'Padreada a modificar :',
                                                  value = None,
                                                  placeholder = "Escribe el número de la padreada...",
                                                  step = 1,
                                                  min_value = 0,
                                                  max_value = st.session_state.historico_padreadas.shape[0] - 1)
        if index:
        
            Faltoso = st.selectbox("Faltoso:", 
                                 st.session_state.lst_gente, 
                                 index = st.session_state.lst_gente.index(
                                     st.session_state.historico_padreadas.loc[index,'Faltoso']
                                     )
                                 )
            
            Víctima = st.selectbox("Víctima:", 
                                 st.session_state.lst_gente, 
                                 index = st.session_state.lst_gente.index(
                                     st.session_state.historico_padreadas.loc[index,'Víctima']
                                     )
                                 )
            
            Padreada = st.text_input("Padreada : ",
                                     value = st.session_state.historico_padreadas.loc[index,'Padreada']
                                     )
            
            Puntos = st.selectbox('Puntos de la Padreada', 
                                        [1,2,3,4,5],
                                        index = [1,2,3,4,5].index(
                                            st.session_state.historico_padreadas.loc[index,'Puntos']
                                            ))
            Fecha = st.date_input('Fecha de la Padreada',
                                  value = st.session_state.historico_padreadas.loc[index,'Fecha']
                                  )
            
            st.button('Modificar', on_click = modify_padreada, args= [Fecha,
                            Faltoso,
                            Víctima,
                            Padreada,
                            Puntos,
                            st.session_state.historico_padreadas,
                            index])

        st.button('Inicio', on_click= set_stage, args = ['Inicio'] )
            

    if st.session_state.stage == 'Eliminar_Padreada':
        
        st.dataframe(st.session_state.historico_padreadas,
                     use_container_width = True,
                     height = st.session_state.historico_padreadas.shape[0] * 37,
                     hide_index = False
                     )
        st.session_state.index = st.number_input ( 'Padreada a eliminar :',
                                                  value = None,
                                                  placeholder = "Escribe el número de la padreada...",
                                                  step = 1,
                                                  min_value = 0,
                                                  max_value = st.session_state.historico_padreadas.shape[0] - 1)
        
        st.button('Eliminar', on_click= set_stage, args = ['Seguro_eliminar'])
        st.button('Inicio', on_click = set_stage, args = ['Inicio'])

    if st.session_state.stage == 'Seguro_eliminar':
        
        st.text("¿Seguro que quieres eliminar esta padreada ?")
        st.dataframe(st.session_state.historico_padreadas.iloc[st.session_state.index])
        
        st.button('Si, seguro', on_click = delete_padreada, args = [st.session_state.historico_padreadas,
                                                                    st.session_state.index])
        
        st.button('No, volver al inicio', on_click= set_stage, args = ['Inicio'])
        
        

if __name__ == "__main__":
    
    ruta_csv = 'Padreadas.csv'
    ruta_imagen_bg = 'image_op_2.jpg'
    ruta_imagen_sd = 'lebron.jpg'


    main(ruta_csv,ruta_imagen_bg, ruta_imagen_sd)
