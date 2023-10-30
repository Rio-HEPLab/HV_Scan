import matplotlib.pyplot
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_name= str(filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")]))

with open(file_name, 'r') as arquivo:
    conteudo = arquivo.read()
    

List=conteudo.split()
size=len(List)
event=0

while(event<size):
    if List[event]=='Correntes:':
        find=event
        event=event+1

    else:
        event=event+1


Voltagens=List[1:find]
Correntes=List[find+1:]

num=0

while(num<find-1):
    Voltagens[num]=float(Voltagens[num])
    Correntes[num]=float(Correntes[num][2:15])
    
    num=num+1


#print(Voltagens)
#print(Correntes)

matplotlib.pyplot.plot(Voltagens,Correntes)
matplotlib.pyplot.show()
