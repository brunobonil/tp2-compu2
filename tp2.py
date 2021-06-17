#!/usr/bin/python3
import argparse
import os
from posix import O_RDONLY


def new_header(header):
    header = header.split(b'\n')
    if b'#' in header[1]:
        dim = header[2].split(b' ')
        dim[0], dim[1] = dim[1], dim[0]
        width = int(dim[0].decode('utf-8'))
        height = int(dim[1].decode('utf-8'))
        dim = b' '.join(dim)
        header[2] = dim
        header = b'\n'.join(header)
    else:
        dim = header[1].split(b' ')
        dim[0], dim[1] = dim[1], dim[0]
        width = int(dim[0].decode('utf-8'))
        height = int(dim[1].decode('utf-8'))
        dim = b' '.join(dim)
        header[1] = dim
        header = b'\n'.join(header)
    return [header, width, height]


def header(fd):
    leer_header = os.read(fd, 50)
    leer_header = (leer_header.split(b'\n'))
    len_header = 0
    for i in range(len(leer_header)):
        if leer_header[i-1] == b'255':
            break
        len_header += (len(leer_header[i]))
        len_header += 1
    os.lseek(fd, 0, 0)
    header = os.read(fd, len_header)
    return header

def rotar(fd, w, h, name, chunk):
    os.lseek(fd, 0, 0)


    name = 'left_' + name
    file = os.open(name, os.O_CREAT | os.O_RDWR)
    os.write(file, new_header(header(fd))[0])


    lectura = os.read(fd, chunk)
    block = list()
    for i in lectura:
        block.append(bytes([i]))

    j = 0
    f = h
    # dim = [c, f]
    matriz = list()
    matriz = [[[0,0,0] for i in range(w)]for i in range(h)]
    for x in range(3):
        f = h
        j = 0
        for i in block[x::3]:
            if f == 0:
                j += 1
                f = h
            matriz[f-1][j][x] = i
            f -= 1

    # f = h
    # j = 0
    # for i in block[1::3]:
    #     if f == 0:
    #         j += 1
    #         f = dim[1]
    #     matriz[f-1][j][k+1] = i
    #     f -= 1


    # f = h
    # j = 0
    # for i in block[2::3]:
    #     if f == 0:
    #         j += 1
    #         f = dim[1]
    #     matriz[f-1][j][k+2] = i
    #     f -= 1


    
    for i in matriz:
        b = b''
        for j in i:
            b += b''.join(j)
        os.write(file, b)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Procesador de Imagenes')
    parser.add_argument('-f', '--file', help='Archivo que se desea leer', type=str)
    parser.add_argument('-s', '--size', help='Bloque que desea leer', type=int)
    args = parser.parse_args()

    file = 'test.ppm'

    try:
        fd = os.open(file, os.O_RDWR)
    except FileNotFoundError:
        print('ERROR: El archivo no existe')
        exit(1)


    hd = header(fd)
    lista_header = new_header(hd)
    long = len(lista_header[0])


    fd = os.open(file, os.O_RDWR)
    os.lseek(fd, long, 0)
    chunk = 48 - long      #178829 - long
    chunk = chunk - (chunk % 3)
    rotar(fd, lista_header[1], lista_header[2], file, chunk)


    # args.size = args.size - (args.size % 3)
    # if args.size <= 0:
    #     print("El valor size no puede ser negativo o cero")
    #     exit(1)

    # os.lseek(fd, lista_header[0], 0)
    # while True:
    #     lectura = os.read(fd, args.size)

    #     if b'' in lectura and len(lectura) < args.size:
    #         break
    # os.close(fd)

    #print('Se crearon los archivos de manera exitosa')
