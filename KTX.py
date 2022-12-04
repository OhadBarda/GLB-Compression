from pathlib import Path
import subprocess
import tempfile
import shutil
import shlex
import PIL
from PIL import Image
import os

# KTX compression type for Normal maps (uastc/etc1s)
ktxCompNormal = 'etc1s'
# KTX compression type for other maps(uastc/etc1s)
ktxComp = 'etc1s'

ktxCompNormalInfo = ''
if 'uastc' in ktxCompNormal:
    ktxCompNormal = '--uastc 2 --zcmp 3'
    ktxCompNormalInfo = 'nrmUASTC'
if 'etc1s' in ktxCompNormal:
    ktxCompNormal = '--bcmp'
    ktxCompNormalInfo = 'nrmETC1S'

glbFilePath = ''
while os.path.isfile(glbFilePath) == 0:
    glbFilePath = input('\nDrag the GLB file here and press enter: \n')
    glbFilePath = glbFilePath[1:-1]

glbFileName = os.path.basename(glbFilePath)

glbFolderPath = os.path.dirname(glbFilePath)

tempFolderPath = tempfile.mkdtemp(dir = glbFolderPath)

shutil.copy(glbFilePath , tempFolderPath)

GltfFilePath = tempFolderPath + '.gltf'

GltfFileName = os.path.basename(GltfFilePath)

os.chdir(tempFolderPath)

subprocess.run('gltf-transform copy ' + glbFileName + ' ' + GltfFileName , shell = True)

ext = ('.png', '.jpg')

# input('ktx the clean png - Start ')

for file in os.listdir(tempFolderPath):
    if file.endswith(ext):
        print(file + ' ...' , end =" ")
        subprocess.run('magick convert -strip ' + file + ' ' + file , shell = True)
        img = PIL.Image.open(file)
        wid, hgt = img.size
        if wid not in (2048 , 4096):
            print('Extending: ' , file)
            if 1 < wid < 2048:
                delta = str(2048 - wid)
            else:
                delta = str(4096 - wid)
            subprocess.run('magick ' + file + ' -gravity northeast -splice ' + delta + 'x' + delta + ' ' + file , shell = True)
        print('Done')

# input('ktx the clean png - Finished')

subprocess.run('gltf-transform ' + ktxComp + ' ' + GltfFileName + ' ' + glbFileName , shell = True)

input('unpack the glb')

subprocess.run('gltf-transform copy ' + glbFileName + ' ' + GltfFileName, shell = True)

# input('ktx the normal')

keyword = 'normal'
for file in os.listdir(tempFolderPath):
    if file.endswith(ext):
        if keyword in file:
            fileKtx2Name = os.path.splitext(file)[0] + '.ktx2'
            fileKtx2Path = os.path.join(tempFolderPath , fileKtx2Name)
            fileKtx2PathDoublequote = '"{}"'.format(fileKtx2Path)
            filePath = os.path.join(tempFolderPath , file)
            filePathDoublequote = '"{}"'.format(filePath)
            subprocess.run('toktx --t2 ' + ktxCompNormal + ' ' + fileKtx2PathDoublequote + ' ' + filePathDoublequote , shell = True)

# input('Pack back to glb')

subprocess.run('gltf-transform copy ' + GltfFileName + ' ' + glbFileName , shell = True)

# input('use gltf-pipeline to pack the glb to glb')

subprocess.run('gltf-pipeline -i ' + glbFileName + ' -o ' + glbFileName + ' -d --draco.quantizePositionBits 0' , shell = True)

compGlbFileName = Path(glbFilePath).stem + '_' + ktxComp + '_' + ktxCompNormalInfo + '.glb'

compGlbFile = os.path.join(glbFolderPath , compGlbFileName)

shutil.copy(glbFileName , compGlbFile)

os.chdir("..")

shutil.rmtree(tempFolderPath)