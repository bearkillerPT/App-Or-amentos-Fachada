# -*- coding: utf-8 -*-
import csv
from calc import Piso
from typing import List

equipPrice = {}

def getEquipPrice():
    with open("precos.csv", 'rt') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            tempDict = dict(row)
            equipPrice.update({tempDict["Equipamento"] : tempDict["Preço"]})


def report(report_name: str, pisos, areaTotal, volumeTotal, potenciaBomba, numeroModulos):
    #Função para criar o excel com as divisões e equipamentos
    getEquipPrice()  
    with open(report_name, 'w', newline='') as csvfile:
        labels = ["Piso", "Divisão", "Área", "Volume", "Equipamento", "Preço", "Área Total", "Volume Total", "Potência bomba de calor", "Número de módulos"]
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=labels)
        writer.writeheader()
        for pisoName, pisoObj in list(pisos.items()):
            buildDict(pisoName, pisoObj, writer, areaTotal, volumeTotal, potenciaBomba, numeroModulos)
        precoTotal = 0
        for _, price in list(equipPrice.items()):
            precoTotal += float(price)
        writer.writerow({"Piso": "-", "Divisão": "-", "Área": "-", "Volume": "-", "Equipamento": "-", "Preço": precoTotal, "Área Total": areaTotal, "Volume Total": volumeTotal, "Potência bomba de calor": potenciaBomba, "Número de módulos": numeroModulos})

#Função para ler orçamentos através do csv            
def readOrc(filename):
    pisosReturn = {}
    with open(filename, 'rt') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            tempDict = dict(row)
            infoArr = list(tempDict.items())
            if infoArr[6][1] != "-":
                break
            pisoIndex = infoArr[0][1]
            divName = infoArr[1][1]
            area = float(infoArr[2][1])
            volume = float(infoArr[3][1])
            equipamento = infoArr[4][1]
            if not pisoCheck(pisosReturn, pisoIndex):
                pisosReturn[pisoIndex] = Piso(pisoIndex)
            pisosReturn[pisoIndex].buildDiv(divName, float(area), float(volume), equipamento)
    return pisosReturn

#Check if piso already exits

def pisoCheck(pisos: dict, pisoname: str):
    for piso, _ in pisos.items():
        if piso == pisoname:  
            return True
    return False    


def buildDict(pisoName, pisoObj: dict, writer, areaTotal, volumeTotal, potenciaBomba, numeroModulos):
    divName = ""
    divsInfoList = []
    for divName, divsInfoList in pisoObj.getDivs().items():
        tempDict =  {"Piso": pisoName, "Divisão": divName, "Área": divsInfoList[0], "Volume": divsInfoList[1], "Equipamento": divsInfoList[2], "Preço": equipPrice[divsInfoList[2]],"Área Total": "-", "Volume Total": "-", "Potência bomba de calor": "-", "Número de módulos": "-"}
        writer.writerow(tempDict)
