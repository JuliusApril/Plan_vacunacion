# Librerias
#----------------------------------------------------------
from datetime import date,timedelta,datetime
import requests
import os, time
import json


# Función para descarga de informes 
#----------------------------------------------------------
def descarga_informes_vacunacion(inicio, fin, url, path):
    '''
    Esta función descarga los informes de vacunación del ministerio de Sanidad español. la url donde se alojan
    es url='https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/'.
    Introducir las fechas de inicio y fin en formato DD/MM/YYYY y el directorio donde se quieran guardar 
    los documentos.
    
    Cuando se ejecuta la función se archivan los documentos pdf en el directorio y se genera un diccionario con 
    los resultados, por lo que se recomienda asignar la función a una variable para conservar el registro de los 
    resultados.
    '''
    
    # Generacion lista de archivos
    # Inicializar las variables
    inicio=datetime.strptime(inicio,'%d/%m/%Y')    #Inferir fecha inicio.
    fin=datetime.strptime(fin,'%d/%m/%Y')         # Inferir Fecha fin
    periodo=(fin-inicio).days
    print('Días desde ',inicio,' :',periodo,'\n')

    # lista de días
    listado=['Informe_GIV_comunicacion_'+date.strftime(inicio+timedelta(days=dia),'%Y%m%d')+'.pdf' for dia in range(periodo)]
    print('\nTotal elementos en la lista: ',len(listado))
    
    # User agent
    UA = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    # crear directorio donde voy a guardar
    os.makedirs(path, exist_ok=True)
    
    # Bucle for para descargar archivos
    log={}
    for archivo in listado:
        if os.path.isfile(path+archivo):        # Comprobar si el archivo existe en nuestro directorio
            print(archivo+': Ya descargado.')        # Si existe imprimir aviso
            report=['--','Ya descargado']
        else:
        # Descarga archivo
            r=requests.get(url+archivo,
                           headers=UA)           
        # Abrir archivo y guardar
            if(r.status_code == 200):                            # Si status es 200
                print('Descargando archivo...')
                with open(path+archivo, 'wb') as fd:             # hemos descargado un archivo pdf y lo podemos
                    for chunk in r.iter_content(chunk_size=128): # guardar en nuestra carpeta.
                        fd.write(chunk)
                print(archivo+' guardado...')
                report=[r.status_code,'Creado ok']
            else:
                print(archivo,'no existe.')
                report=[r.status_code,'No existe']
        log[archivo]=report
        time.sleep(2)
    
    return log


# Ejecución script - Instanciar variables
#----------------------------------------------------------
url='https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/'
path='datasets/'
fecha_inicio=input('Intruduzca fecha inicio (formato: DD/MM/YYYY):' )
fecha_fin=input('Intruduzca fecha final (formato: DD/MM/YYYY):' )

# Ejecución script - ejecutar función
#----------------------------------------------------------
archivo_log=descarga_informes_vacunacion(fecha_inicio,fecha_fin,url, path)

# Ejecución script - crear log descarga
#----------------------------------------------------------
archivo=(path+'log_descarga.json')
with open(archivo,'w') as file:
    json.dump(archivo_log,open(archivo,'w'))
