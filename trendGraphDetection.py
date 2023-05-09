import sys
import rrdtool
import time
import datetime
from  Notify import send_alert_attached
import time
rrdpath = '/mnt/c/Users/52557/Desktop/P3/RRD/'
imgpath = '/mnt/c/Users/52557/Desktop/P3/IMG/'

ultima_lectura = int(rrdtool.last(rrdpath+"trend.rrd"))
tiempo_final = ultima_lectura
tiempo_inicial = tiempo_final - 1800

def generarGrafica(ultima_lectura,dato,title,d1,d2,d3):
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 1800
    ret = rrdtool.graphv( imgpath+ title + ".png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Cpu load",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "--title=Carga del" + title + "\n Detección de umbrales \n Baldovinos Gutierrez Kevin",
                    "DEF:carga="+rrdpath+"trend.rrd:" + dato + ":AVERAGE",
                     "VDEF:cargaMAX=carga,MAXIMUM",
                     "VDEF:cargaMIN=carga,MINIMUM",
                     "VDEF:cargaSTDEV=carga,STDEV",
                     "VDEF:cargaLAST=carga,LAST",
                     "CDEF:umbral"+d1+"=carga,"+d1+",LT,0,carga,IF",
                     "CDEF:umbral"+d2+"=carga,"+d2+",LT,0,carga,IF",
                     "CDEF:umbral"+d3+"=carga,"+d3+",LT,0,carga,IF",
                     "AREA:carga#00FF00:Carga de " + title ,
                     "AREA:umbral"+d1+"#00FF00:Carga " + title +" mayor de "+d1+"",
                     "AREA:umbral"+d2+"#FF7A00:Carga " + title +" mayor de "+d2+"",
                     "AREA:umbral"+d3+"#FF0000:Carga " + title +" mayor de "+d3+"",
                     "HRULE:"+d1+"#00FF00:Umbral  "+d1+"%",
                     "HRULE:"+d2+"#FF7A00:Umbral  "+d2+"%",
                     "HRULE:"+d3+"#FF0000:Umbral  "+d3+"%",
                     "PRINT:cargaLAST:%6.2lf",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST" )
    
    print (ret)
    
pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/useCPU.png"
envioCPU30 = True
envioCPU75 = True
envioCPU80 = True

envioRAM30 = True
envioRAM70 = True
envioRAM80 = True

envioDisco30 = True
envioDisco70 = True
envioDisco90 = True

while (1):
    ultima_actualizacion = rrdtool.lastupdate(rrdpath + "trend.rrd")
    timestamp=ultima_actualizacion['date'].timestamp()
    CPU_data=ultima_actualizacion['ds']["CPUload"]
    RAM_data=ultima_actualizacion['ds']["RAMused"]
    Disk_data=ultima_actualizacion['ds']["Diskused"]
    #print(CPUload)
    #print(RAMused)
    #print(Diskused)
    
    if CPU_data> 80 and envioCPU80:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/CPU.png"
        generarGrafica(int(timestamp),"CPUload","CPU","30","75","80")
        send_alert_attached("-----NOTIFICACIÓN: USO EXCESIVO CPU-----","El uso del CPU esta por encima del 80%, favor de tomar las medidas correspondientes. Nombre del dispositivo: LAPTOP-KHO3L8D1 ; S.O.: Windows ; Nodo detectado: 1.3.6.1.2.1.25.3.3.1.2.5 ; Info. de contacto del dispositivo: baldovinosgutierrezkevin@gmail.com", pathImage)
        envioCPU80 = False
        print("Enviado")
    elif CPU_data >75 and envioCPU75:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/CPU.png"
        generarGrafica(int(timestamp),"CPUload","CPU","30","75","80")
        send_alert_attached("-----NOTIFICACIÓN: USO MODERADO CPU-----","El uso del CPU esta por encima del 75%, favor de monitoriar el uso. Nombre del dispositivo: LAPTOP-KHO3L8D1 S.O.: Windows ; Nodo detectado: 1.3.6.1.2.1.25.3.3.1.2.5 ; Info. de contacto del dispositivo: ", pathImage)
        envioCPU75 = False
        print("Enviado")
    elif CPU_data > 30 and envioCPU30:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/CPU.png"
        generarGrafica(int(timestamp),"CPUload","CPU","30","75","80")
        envioCPU30 = False
        send_alert_attached("-----NOTIFICACIÓN: USO NORMAL CPU-----","El uso del CPU esta por encima del 30%. Nombre del dispositivo: LAPTOP-KHO3L8D1 S.O.: Windows Nodo detectado: 1.3.6.1.2.1.25.3.3.1.2.5 Info. de contacto del dispositivo: ", pathImage)
        print("Enviado")
    
    if RAM_data> 80 and envioRAM80:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/RAM.png"
        generarGrafica(int(timestamp),"RAMused","RAM","30","70","80")
        send_alert_attached("-----NOTIFICACIÓN: USO EXCESIVO RAM-----","El uso de la RAM esta por encima del 80%, favor de tomar las medidas correspondientes. Nombre del dispositivo: LAPTOP-KHO3L8D1 ; S.O.: Windows Nodo detectado: 1.3.6.1.2.1.25.2.3.1.5. ;  Info. de contacto del dispositivo: @gmail.com", pathImage)
        envioRAM80 = False
        print("Enviado")
    elif RAM_data >70 and envioRAM70:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/RAM.png"
        generarGrafica(int(timestamp),"RAMused","RAM","30","70","80")
        send_alert_attached("-----NOTIFICACIÓN: USO MODERADO RAM-----","El uso de la RAM esta por encima del 70%, favor de monitoriar el uso. Nombre del dispositivo: LAPTOP-KHO3L8D1 S.O.: Windows ; Nodo detectado: 1.3.6.1.2.1.25.2.3.1.5.3 ; Info. de contacto del dispositivo: @gmail.com", pathImage)
        envioRAM70 = False
        print("Enviado")
    elif RAM_data > 30 and envioRAM30:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/RAM.png"
        generarGrafica(int(timestamp),"RAMused","RAM","30","70","80")
        envioRAM30 = False
        send_alert_attached("-----NOTIFICACIÓN: USO NORMAL RAM-----","El uso de la RAM esta por encima del 30%., Nombre del dispositivo: LAPTOP-KHO3L8D1 S.O.: Windows ; Nodo detectado: 1.3.6.1.2.1.25.2.3.1.5.3 ; Info. de contacto del dispositivo: @gmail.com", pathImage)
        print("Enviado")

    """if Disk_data> 90 and envioDisco90:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/Disco.png"
        generarGrafica(int(timestamp),"Diskused","Disco","30","70","90")
        send_alert_attached("-----NOTIFICACIÓN: USO EXCESIVO DISCO-----","El uso del Disco esta por encima del 90%, favor de tomar las medidas correspondientes.",pathImage)
        envioDisco90 = False
        print("Enviado")
    elif Disk_data >70 and envioDisco70:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/Disco.png"
        generarGrafica(int(timestamp),"Diskused","Disco","30","70","90")
        send_alert_attached("-----NOTIFICACIÓN: USO MODERADO DISCO-----","El uso del Disco esta por encima del 70%, favor de monitoriar el uso del Disco.",pathImage)
        envioDisco70 = False
        print("Enviado")
    elif Disk_data > 30 and envioDisco30:
        pathImage = "/mnt/c/Users/52557/Desktop/P3/IMG/Disco.png"
        generarGrafica(int(timestamp),"Diskused","Disco","30","70","90")
        envioDisco30 = False
        send_alert_attached("-----NOTIFICACIÓN: USO NORMAL DISCO-----","El uso del Disco esta por encima del 30%.",pathImage)
        print("Enviado")"""
    time.sleep(30)
  
  
    

    
