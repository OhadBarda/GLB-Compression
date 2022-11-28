from pathlib import Path
import subprocess
import tempfile
import shutil
import msvcrt
import shlex
import os

glbFile = input('\nDrag the GLB file here and press enter: \n')

glbFile = glbFile[1:-1]

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
ktxCompInput = ''
while ktxCompInput not in (yes+no):
    ktxCompInput = input('\nDo you want compressed textures (KTX) ? (Y/N): ')
    if ktxCompInput in yes:
        while ktxCompType not in (uastc , etc1s):
            ktxCompType = input('\nTexture compression type ? \n1 = Low\n2 = High\n')
        if ktxCompType == '1':
            ktxCompType = 'uastc'
        if ktxCompType == '2':
            ktxCompType = 'etc1s'

geoCompInput = ''
geoCompState = ''
while geoCompInput not in (yes+no): 
    geoCompInput = input('\nDo you want compressd geomety (Draco) ? (Y/N): ')
    if geoCompInput in yes:
        geoCompState = '_Draco'

glbFileName = os.path.basename(glbFile)

glbFolderPath = os.path.dirname(glbFile)

tempFolderPath = tempfile.mkdtemp(dir = glbFolderPath)

tempGlbFile = os.path.join(tempFolderPath , glbFileName)

shutil.copy(glbFile , tempFolderPath)

tempGltfFile = os.path.splitext(tempGlbFile)[0] + '.gltf'

tempGltfFileName = os.path.basename(tempGltfFile)

os.chdir(tempFolderPath)

# <------- Restore From Here

if textureLimitInput in yes:
        subprocess.run('gltf-transform resize ' + glbFileName + ' ' + glbFileName + ' --width ' + textureLimitInputWidth + ' --height ' + textureLimitInputHeight , shell = True)


if ktxCompInput in yes:
    subprocess.run('gltf-transform copy ' + glbFileName + ' ' + tempGltfFileName , shell = True)

    ext = ('.png', '.jpg')

    for file in os.listdir(tempFolderPath):
        if file.endswith(ext):
            print(file + ' ...' , end =" ")
            subprocess.run('magick convert -strip ' + file + ' ' + file , shell = True)
            print('Done')
    subprocess.run('gltf-transform ' + ktxCompType + ' ' + tempGltfFileName + ' ' + glbFileName , shell = True)
    print('ktx applied')
    
if geoCompInput in yes:
    subprocess.run('gltf-pipeline -i ' + glbFileName + ' -o ' + glbFileName + ' -d --draco.quantizePositionBits 0' , shell = True)

# -------------> To here

if textureLimitInput in yes:
    txtLimitInfo = '_textureLimitInput' + '_w' + textureLimitInputWidth + '_h' + textureLimitInputHeight
else:
    txtLimitInfo = ''

if yes in (textureLimitInput , ktxCompInput , geoCompInput):
    firstName = txtLimitInfo + '_Ktx(' + ktxCompType + ')' + geoCompState

    compGlbFileName = Path(glbFile).stem + firstName + '.glb'

    compGlbFile = os.path.join(glbFolderPath , compGlbFileName)

    shutil.copy(glbFileName , compGlbFile)

os.chdir("..")

shutil.rmtree(tempFolderPath)
