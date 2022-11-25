from pathlib import Path
import subprocess
import tempfile
import shutil
import shlex
import os

glbFilePath = input('Please type the path for the GLB file: \n')

glbFilePath = glbFilePath[1:-1]

glbFileName = os.path.basename(glbFilePath)

glbFolderPath = os.path.dirname(glbFilePath)

tempFolderPath = tempfile.mkdtemp(dir = glbFolderPath)

tempglbFilePath = os.path.join(tempFolderPath , glbFileName)

shutil.copy(glbFilePath , tempFolderPath)

tempGltfFile = os.path.splitext(tempglbFilePath)[0] + '.gltf'

gltfFileName = os.path.basename(tempGltfFile)

os.chdir(tempFolderPath)

subprocess.run('gltf-transform copy ' + glbFileName + ' ' + gltfFileName , shell = True)

ext = ('.png', '.jpg')

for file in os.listdir(tempFolderPath):
    if file.endswith(ext):
        print(file + ' ...' , end =" ")
        subprocess.run('magick convert -strip ' + file + ' ' + file , shell = True)
        print('Done')

subprocess.run('gltf-transform etc1s ' + gltfFileName + ' ' + glbFileName , shell = True)

subprocess.run('gltf-pipeline -i ' + glbFileName + ' -o ' + glbFileName + ' -d --draco.quantizePositionBits 0' , shell = True)

glbFileSize = round(os.path.getsize(glbFileName) / 1024 , 2)

print('Compressed file size:' , glbFileSize , 'KB')

compGlbFileName = Path(glbFilePath).stem + '_ktx_draco.glb'

compGlbFile = os.path.join(glbFolderPath , compGlbFileName)

shutil.copy(glbFileName , compGlbFile)

os.chdir("..")

shutil.rmtree(tempFolderPath)