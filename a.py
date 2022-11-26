from pathlib import Path
import subprocess
import tempfile
import shutil
import shlex
import sys
import os

glbFile = input('Please type the path for the GLB file: \n')

glbFile = glbFile[1:-1]

if glbFile == "":
    print('Error: Please try again and drag a GLB file after the prompt.')
    sys.exit()

yes = ('Y' , 'y')
no = ('N' , 'n')
textureLimit = ''
textureLimitProp = ''

while textureLimit not in (yes+no): 
    textureLimit = input('\nDo you want to limit texture resolution? (Y/N): ')
    if textureLimit in yes:
        while textureLimitProp not in (yes+no): 
            textureLimitProp = input('Proportional limit? (Y/N): ')
            if textureLimitProp in yes:
                textureLimitWidth = input('Width limit (px): ')
                textureLimitHeight = textureLimitWidth
            if textureLimitProp in no:
                textureLimitWidth = input('Width limit (px): ')
                textureLimitHeight = input('Height limit (px): ')

glbFileName = os.path.basename(glbFile)

glbFolderPath = os.path.dirname(glbFile)

tempFolderPath = tempfile.mkdtemp(dir = glbFolderPath)

tempglbFile = os.path.join(tempFolderPath , glbFileName)

shutil.copy(glbFile , tempFolderPath)

tempGltfFile = os.path.splitext(tempglbFile)[0] + '.gltf'

gltfFileName = os.path.basename(tempGltfFile)

os.chdir(tempFolderPath)

# <------- Restore From Here

# if textureLimit in yes:
        # subprocess.run('gltf-transform resize ' + glbFileName + ' ' + glbFileName + ' --width ' + textureLimitWidth + ' --height ' + textureLimitHeight , shell = True)

# subprocess.run('gltf-transform copy ' + glbFileName + ' ' + gltfFileName , shell = True)

# ext = ('.png', '.jpg')

# for file in os.listdir(tempFolderPath):
    # if file.endswith(ext):
        # print(file + ' ...' , end =" ")
        # subprocess.run('magick convert -strip ' + file + ' ' + file , shell = True)
        # print('Done')

# subprocess.run('gltf-transform etc1s ' + ' ' + gltfFileName + ' ' + glbFileName , shell = True)

# subprocess.run('gltf-pipeline -i ' + glbFileName + ' -o ' + glbFileName + ' -d --draco.quantizePositionBits 0' , shell = True)

# -------------> To here

if textureLimit in yes:
    txtLimitInfo = '_TextureLimit' + '_w' + textureLimitWidth + '_h' + textureLimitHeight
else:
    txtLimitInfo = ''
    
firstName = txtLimitInfo + '_ktx_draco_1'

compGlbFileName = Path(glbFile).stem + firstName + '.glb'

compGlbFile = os.path.join(glbFolderPath , compGlbFileName)

shutil.copy(glbFileName , compGlbFile)

os.chdir("..")

# <------- Restore From Here
shutil.rmtree(tempFolderPath)
# -------------> To here
