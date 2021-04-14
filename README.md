# Extracting Resources from HACKERS.EXE

Someone recently posted a link to the internet archive to the HACKERS movie multimedia/game HACKERS.EXE. This was made available to both Windows and Macs (which you can download here: https://web.archive.org/web/19970501051247/http://www.hollywood.com/movies/hackers/director/index.html)

The A E S T H E T I C of this multimedia game made me want to extract the resources from this file. Taking a look at the strings in the file we can see some strings
whichs leads us to believe it was made with Macromedia Director 4.0. Just to double check we use Rezilla on the mac to also take a look at `vers` resource and see
references to MacroMin Player 3.1.3. Eitherway we know this was likely made with Macromedia Director.

In a land at the beginning of the internet macromeda was a way to easily make cross platform multimedia that runs on both macs and windows machines.

Now that we know what the multimedia experience is made of how do we extract the resources contained within. Unfortunately this program is too old to use the current
macromedia extractions tools for windows, mac or linux. So we'll have to do it the hard way.

The first thing to try and do is find the macromind file. This is a 'RIFF' file. Using a HEX editor you can search for `RIFF`. In HACKERS.EXE this shows up 3 times.
The first two times it is obviously strings (RIFF is required to be followed by the size, but the first two instances is looks like its null terminated followed by
another null terminated string):

```
52 49 46 46 00 57 41 56 45 00 RIFF.WAVE.
```

```
52 49 46 46 00 52 4D 4D 50 00 RIFF.RMMP.
```

These are obviously not RIFF format. So lets look at the third RIFF:

```
0005b9f2: 5249 4646 56b0 1b00 RIFFV...
```

Now this is more like it. If we look backwards a little (23 bytes) from this offset we can see:`0c48 434b 5253 5043 372e 4d4d 4d .HCKRSPC7.MMM` followed
by: `0943 3a5c 4e41 4e43 595c .C:\NANCY\`. The first byte is the length of the string, followed by that string. So now we have a file name: `HCKRSPC7.MMM` and
where this file was stored in Windows: `C:\NANCY\`. Thanks Nancy!

Keep in mind mere mortals aren't supposed to be reading these files. You likely wont be able to extract all the data but at least you can get some of it out of here.

The RIFF format isn't very complicated and goes `RIFF` followed the size of the data chunk (little endian). Looking at the data its easy to see that this is an
RMMP format file and the size is to the end of the file. At this point we can extract the MMM file from the exe using `dd`: `dd skip=375282 if=HACKERS.EXE of=HCKRSPC7.MMM iflag=skip_bytes,count_bytes`

So at this point we have an MMM file, unfortunately there's really no way to open such a file. Luckily the folks over at the archiveteam have written a rudimentary tool to extract resources from RMMP
files: http://fileformats.archiveteam.org/wiki/User:Effect2/readRMPP.c Download this file and compile it: `cc -o readrmpp readrmpp.c` and then run
it: `./readrmpp df HCKRSPC7.MMM`

This will dump all the files in the RMMP file

```
 1001570.DIB   1247068.DIB     1751452.VWFI   1799064.VWCI   1804716.VWCI   1813200.VWCI   523528.DIB   772022.DIB
 1003288.DIB   1249842.DIB     1751570.VWLB   1799126.VWCI   1804838.VWCI   1813294.VWCI   523648.DIB   776276.DIB
 1003666.DIB   1249912.DIB     1752366.VWAC   1799198.VWCI   1804936.VWCI   1813364.VWCI   524614.DIB   780070.DIB
 1003876.DIB  '1249982.STR '   175618.DIB     1799262.VWCI   1805028.VWCI   1813434.VWCI   534084.DIB   783544.DIB
 1017294.DIB   1250016.vers    1756302.VWSC   1799330.VWCI   1805126.VWCI   1813504.VWCI   543554.DIB   787358.DIB
 1029998.DIB   1250106.vers    176456.DIB     1799394.VWCI   1805194.VWCI   1813576.VWCI   553024.DIB   791548.DIB
 1034012.DIB   1250154.WDEF    176798.DIB     1799458.VWCI   1805714.VWCI   1814114.VWCI   562494.DIB   796568.DIB
 1042498.DIB   1250246.XCOD    1795456.VWCI   1799522.VWCI   1806114.VWCI   1814522.VWCI   571964.DIB   801484.DIB
 1044676.DIB  '1268788.snd '   1795522.VWCI   1799586.VWCI   1806638.VWCI   186576.DIB     57782.DIB    805666.DIB
 1046854.DIB  '1299712.snd '   1795614.VWCI   1799650.VWCI   1807040.VWCI   188054.DIB     581434.DIB   810114.DIB
 1047196.DIB   12.CFTC         1795698.VWCI   1799714.VWCI   1807132.VWCI   197568.DIB     590948.DIB   814824.DIB
 1049530.DIB   137204.DIB      1795764.VWCI   1799780.VWCI   1807222.VWCI   207082.DIB     59258.DIB    819454.DIB
 1050956.DIB   137398.DIB      1795840.VWCI   1799846.VWCI   1807344.VWCI   216596.DIB     600462.DIB   824500.DIB
 1051226.DIB   137592.DIB      1795960.VWCI   1799912.VWCI   1807418.VWCI   226110.DIB     609976.DIB   829052.DIB
 1052282.DIB   137794.DIB      1796028.VWCI   1799990.VWCI   1807494.VWCI   22764.DIB      610302.DIB   833474.DIB
 1052768.DIB   137988.DIB      1796096.VWCI   1800076.VWCI   1807566.VWCI   228540.DIB     610532.DIB   838130.DIB
 1053008.DIB   138322.DIB      1796162.VWCI   1800148.VWCI   1807634.VWCI   230552.DIB     610858.DIB   842288.DIB
 1054256.DIB   138524.DIB      1796230.VWCI   1800218.VWCI   1807710.VWCI   232742.DIB     610930.DIB   846060.DIB
 1058278.DIB  '1388026.snd '   1796326.VWCI   1800288.VWCI   1807784.VWCI   236852.DIB     620400.DIB   846130.DIB
 1058334.DIB   139610.DIB      1796392.VWCI   1800358.VWCI   1807854.VWCI   252194.DIB     629870.DIB   846200.DIB
 1062356.DIB   14046.DIB       1796458.VWCI   1800428.VWCI   1807960.VWCI   260956.DIB     639340.DIB   846674.DIB
 1064698.DIB  '1430104.snd '   1796524.VWCI   1800498.VWCI   1808036.VWCI   270470.DIB     648810.DIB   847048.DIB
 1067144.DIB   144172.DIB      1796590.VWCI   1800568.VWCI   1808106.VWCI   284620.DIB     658280.DIB   847444.DIB
 1069170.DIB   144402.DIB      1796710.VWCI   1800638.VWCI   1808176.VWCI   293970.DIB     667750.DIB   847740.DIB
 1071200.DIB  '1458828.snd '   1796778.VWCI   1800708.VWCI   1808304.VWCI   303484.DIB     677220.DIB   847810.DIB
 1073230.DIB   147732.DIB      1796850.VWCI   1800778.VWCI   1808376.VWCI   312998.DIB     686690.DIB   847880.DIB
 1075488.DIB  '1501334.snd '   1796918.VWCI   1800846.VWCI   1808464.VWCI   322512.DIB     696160.DIB   847950.DIB
 1075974.DIB  '1547736.snd '   1797012.VWCI   1800908.VWCI   1808538.VWCI   332026.DIB     7016.Ver.    848020.DIB
 1076812.DIB   15510.DIB       1797082.VWCI   1800978.VWCI   1810550.VWCI   341540.DIB     7030.McNm    848250.DIB
 1101442.DIB  '1572312.snd '   1797174.VWCI   1801040.VWCI   1810884.VWCI   351054.DIB     705630.DIB   848524.DIB
 110430.DIB   '1593418.snd '   1797246.VWCI   1801102.VWCI   1811140.VWCI   360568.DIB     7092.VWCF    848594.DIB
 1126072.DIB  '1602076.snd '   1797320.VWCI   1801168.VWCI   1811414.VWCI   370082.DIB     709518.DIB   848664.DIB
 113918.DIB    160638.DIB      1797392.VWCI   1801238.VWCI   1811512.VWCI   37338.DIB      709844.DIB   848734.DIB
 1150702.DIB   160912.DIB      1797464.VWCI   1801298.VWCI   1811594.VWCI   379596.DIB     713732.DIB   848804.DIB
 1175332.DIB   161164.DIB      1797536.VWCI   1801404.VWCI   1811656.VWCI   389110.DIB     7154.VWCR    848966.DIB
 1175638.DIB   161218.DIB      1797608.VWCI   1801508.VWCI   1811714.VWCI   421772.DIB     717194.DIB   849196.DIB
 1177340.DIB  '1640162.snd '   1797680.VWCI   1801610.VWCI   1811772.VWCI   431198.DIB     721082.DIB   870610.DIB
 1183574.DIB   165400.DIB      1797758.VWCI   1801714.VWCI   1811830.VWCI   440624.DIB     725822.DIB   889746.DIB
 1197092.DIB   1703866.STXT    1797840.VWCI   1801822.VWCI   1811888.VWCI   45296.DIB      726052.DIB   90316.DIB
 1197344.DIB   1704004.STXT    1797916.VWCI   1801924.VWCI   1811946.VWCI   456066.DIB     730366.DIB   906320.DIB
 1201358.DIB   1707912.STXT    1797998.VWCI   1802028.VWCI   1812004.VWCI   456186.DIB     735532.DIB   927314.DIB
 1201632.DIB   1724284.STXT    1798068.VWCI   1802124.VWCI   1812072.VWCI   456394.DIB     739546.DIB   948308.DIB
 1205790.DIB   1724882.STXT    1798138.VWCI   1802248.VWCI   1812404.VWCI   456536.DIB     743158.DIB   969302.DIB
 1209996.DIB   1725348.STXT    1798208.VWCI   1802316.VWCI   1812478.VWCI   456656.DIB     746430.DIB   982364.DIB
 1214562.DIB   1725970.STXT    1798298.VWCI   1802382.VWCI   1812542.VWCI   456930.DIB     750444.DIB
 1219128.DIB   1730004.STXT    1798390.VWCI   1802450.VWCI   1812638.VWCI   466444.DIB     75422.DIB
 1222470.DIB   1730538.STXT    1798482.VWCI   1802520.VWCI   1812706.VWCI   475958.DIB     754458.DIB
 1226604.DIB   1736774.STXT    1798574.VWCI   1802616.VWCI   1812764.VWCI   485472.DIB     754710.DIB
 1231520.DIB   1736824.STXT    1798644.VWCI   1802708.VWCI   1812824.VWCI   48892.DIB      754940.DIB
 1235408.DIB   1736874.STXT    1798714.VWCI   1803232.VWCI   1812884.VWCI   494986.DIB     758954.DIB
 1239722.DIB   1737580.STXT    1798784.VWCI   1803634.VWCI   1812944.VWCI   504500.DIB     762968.DIB
 1240416.DIB   1737632.STXT    1798854.VWCI   1804164.VWCI   1813008.VWCI   514014.DIB     763220.DIB
 1244952.DIB   1738070.STXT    1798924.VWCI   1804568.VWCI   1813072.VWCI   51466.DIB      763472.DIB
 1245654.DIB   1751416.VWFM    1798994.VWCI   1804642.VWCI   1813136.VWCI   52220.DIB      767504.DIB
```

This is hard to work with though. It removes information. Lets take a look at RMMP format:

* 4 bytes: Chunk ID (e.g. 'DIB ', 'snd ', VWCF, etc)
* 4 bytes: The size of this chunk
* 4 bytes: ID (some documents call this a sequence)

Then the data.

The interesting thing here is the 'ID' field. If you look at the MMM file in a RIFF viewer you'll notice that DIB and VWCI files have the same sequence number!

VWCI appears to be Video Works Cast Information 'files'. If byte 15 is set to 0x00 then this is a file name (otherwise it appears to be instructions/commands). The
filename length can be found at offset 44 (after the RIFF chunkid and size) with the filename itself imediately following it with N bytes. Of note, however, is that not all files have a corresponding VWCI entry. Why? Who knows.

Ok, let's look at offset 0x001b6580:

```
001b6580  56 57 43 49 3a 00 00 00  02 04 00 00 00 63 00 00  |VWCI:........c..|
001b6590  00 10 00 00 00 00 00 00  00 00 00 00 00 00 00 05  |................|
001b65a0  00 00 00 00 00 00 00 00  00 00 00 0a 00 00 00 0a  |................|
001b65b0  00 00 00 0a 00 00 00 0a  09 68 61 6b 20 74 69 74  |.........hak tit|
001b65c0  6c 65                                             |le|
001b65c2
```

* Chunk ID: `VWCI`
* Size: 58
* ID number: 1026
* Filename (0 for yes): 0
* Filename length: 9
* Filename: hak title

Now all we need to do is find the corresponding DIB file with the same sequence. At offset 0x36DE we have the following:

```
000036de  44 49 42 20 b0 05 00 00  02 04 00 00 00 9a 28 00  |DIB ..........(.|
000036ee  00 00 24 00 00 00 eb 00  00 00 01 00 01 00 00 00  |..$.............|
000036fe  00 00 82 05 00 00 14 0a  00 00 8f 07 00 00 00 00  |................|
0000370e  00 00 00 00 00 00                                 |......|
```

* Chunk ID: `DIB `
* Size: 1456
* ID number: 1026

Followed by 0x009A, this is a mystery to me. Afterwards we have the DIB file.

## DIB files

DIB files are essentially BMP files without the BMP header. They break down as header, pallet, bitmap data.

Using the DIB file 1026 hak title (above) here's the BITMAPINFOHEADER:

* Header Size (4 bytes) - 40
* Width (4 bytes) -  36
* Height (4 bytes) - 235
* Color Planes (2 bytes): 1
* Depth (2 bytes) -  1
* Compression: 0
* Size: 1410
* X pixels (4 bytes) - 2580
* Y Pixels (4 bytes) - 1935
* Pallet (4 bytes) - 0
* Important (4 bytes) -  0

Followed by pallet information then the bitmap itself. Unfortunately most programs won't load these DIB files but a few lines of python will convert the majority of them:

```python
#!/usr/bin/env

import sys
from PIL import Image
ImageFile.LOAD_TRUNCATED_IMAGES = True

with open(sys.argv[1], 'rb') as f:
    dib = f.read()

try:
    Image.open(sys.argv[1]).save(sys.argv[1]+".bmp")
except:
    print("FAILED:", sys.argv[1])
```

At this point this is the best we can do for these images. Some of them will be negatives, some are skewed, etc.

## SND files

The SND files are a little simpler.

```
00135c34  73 6e 64 20 c4 78 00 00  5e 04 00 00 04 6c 6f 6f 70 |snd .x..^....loop|
```

* Chunk ID: `snd `
* Size: 30,916
* ID: 1118
* Filename Size: 4
* Filename: loop

Following the filename is a mono PCM file with a sample rate of 11,025 Hz. Converting the SND files to a wav file is also very easy with Python:

```python
#!/usr/bin/env
import sys
import wave
with open(sys.argv[1], 'rb') as f:
    snd = f.read
txt_len = snd[0]
filename = snd[1:1+txt_len]
pcm = snd[1 + txt_len:]
with wave.open(filename+'.wav', 'wb') as wavfile:
    wavfile.setparams((1, 1, 11025, 0, 'NONE', 'NONE'))
    wavfile.writeframes(pcm)
```

## Table of Contents

Within the RMMP is a table of contents. This is a list of all the files in this RIFF, their size, ID, and offset from the top of the file.

* Name (4 bytes)
* Size (4 ybtes)
* ID (4 bytes)
* Offset (4 bytes)

This is here just for informational purposes, these were likely there to save on ram back in the day since you didn't really want to try and load a 4mb
RMMP file in to your 1mb of ram in Windows 3.11.

To parse this section out is easy enough:

```python
for i in range(0, len(rmmp), 16):
        ctfc = rmmp[i:i+16]
        name = ctfc[0:4].decode('utf-8')
        size = int.from_bytes(ctfc[4:8], 'little')
        seq = int.from_bytes(ctfc[8:12], 'little')
        offset = int.from_bytes(ctfc[12:16], 'little')
```

## STXT

I'm going to assume the S stands for Script, and the txt stands for text. These sections are made up of a 15 byte header, then the text, followed by a footer
with between 22-25 bytes of data. Converting these to text files is also fairly straight forward:

```python
#!/usr/bin/env
import sys

with open(sys.argv[1], 'rb') as f:
    stxt = f.read

    x = -30
    while stxt[x] < 128 and stxt[x] > 0:
        x += 1

    text = STXT[i][14:x].replace(b'\r', b'\n')

    with open(fname+".txt", 'wb') as f:
        f.write(text)
```

Putting the above together we can dump and convert most of the resources in this RMMP file:

```python
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
```


## Vers

These contain version information. They appear to have a header then text.

```
0013133a  76 65 72 73 28 00 00 00  02 00 00 00 00 56 04 00  |vers(........V..|
0013134a  80 00 00 00 03 34 2e 30  17 4d 61 63 72 6f 6d 65  |.....4.0.Macrome|
0013135a  64 69 61 20 44 69 72 65  63 74 6f 72 20 34 2e 30  |dia Director 4.0|
0013136a  57 44 45 46 54 00 00 00  64 2f 00 00 0e 52 65 61  |WDEFT...d/...Rea|
0013137a  72 57 69 6e 64 6f 77 57  44 45 46 00 60 0e 00 00  |rWindowWDEF.`...|
0013138a  57 44 45 46 2f 64 00 00                           |WDEF/d..|
00131392
```

```
0013133a  76 65 72 73 28 00 00 00  02 00 00 00 00 56 04 00  |vers(........V..|
0013134a  80 00 00 00 03 34 2e 30  17 4d 61 63 72 6f 6d 65  |.....4.0.Macrome|
0013135a  64 69 61 20 44 69 72 65  63 74 6f 72 20 34 2e 30  |dia Director 4.0|
0013136a
```

# STR

This only shows up once but appears to be a string

```
001312be  53 54 52 20 1a 00 00 00  f4 bf ff ff 00 00 13 4d  |STR ...........M|
001312ce  61 63 72 6f 6d 65 64 69  61 20 44 69 72 65 63 74  |acromedia Direct|
001312de  6f 72                                             |or|
```

# Font

The resource VWFM looks to contain the name of the fonts to use.

```
001ab978  56 57 46 4d 1b 00 00 00  00 04 00 00 00 63 00 02  |VWFM.........c..|
001ab988  00 03 00 00 06 47 65 6e  65 76 61 07 43 68 69 63  |.....Geneva.Chic|
001ab998  61 67 6f                                          |ago|
001ab99b
```

## The Rest

The remaining resources I can't figure out what they'd be for. Here's some educated guesses:

| Resource | Potential Use                |
|----------|------------------------------|
| VWCF     | Cast Files?                  |
| VWCR     | Cast Resources?              |
| WDEF     | External resource definition |
| XCOD     | External code (macro)        |
| VWFI     | Font Info?                   |
| VWLB     | No Idea                      |
| VWAC     | No Idea                      |
| VWSC     | No Idea                      |

# Files

## Images

The DIB files (and converted to BMP) are located in `Images/DIB` but I wasn't happy with trying to extract the resources from these files so I just played the game and took screenshots stored in `Images/Screenshots`

## Sounds

The sounds, as extracted from the MMM file are stored in `Sounds`

## Text

Text files are stored in `Text`