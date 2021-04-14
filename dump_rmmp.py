#!/usr/bin/env python3
# Obtain HACKERS.EXE from the internet acrhive
# Dump the MMM: dd skip=375282 if=HACKERS.EXE of=HCKRSPC7.MMM iflag=skip_bytes,count_bytes
# Dump the content: ./dump.py HCKRSPC7.MMM
import sys
from PIL import Image
from hexdump import hexdump
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import wave

VWCI = {}
DIBS = {}
SNDS = {}
STXT = {}
ctfc_data = ''

def read_cftc(rmmp):
    ctfc_array = []
    for i in range(0, len(rmmp), 16):
        ctfc = rmmp[i:i+16]
        name = ctfc[0:4].decode('utf-8')
        size = int.from_bytes(ctfc[4:8], 'little')
        seq = int.from_bytes(ctfc[8:12], 'little')
        offset = int.from_bytes(ctfc[12:16], 'little')
        ctfc_array.append("Name: {} Size: {} ID: {} Offset: {}".format(name, size, seq, offset))
    return ctfc_array

def Read_rmmp(filename):
    with open(filename, 'rb') as f:
        riff = f.read()

    if 'RMMP' not in riff[8:12].decode('utf-8').upper():
        print('{} not an RMMP file'.format(filename))
        return

    rmmp = riff[12:]

    i = 0
    while i < len(rmmp):
        name = rmmp[i:i + 4].decode('utf-8').upper()
        size = int.from_bytes(rmmp[i+4:i+8], 'little')
        seq = int.from_bytes(rmmp[i+8:i+12], 'little')
        end_of_data = i + size + 8
        if end_of_data % 2 != 0:
            end_of_data += 1
        data = rmmp[i+12:end_of_data]

        if name == 'DIB ':
            print('DIB  Offset: {} Size: {} Seq: {}'.format(i, size, seq))

            DIBS[seq] = data[2:]
        elif name == 'VWCI':
            if data[13] == 0:
                filename_len = data[44]
                filename = data[45:filename_len+45].decode('utf-8')
                print('VWCI Offset: {} Size: {} Seq: {} filename_len: {} filename: {}'.format(i, size, seq, filename_len, filename))
                VWCI[seq] = filename
            else:
                print(data[44:])
        elif name == 'CFTC':
            ctfc_data = '\n'.join(read_cftc(data))

        elif name == 'SND ':
            SNDS[seq] = data

        elif name == 'STXT':
            STXT[seq] = data

        elif name == 'MCNM':
            name_len = data[0]
            print("McNm Name:", data[1:1+name_len].decode())
            other_len = data[1+name_len]
            print("McNm Name:", data[1+name_len:1+other_len].decode())

        i = end_of_data

Read_rmmp(sys.argv[1])
print('\nSounds:')
for i in SNDS:
    if i in VWCI:
        fname = str(i)+"_"+VWCI[i].replace("/","-")+".snd"
    else:
        fname = str(i)+".snd"

    print("snd file: {} size: {}".format(fname, len(SNDS[i])))
    with open(fname, 'wb') as f:
        f.write(SNDS[i])

    txt_len = SNDS[i][0]
    pcm = SNDS[i][1 + txt_len:]
    with wave.open(fname+'.wav', 'wb') as wavfile:
        wavfile.setparams((1, 1, 11025, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcm)

print("\nDIBs:")
for i in DIBS:
    if i in VWCI:
        fname = str(i)+"_"+VWCI[i].replace("/","-")+".dib"
    else:
        fname = str(i)+".dib"

    with open(fname, 'wb') as f:
        f.write(DIBS[i])

    header = DIBS[i][0:40]
    h_size = int.from_bytes(header[0:4], 'little')
    w = int.from_bytes(header[4:8], 'little')
    h = int.from_bytes(header[8:12], 'little')
    color_planes = int.from_bytes(header[12:14], 'little')
    depth = int.from_bytes(header[14:16], 'little')
    compression = int.from_bytes(header[16:20], 'little')
    size = int.from_bytes(header[20:24], 'little')
    hres = int.from_bytes(header[24:28], 'little')
    vres = int.from_bytes(header[28:32], 'little')
    pallet = int.from_bytes(header[32:36], 'little')
    important = int.from_bytes(header[36:40], 'little')
    DIB_num_in_plt = 2 ** depth
    pallet_size = DIB_num_in_plt * 4

    print("name: {} ({}) {}x{} color planes: {} depth: {} compression: {} size: {} {}x{} pallet: {} important: {} data size: {}".format(
        fname, h_size,w,h, color_planes, depth, compression, size, hres, vres, pallet, important, len(DIBS[i])))

    if compression == 0:
        try:
            img = Image.open(fname).save(fname+".bmp")
        except:
            print("Failed to convert {} to BMP".format(fname))
    else:
        print("Compression {} in {} not supported".format(compression, fname))


print("\nSTXT:")
for i in STXT:
    if i in VWCI:
        fname = str(i)+"_"+VWCI[i].replace("/","-")+".stxt"
    else:
        fname = str(i)+".dib"

    with open(fname, 'wb') as f:
        f.write(STXT[i])
    print("{} Size: {}".format(fname, len(STXT[i])))

    x = -30
    while STXT[i][x] < 128 and STXT[i][x] > 0:
        x += 1

    text = STXT[i][14:x].replace(b'\r', b'\n')

    with open(fname+".txt", 'wb') as f:
        f.write(text)

print(ctfc_data)