import openpyxl 

Meses = {
    "Enero": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "June": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Octubre": "10",
    "Noviembre": "11",
    "Diciembre": "12"
}

#hora_1 oblitario
def ordenar_fechas(horas: list):
    #sorted(horas, key = lambda fecha: fecha.split(" ")[0].split("/")[1])
    meses = {}
    resultado = []
    for i in horas:
        mes_consultado = i.split(" ")[0].split("/")[1]
        if not mes_consultado in meses:
            meses[mes_consultado] = [i]
        else:
            meses[mes_consultado].append(i)
    for i in meses.keys():
        meses[i].sort()
    lista = list(meses.keys())
    lista.sort()
    for i in lista:
        resultado += meses[i]
    return resultado

#formato: (2h y 30m)
#extrae horas y minutos segun formato anterior
def horas_minutos(horas_texto:str):
    horas_texto = horas_texto.split("y")
    hora, minuto = 0,0
    for i in horas_texto:
        j = ""
        for h in i:
            if h.isdigit():
                j += h
            else:
                if h == "h":
                    hora = int(j)
                elif h == "m":
                    minuto = int(j)

    return hora, minuto

#formato 12:30
#de la cantidad de horas y minutos se le suman 10 horas ya que se asume hora de inicio 10:00
def hora_termino(hora):
    hora, minuto = horas_minutos(hora)
    texto = str(hora+10)+":"+str(minuto)
    if minuto == 0:
        texto+="0"
    return texto

def convertir_formato_fecha_tita(texto):
    descripcion, fecha = texto.split(" --> ")
    mes, year = fecha.split(",")
    mes, dia  = mes.split(" ")
    if int(dia) < 10:
        dia = "0"+dia
    return dia+"/"+Meses[mes]+" "+descripcion


#extrae horas del texto
def horas_texto(nombre_archivo_1: list, nombre_archivo_2 = ""):
    with open(nombre_archivo_1, "r") as fd:
        data = fd.readlines()
    data_oficial = []
    for i in data:
        if not "nada" in i.split(" ")[1]:#i.split(" ")[1] != "nada\n":
            data_oficial.append(i.replace("\n", ""))
    if nombre_archivo_2 != "":

        with open(nombre_archivo_2, "r") as fd:
            data_2 = fd.readlines()

        for i in data_2:
            if not "nada" in i.split(" ")[1]:#i.split(" ")[1] != "nada\n":
                texto_nuevo = convertir_formato_fecha_tita(i)
                data_oficial.append(texto_nuevo.replace("\n", ""))
    data_oficial = ordenar_fechas(data_oficial)
    return data_oficial

def total_horas_formato(hora_min):
    hora, min = hora_min
    if hora == 1:
        if min == 0:
            mensaje = "1 hora"
        else:
            #min != 0
            mensaje = "1 hora y "+str(min)+ " min"
    elif hora == 0:
        mensaje = str(min) + " min"
    elif min == 0:
        mensaje = str(hora) + " horas"
    else:
        mensaje = str(hora) + " horas y "+str(min)+ " min"
    return mensaje

def cantidad_horas(horas):
    min = horas%60
    hora = (horas-min)//60
#    print("H: {}, M: {}".format(hora, min))
    if min == 0:
        return (str(hora)+" horas", hora, min)    
    return (str(hora)+" horas y "+str(min)+" min", hora, min)

def descripcion(desc):
    mensaje = ""
    if "rea" in desc:
        mensaje = "Creación"
        if "ifu" in desc:
            mensaje += " y difusión"
    elif "ifu" in desc:
        mensaje = "Difusión"
    mensaje += " de contenido"
    return mensaje

def extraer_info(nombre_archivo_horas, nombre_archivo_horas_2 = ""):
    
    lista_horas = []
    horas_oficiales = horas_texto(nombre_archivo_horas, nombre_archivo_horas_2)
    total_horas = 0
    for i in horas_oficiales:    
        hora = ""
        if len(i.split("(")) == 2:
            hora = "("+i.split("(")[1]
        
        fecha = i.split(" ",1)[0]
        desc = i.split("(")[0].split(" ",1)[1]
        if hora == "":
            if "ifusi" in desc.split(" ")[0]:
                hora = "1 hora"
        else:
            hora = hora.replace("(", "").replace(")","")
            hora = hora.replace("h ", " horas ")
        
        temp = hora_termino(hora).split(":")
        total_horas += (int(temp[0])-10)*60+int(temp[1])
        lista = [fecha,"10:00", hora_termino(hora), descripcion(desc), total_horas_formato(cantidad_horas((int(temp[0])-10)*60+int(temp[1]))[1:])]
    #fecha, hora inicio, hora fin, trabajo, total minutos
        
        lista_horas.append(lista)
    return lista_horas, total_horas
    
def horas_minutos_digitos(hora, min):
    if min == "":
        min = "0"
    if hora == "":
        hora = "0"
    horas = ""
    minutos = ""
    for i in hora:
        if i.isdigit():
            horas+=i
    for i in min:
        if i.isdigit():
            minutos += i
    return int(horas), int(minutos)

def hora_minuto_split(texto):
    if " y " in texto:
        hora, min = texto.split(" y ")
        horas, minutos = horas_minutos_digitos(hora, min)
        return horas, minutos
    elif "hora" in texto:
        return horas_minutos_digitos(texto,"")
    else:
        return horas_minutos_digitos("",texto)
def horas_texto_a_numero(texto, texto_2):
    
    
    horas, minutos = hora_minuto_split(texto)

    horas_2, minutos_2 = hora_minuto_split(texto_2)
    
    horas += horas_2
    minutos += minutos_2
    if minutos >59:
        horas = horas + minutos//60
        minutos = minutos%60
    horas = str(horas)
    minutos = str(minutos)
    
    text = ""
    if minutos != "0" and horas:
        text = horas + " horas y " + minutos + " min"
        if int(minutos) < 10:
            return text, str(10+int(horas))+":0"+minutos
        return text, str(10+int(horas))+":"+minutos
    elif horas:
        if int(horas) == 1:
            return "1 hora", "11:00"
        return horas + " horas", str(10+int(horas))+":00"
    else:
        if int(minutos) < 10:
            return minutos + " min", "10:0"+minutos
        return minutos + " min", "10:"+minutos


def duplicados_horas(lista_horas):
    dias = {}
    for i in range(len(lista_horas)):
        if lista_horas[i][0] in dias:
            hora_final_texto, hora_final = horas_texto_a_numero(lista_horas[i][4], dias[lista_horas[i][0]][4])
            #                                 29/04             10:00             11:00        Descripcion       1 hora
            dias[lista_horas[i][0]] = [lista_horas[i][0], lista_horas[i][1],  hora_final, lista_horas[i][3], hora_final_texto   ]
        else:
            dias[lista_horas[i][0]] = lista_horas[i]
    return list(dias.values())
    
def agregar_a_excel(nombre_archivo_excel, nombre_archivo_horas, nombre_archivo_horas_2 = ""):
    lista_horas, total_horas = extraer_info(nombre_archivo_horas, nombre_archivo_horas_2)
    lista_horas = duplicados_horas(lista_horas)
    
    wb = openpyxl.Workbook() 
    sheet = wb.active 
    fil = 1
    for lista in lista_horas:    
        col = 65
        for j in lista:
            pos = chr(col)+str(fil)
            c = sheet[pos] 
            c.value = j
            col += 1
        fil += 1
    sheet[f'A{fil}'].value = "TOTAL"
    pos = "B"+str(fil)
    c = sheet[pos]
    c.value = cantidad_horas(total_horas)[0]
    pos = "C"+str(fil)
    c = sheet[pos]
    c.value = "$"+str(total_horas*(3500/60))
    wb.save(filename = nombre_archivo_excel)

def main():
    import yaml
    with open("datos.yml", "r") as archivo:
        datos = yaml.safe_load(archivo)

    nombre_excel = datos["excel"]
    nombre_horas_1 = datos["hora_1"]
    nombre_horas_2 = datos["hora_2"]
    agregar_a_excel(nombre_excel, nombre_horas_1, nombre_horas_2)

if __name__ == "__main__":
    main()