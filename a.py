from pathlib import Path
import subprocess
import tempfile
import shutil
import msvcrt
import shlex
import sys
import os

glbFilePath = ''
while os.path.isfile(glbFilePath) == 0:
    glbFilePath = input('\nDrag the GLB file here and press enter: \n')
    glbFilePath = glbFilePath[1:-1]

yes = ('Y' , 'y')
no = ('N' , 'n')
textureLimitInput = ''
textureLimitInputProp = ''
textureLimitInputWidth = ''
textureLimitInputHeight = ''
while textureLimitInput not in (yes+no):
    textureLimitInput = input('\nDo you want to limit texture resolution? (Y/N): ')
    if textureLimitInput in yes:
        while textureLimitInputProp not in (yes+no): 
            textureLimitInputProp = input('Proportional limit? (Y/N): ')
            if textureLimitInputProp in yes:
                while str.isdigit(textureLimitInputWidth) != True:
                    textureLimitInputWidth = input('Width limit (px): ')
                textureLimitInputHeight = textureLimitInputWidth
            if textureLimitInputProp in no:
                while str.isdigit(textureLimitInputWidth) != True:
                    textureLimitInputWidth = input('Width limit (px): ')
                while str.isdigit(textureLimitInputHeight) != True:
                    textureLimitInputHeight = input('Height limit (px): ')

uastc = '1'
etc1s = '2'
ktxCompType = ''
ktxCompInfo = ''
ktxCompInput = ''
while ktxCompInput not in (yes+no):
    ktxCompInput = input('\nDo you want compressed textures (KTX) ? (Y/N): ')
    if ktxCompInput in yes:
        while ktxCompType not in (uastc , etc1s):
            ktxCompType = input('\nTexture compression type ? \n1 = Low\n2 = High\n')
        if ktxCompType == '1':
            ktxCompType = 'uastc'
            ktxCompInfo = '_Ktx(uastc)'
        if ktxCompType == '2':
            ktxCompType = 'etc1s'
            ktxCompInfo = '_Ktx(etc1s)'

geoCompInput = ''
geoCompInfo = ''
while geoCompInput not in (yes+no): 
    geoCompInput = input('\nDo you want compressd geomety (Draco) ? (Y/N): ')
    if geoCompInput in yes:
        geoCompInfo = '_Draco'

glbFileName = os.path.basename(glbFilePath)

glbFolderPath = os.path.dirname(glbFilePath)

tempFolderPath = tempfile.mkdtemp(dir = glbFolderPath)

shutil.copy(glbFilePath , tempFolderPath)

GltfFilePath = tempFolderPath + '.gltf'

GltfFileName = os.path.basename(GltfFilePath)

os.chdir(tempFolderPath)

# <------- Restore From Here

if textureLimitInput in yes:
    subprocess.run('gltf-transform resize ' + glbFileName + ' ' + glbFileName + ' --width ' + textureLimitInputWidth + ' --height ' + textureLimitInputHeight , shell = True)
    txtLimitInfo = '_MaxRes' + textureLimitInputWidth + 'x' + textureLimitInputHeight
else:
    txtLimitInfo = ''

if ktxCompInput in yes:
    subprocess.run('gltf-transform copy ' + glbFileName + ' ' + GltfFileName , shell = True)

    ext = ('.png', '.jpg')

    for file in os.listdir(tempFolderPath):
        if file.endswith(ext):
            print(file + ' ...' , end =" ")
            subprocess.run('magick convert -strip ' + file + ' ' + file , shell = True)
            print('Done')
    subprocess.run('gltf-transform ' + ktxCompType + ' ' + GltfFileName + ' ' + glbFileName , shell = True)

if geoCompInput in yes:
    subprocess.run('gltf-pipeline -i ' + glbFileName + ' -o ' + glbFileName + ' -d --draco.quantizePositionBits 0' , shell = True)

# -------------> To here

if textureLimitInput in yes or ktxCompInput in yes or geoCompInput in yes:
    exportInfo = txtLimitInfo + ktxCompInfo + geoCompInfo

    compGlbFileName = Path(glbFilePath).stem + exportInfo + '.glb'

    compGlbFile = os.path.join(glbFolderPath , compGlbFileName)

    shutil.copy(glbFileName , compGlbFile)

os.chdir("..")

shutil.rmtree(tempFolderPath)
