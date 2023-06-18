#! /usr/bin/python3 -u

import struct

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from docopt import docopt
import numpy as np
from scipy.stats import multivariate_normal as gauss


def read_fmatrix(fileFM):
    '''
       Reads an fmatrix from a file
    '''
    try:
        with open(fileFM, 'rb') as fpFM:
            (numFrm, numCof) = struct.unpack('@II', fpFM.read(2 * 4))
            data = struct.unpack(f'@{numFrm * numCof}f', fpFM.read(numFrm * numCof * 4))
            data = np.array(data).reshape(numFrm, numCof)

            return data
    except:
        raise Exception(f'Error al leer el fichero {fileFM}')


def plotFeat(xDim, yDim, filesFeat=None, colorFeat=None, subplot=111):

    ax = plt.subplot(subplot)
    if filesFeat:
        feats = np.ndarray((0, 2))
        for fileFeat in filesFeat:
            feat = read_fmatrix(fileFeat)
            feat = np.stack((feat[..., xDim], feat[..., yDim]), axis=-1)
            feats = np.concatenate((feats, feat))

        ax.scatter(feats[:, 0], feats[:, 1], .05, color=colorFeat)

    
    param = filesFeat[0].split("/")[1].upper()

    if param != 'MFCC':
        coef1 = xDim-1
        coef2 = yDim-1
    else:
        coef1 = xDim
        coef2 = yDim
            
    plt.title(f'{param}: Dependencia coeficientes {coef1} y {coef2}')
    plt.axis('tight')
    plt.show()


########################################################################################################
# Main Program
########################################################################################################

USAGE='''
Draws the regions in space covered with a certain probability by a GMM.

Usage:
    plotGMM [--help|-h] [options] <file-feat>...

Options:
    --xDim INT, -x INT               'x' dimension to use from GMM and feature vectors [default: 0]
    --yDim INT, -y INT               'y' dimension to use from GMM and feature vectors [default: 1]
    --colorFEAT STR, -f STR           Color of the feature population [default: red]
    --limits xyLimits -l xyLimits     xyLimits are the four values xMin,xMax,yMin,yMax [default: auto]

    --help, -h                        Shows this message

Arguments:
    <file-feat>   Feature files to be plotted along the GMM 
'''

if __name__ == '__main__':
    args = docopt(USAGE)

    filesFeat = args['<file-feat>']
    xDim = int(args['--xDim'])
    yDim = int(args['--yDim'])
    colorFeat = args['--colorFEAT']

    plotFeat(xDim, yDim, filesFeat, colorFeat, 111)















# #! /usr/bin/python3 -u
# import struct
# import matplotlib as po
# import matplotlib.pyplot as plt
# po.use('TkAgg')
# import os

# current_dir = os.getcwd()
# print(f"El directorio actual es: {current_dir}")

# #Moverse al directorio anterior
# os.chdir("..")

# #Solicitar al usuario el nombre del archivo
# filename = input("Ingrese el nombre del archivo: ")

# #Leer los datos desde el archivo de texto
# with open(os.path.join(current_dir, filename), "r") as f:
#    data = f.readlines()

# # Leer los datos desde el archivo de texto
# #with open("lp_2_3.txt", "r") as f:
# #data = f.readlines()

# #Separar las columnas 
# x = []
# y = []
# for line in data:
#     columns = line.split()
#     x.append(float(columns[1])) #0 1 para mfcc
#     y.append(float(columns[2]))

# #Crear el gráfico de puntos
# plt.scatter(x, y)

# #Ajustar los límites de los ejes
# plt.xlim(min(x) - 0.5, max(x) + 0.5)
# plt.ylim(min(y) - 0.5, max(y) + 0.5)

# #Etiquetas a los ejes
# plt.xlabel("Coeficiente 2")
# plt.ylabel("Coeficiente 3")

# plt.show()