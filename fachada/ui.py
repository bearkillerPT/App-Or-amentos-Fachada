# -*- coding: utf-8 -*-
import math
import os
import copy
from calc import Piso
import tkinter
from ttkthemes import themed_tk as tk
from tkinter import ttk
from tkinter import filedialog
import csvCommunicator as csvComm
from scrframe import VerticalScrolledFrame
from PIL import ImageTk, Image

class appfachada:
    def __init__(self):    
        self.HEIGHT = 450
        self.WIDTH = 900
        self.pisos = {}
        self.alturaref = 2.7
        self.potenciaref = 80
        self.delete_entry = Image.open("images/delete.png")
        self.rowCount = 0
        self.filename = ""
        self.lastOpened = {}


    def numeroTotalModulos(self, totalArea):
        return math.ceil(totalArea * 0.05)

    def checkPiso(self, pisoName):
        for piso, _ in self.pisos.items():
            if piso == pisoName:
                return True
        return False

    def checkDiv(self, piso, divName):
        tempDiv = piso.getDivs()
        for divN, _ in tempDiv.items():
            if divN == divName:
                return True
        return False

    def clicked(self, root, totalArea, totalVolume, numeroModulos, potenciaBomba):
        #Arranjar acesso aos widgets
        sub_root = list(root.children.values())
        input_frame = sub_root[3]
        bottom_frame = sub_root[4]
        footer_frame = sub_root[5]
        input_frame_widgets = list(input_frame.children.values())
        bottom_frame_widgets = list(bottom_frame.children.values())
        footer_frame_widgets = list(footer_frame.children.values())

        #Calculo e display dos resultados
        pisoTemp = input_frame_widgets[0].get()
        newPiso = Piso(pisoTemp)
        if not self.checkPiso(pisoTemp):
            self.pisos[pisoTemp] = newPiso
        if not self.checkDiv(self.pisos[pisoTemp], input_frame_widgets[1].get()):
            self.pisos[pisoTemp].addDiv(input_frame_widgets[1].get(), float(input_frame_widgets[2].get()), self.potenciaref, self.alturaref)
            pisoDivs = self.pisos[pisoTemp].getDivs()
            string_result = "Piso: " + pisoTemp + "      Tipo: " + input_frame_widgets[1].get() + "      Área: " + input_frame_widgets[2].get() + "      Equipamento: " + pisoDivs[input_frame_widgets[1].get()][2] + "\n"
            totalAreacalc = 0
            for _, piso in self.pisos.items():
                totalAreacalc += piso.totalArea()
            
            #Precisao das casas decimais
            self.totalAreaVal = round(totalAreacalc,3)
            self.totalVolumeVal = round(self.totalAreaVal * self.alturaref,3)
            self.numeroTotalModulosVal = self.numeroTotalModulos(self.totalAreaVal)
            self.potenciaBombaVal = round((self.totalAreaVal * self.potenciaref)/1000,3)
            totalArea.set("Area: " + str(self.totalAreaVal) + "m\u00b2")
            totalVolume.set("Volume: " + str(self.totalVolumeVal) + "m\u00b3")
            numeroModulos.set("Módulos estimados: " + str(self.numeroTotalModulosVal))
            potenciaBomba.set("Potência bomba de calor: " + str(self.potenciaBombaVal) + "kW")
            
            #UI adcionar entradas
            entry_frame = ttk.Frame(bottom_frame_widgets[0].interior)
            label = ttk.Label(entry_frame, text=string_result, justify="center")
            label.config(anchor="center")
            deleteButton = ttk.Button(entry_frame)
            deleteButton.config(image=self.delete_entry_image, command=lambda: self.deleteEntry(deleteButton))
            label.grid(row=self.rowCount, column=0, pady=10, sticky=tkinter.N)
            deleteButton.grid(row=self.rowCount, column=1, padx=40, pady=10)
            self.rowCount += 1
            entry_frame.pack()

    def save(self, openToo, bottom_frame, root, areaTotal, volumeTotal, numeroModulos, potenciaBomba):
        self.filename = filedialog.asksaveasfile(mode="w", defaultextension=".csv").name
        csvComm.report(self.filename, self.pisos, self.totalAreaVal, self.totalVolumeVal, self.potenciaBombaVal, self.numeroTotalModulosVal)
        self.lastOpened = copy.deepcopy(self.pisos)
        if openToo == True:
            frame.children = {}
            vertScrl_Frame = VerticalScrolledFrame(bottom_frame)
            vertScrl_Frame.pack(fill="both", expand="yes")
            vs_space_label = ttk.Label(vertScrl_Frame.interior)
            vs_space_label.pack()
            self.getFileAndBuild(root, vertScrl_Frame, areaTotal, volumeTotal, numeroModulos, potenciaBomba)
        

    def getInfo(self, startIndex, keyWord, infoArr):
        info = ""
        lastIndex = 1
        for i in range(startIndex, len(infoArr)):
            if infoArr[i] == keyWord:
                lastIndex = i
                break
        for i in range(startIndex, lastIndex):
            info += infoArr[i] + " "
            print(info)
        return (lastIndex, info[:-1])

    #Eliminar a entrada
    def deleteEntry(self, ref):
        print(ref.master.children)
        infoStr = ref.master.children["!label"].cget("text")
        infoArr = infoStr.split()
        i = 1
        lastind, piso = self.getInfo(1, "Tipo:", infoArr)
        lastind, tipo = self.getInfo(lastind + 1, "Área:", infoArr)
        ref.master.destroy()
        self.pisos[piso].removeDiv(tipo)
        

    def createConfigWindow(self, root):
        window = tkinter.Toplevel(root, width=500, height=500)
        window.title = "Configurações"

        #frames
        left_conf_frame = ttk.Frame(window)
        right_conf_frame = ttk.Frame(window)
        left_conf_frame.place(relheight=1, relwidth=0.5)
        right_conf_frame.place(relheight=1, relwidth=0.5, relx=0.5)

        #labels
        potRefLabel = ttk.Label(left_conf_frame, text="Potência de Referência: ")
        alturaRefLabel = ttk.Label(left_conf_frame, text="Altura de Referência: ")
        potRefLabel.place(relheight=0.125, relwidth=0.8, relx=0.1, rely=0.125)
        alturaRefLabel.place(relheight=0.125, relwidth=0.8, relx=0.1, rely=0.325)

        #Entrys
        potRefEntry = ttk.Entry(right_conf_frame, justify="center")
        alturaRefEntry = ttk.Entry(right_conf_frame, justify="center")
        saveConfButton = ttk.Button(right_conf_frame, text="Guardar alterações!", command=lambda: self.changeConfs(window))
        potRefEntry.place(relheight=0.125, relwidth=0.8, relx=0.1, rely=0.125)
        alturaRefEntry.place(relheight=0.125, relwidth=0.8, relx=0.1, rely=0.325)
        saveConfButton.place(relheight=0.125, relwidth=0.8, relx=0.1, rely=0.755)

    def changeConfs(self, confWindow):
        sub_root = list(confWindow.children.values())
        confValWidgets = list(sub_root[1].children.values())
        self.potenciaref = int(confValWidgets[0].get())
        self.alturaref = int(confValWidgets[1].get())
        confWindow.destroy()

    def getFileAndBuild(self, root, current_Frame, totalArea, totalVolume, numeroModulos, potenciaBomba):
        self.filename = filedialog.askopenfilename()
        if len(list(current_Frame.interior.children)) > 1:
            window = tkinter.Toplevel(width=500, height=200)
            window.title = "Atenção!"
            label = ttk.Label(window, text="Ainda tem um documento aberto.")
            saveButton = ttk.Button(window, text="Guardar e abrir novo", command=lambda: self.save(True, current_Frame.parent(), root, totalArea, totalVolume, numeroModulos, potenciaBomba))
            cancelButton = ttk.Button(window, text="Cancelar", command=lambda: window.destroy())
            label.grid(row=0)
            label.config(anchor="center")
            saveButton.grid(row=1, column=0)
            cancelButton.grid(row=1, column=1)
        else:
            self.pisos = csvComm.readOrc(self.filename)
            self.lastOpened = copy.deepcopy(self.pisos)
            self.buildFrame(current_Frame.interior, totalArea, totalVolume, numeroModulos, potenciaBomba)
            

    #Função para abrir documentos cria o frame basiado na mudança do ficheiro
    def buildFrame(self, current_frame, totalArea, totalVolume, numeroModulos, potenciaBomba):
        self.rowCount = 0
        for piso, calcObj in list(self.pisos.items()):
            for div, infoArr in list(calcObj.getDivs().items()):
                string_result = "Piso: " + piso + "      Tipo: " + div + "      Área: " + str(infoArr[0]) + "      Equipamento: " + infoArr[2] + "\n"
                entry_frame = ttk.Frame(current_frame)
                label = ttk.Label(entry_frame, text=string_result, justify="center")
                label.config(anchor="center")
                deleteButton = ttk.Button(entry_frame)
                deleteButton.config(image=self.delete_entry_image, command=lambda: self.deleteEntry(deleteButton))
                label.grid(row=self.rowCount, column=0, pady=10, sticky=tkinter.N)
                deleteButton.grid(row=self.rowCount, column=1, padx=40, pady=10)
                self.rowCount += 1
                entry_frame.pack()
        totalAreacalc = 0
        for _, piso in self.pisos.items():
            totalAreacalc += piso.totalArea()
        self.totalAreaVal = round(totalAreacalc,3)
        self.totalVolumeVal = round(self.totalAreaVal * self.alturaref,3)
        self.numeroTotalModulosVal = self.numeroTotalModulos(self.totalAreaVal)
        self.potenciaBombaVal = round((self.totalAreaVal * self.potenciaref)/1000,3)
        
        #Precisao das casas decimais
        totalArea.set("Area: " + str(round(self.totalAreaVal,3)) + "m\u00b2")
        totalVolume.set("Volume: " + str(round(self.totalAreaVal * self.alturaref,3)) + "m\u00b3")
        numeroModulos.set("Módulos estimados: " + str(self.numeroTotalModulos(self.totalAreaVal)))
        potenciaBomba.set("Potência bomba de calor: " + str(round((self.totalAreaVal * self.potenciaref)/1000,3)) + "kW")

    def exitAndSaveCheck(self, root):
        if self.pisos != {}:
            if self.lastOpened == {}:
                if self.filename != "":
                    if self.pisos != csvComm.readOrc(self.filename):
                        self.save(False, "", "", "", "", "", "")
                else:
                    self.save(False, "", "", "", "", "", "")
            else:
                if not self.compareDict():
                    self.save(False, "", "", "", "", "", "")
        root.destroy()
        
    def compareDict(self):

        try:
            for key, value in list(self.pisos.items()):
                for key2, value2 in list(self.pisos[key].getDivs().items()):
                    if self.pisos[key].getDivs()[key2] != self.lastOpened[key].getDivs()[key2]:
                        return False      
            return True
        except KeyError:
            return False

    def start(self):
        # Tema da aplicacao
        root = tk.ThemedTk() #tkinter.Tk()
        root.title("Orçamentação Fachada Energética - T&T")
        root.get_themes()
        root.set_theme("plastik")
        root.protocol('WM_DELETE_WINDOW', lambda: self.exitAndSaveCheck(root))
        self.delete_entry_image = ImageTk.PhotoImage(self.delete_entry)

        #Inicializacao de variaveis footer 
        totalArea = tkinter.StringVar()
        totalVolume = tkinter.StringVar()
        numeroModulos = tkinter.StringVar()
        potenciaBomba = tkinter.StringVar()
        totalArea.set("Area total: " + str(0))
        totalVolume.set("Volume total: " + str(0))
        numeroModulos.set("Módulos estimados: " + str(0))
        potenciaBomba.set("Potência bomba de calor: " + str(0))

        #Dimensoes defeito
        screen_width = self.WIDTH #root.winfo_screenwidth()
        screen_height = self.HEIGHT #root.winfo_screenheight()
        canvas = tkinter.Canvas(root, width= screen_width, height= screen_height)
        canvas.pack()

        #Barra de menu para poder loadar ficheiros
        menuBar = tkinter.Menu(root)
        filemenu = tkinter.Menu(menuBar, tearoff=0)
        filemenu.add_command(label="Abrir", command=lambda: self.getFileAndBuild(root, vertScrl_Frame, totalArea, totalVolume, numeroModulos, potenciaBomba))
        filemenu.add_command(label="Guardar", command=lambda: self.save(False, "", "", "", "", "", ""))
        menuBar.add_cascade(label="Ficheiro", menu=filemenu)
        root.config(menu=menuBar)

        #Frame com labels
        head_frame = ttk.Frame(root)
        head_frame.place(relheight=0.1, relwidth=1)

        pisoLabel = ttk.Label(head_frame, text="Piso:")
        divLabel = ttk.Label(head_frame, text="Divisão:")
        areaLabel = ttk.Label(head_frame, text="Area:")
        configButton = ttk.Button(head_frame, text="Configurações", command=lambda: self.createConfigWindow(root))
        pisoLabel.place(relheight=0.5, relwidth=0.125, relx=0.1, rely=0.25)
        divLabel.place(relheight=0.5, relwidth=0.125, relx=0.325, rely=0.25)
        areaLabel.place(relheight=0.5, relwidth=0.125, relx=0.55, rely=0.25)
        configButton.place(relheight=0.5, relwidth=0.125, relx=0.775, rely=0.25)
        #Centrar os labels
        pisoLabel.config(anchor="center")
        divLabel.config(anchor="center")
        areaLabel.config(anchor="center")

        #Frame de inputs
        input_frame = ttk.Frame(root)
        input_frame.place(relheight=0.1, relwidth=1, rely=0.1)
        pisoEntry = ttk.Entry(input_frame, justify="center")
        divEntry = ttk.Entry(input_frame, justify="center")
        areaEntry = ttk.Entry(input_frame, justify="center")
        addBTN = ttk.Button(input_frame, text="Adicionar!", command=lambda: self.clicked(root, totalArea, totalVolume, numeroModulos, potenciaBomba))
        pisoEntry.place(relheight=0.5, relwidth=0.125, relx=0.1, rely=0.25)
        divEntry.place(relheight=0.5, relwidth=0.125, relx=0.325, rely=0.25)
        areaEntry.place(relheight=0.5, relwidth=0.125, relx=0.55, rely=0.25)
        addBTN.place(relheight=0.5, relwidth=0.125, relx=0.775, rely=0.25)

        #Frame das divisoes com equipamento
        bottom_frame = ttk.Frame(root)
        bottom_frame.place(relheight=0.6, relwidth=1, rely=0.2)
        vertScrl_Frame = VerticalScrolledFrame(bottom_frame)
        vertScrl_Frame.pack(fill="both", expand="yes")
        vs_space_label = ttk.Label(vertScrl_Frame.interior)
        vs_space_label.pack()

        #Frame footer
        footer_frame = ttk.Frame(root)
        footer_frame.place(relheight=0.2, relwidth=1, rely=0.8)
        totalAreaLabel = ttk.Label(footer_frame, textvariable=totalArea, justify="center")
        totalVolumeLabel = ttk.Label(footer_frame, textvariable=totalVolume, justify="center")
        numeroModulosLabel = ttk.Label(footer_frame, textvariable=numeroModulos, justify="center")
        potenciaBombaLabel = ttk.Label(footer_frame, textvariable=potenciaBomba, justify="center")
        totalAreaLabel.place(relheight=0.3, relwidth=0.2, relx=0.1, rely=0.1)
        totalVolumeLabel.place(relheight=0.3, relwidth=0.2, relx=0.4, rely=0.1)
        numeroModulosLabel.place(relheight=0.3, relwidth=0.2, relx=0.7, rely=0.1)
        potenciaBombaLabel.place(relheight=0.3, relwidth=0.4, relx=0.3, rely=0.6)
        #Centrar os labels
        totalAreaLabel.config(anchor="center")
        totalVolumeLabel.config(anchor="center")
        numeroModulosLabel.config(anchor="center")
        potenciaBombaLabel.config(anchor="center")

        root.mainloop()

app = appfachada()
app.start()