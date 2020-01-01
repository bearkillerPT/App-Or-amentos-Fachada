# -*- coding: utf-8 -*-
class Piso:

    def __init__(self, pisoName):
        self.name = pisoName
        self.divs = {}

    def getDivs(self):
        return self.divs

    def getName(self):
        return self.name

    #Para o csv construir sem saber ponteciaref e alturaref
    def buildDiv(self, divname, area, volume, equipamento):
        self.divs[divname] = [area, volume, equipamento]

    def addDiv(self, divName, area, potenciaRef, alturaRef):
        potenciaDiv = potenciaRef * area
        volume = area * potenciaRef
        equipamento = ""
        if potenciaDiv < 2000:
            equipamento = "SL200"
        elif potenciaDiv < 4000:
            equipamento = "SL400"
        elif potenciaDiv < 6000:
            equipamento = "SL600"
        elif potenciaDiv < 8000:
            equipamento = "SL800"
        elif potenciaDiv < 10000:
            equipamento = "SL1000"
        else:
            equipamento = "verificar!"
        self.divs[divName] = [area, volume, equipamento]

    def removeDiv(self, divName):
        del self.divs[divName]

    def totalArea(self):
        total = 0
        for (_, info) in self.divs.items():
            total += info[0]
        return total

    def printDivs(self):
        for (divname, info) in self.divs.items():
            print("Divisão: " + divname + "\n\tArea: " + str(info[0]) + "\n\tVolume: " + str(info[1]) + "\n\tEquipamento: " + info[2])

    def totalVolume(self):
        total = 0
        for (_, info) in self.divs.items():
            total += info[1]
        return total

