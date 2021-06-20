import os

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

def rotar(lectura, h, color, file):
    global header
    global matriz
    block = list()
    for i in lectura:
        block.append(bytes([i]))

    for x in color:
        f = h
        j = 0
        for i in block[x::3]:
            if f == 0:
                j += 1
                f = h
            matriz[f-1][j][x] = i
            f -= 1
    # for i in matriz:
    #     b = b''
    #     for j in i:
    #         b += b''.join(j)
    #     os.write(file, b)

def write(file):
    global matriz
    for i in matriz:
        b = b''
        for j in i:
            b += b''.join(j)
        os.write(file, b)

if __name__=='__main__':
    fd = os.open('tux.ppm', os.O_RDWR)
    header = new_header(header(fd))
    new = os.open('left_tux.ppm', os.O_RDWR | os.O_CREAT)
    os.write(new, header[0])
    os.lseek(fd, len(header[0]), 0)
    leer = 196624-len(header[0])
    leer = leer - (leer % 3)
    block = os.read(fd, leer)
    matriz = [[[0,0,0] for i in range(header[1])]for i in range(header[2])]
    color = [0, 1, 2]
    rotar(block, header[2], color, new)
    write(new)
    