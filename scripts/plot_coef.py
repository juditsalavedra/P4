#! /usr/bin/python3 -u
import struct
import matplotlib as po
import matplotlib.pyplot as plt
po.use('TkAgg')
import os

current_dir = os.getcwd()
print(f"El directorio actual es: {current_dir}")

#Moverse al directorio anterior
os.chdir("..")

#Solicitar al usuario el nombre del archivo
filename = input("Ingrese el nombre del archivo: ")

#Leer los datos desde el archivo de texto
with open(os.path.join(current_dir, filename), "r") as f:
   data = f.readlines()

# Leer los datos desde el archivo de texto
#with open("lp_2_3.txt", "r") as f:
#data = f.readlines()

#Separar las columnas 
x = []
y = []
for line in data:
    columns = line.split()
    x.append(float(columns[0]))
    y.append(float(columns[1]))

#Crear el gráfico de puntos
plt.scatter(x, y)

#Ajustar los límites de los ejes
plt.xlim(min(x) - 0.5, max(x) + 0.5)
plt.ylim(min(y) - 0.5, max(y) + 0.5)

#Etiquetas a los ejes
plt.xlabel("Coeficiente 2")
plt.ylabel("Coeficiente 3")

plt.show()