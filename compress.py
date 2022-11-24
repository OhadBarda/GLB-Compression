import os
import subprocess
import shutil
import tempfile

glbfile = 'C:\\Dropbox\\Browzwear-Ohad\\Python Compress GLB\\x.glb'

glbFileName = os.path.basename(glbfile)

glbDirName = os.path.dirname(glbfile)

tempdirectory = tempfile.TemporaryDirectory()

tempdir = tempdirectory.name

tempGlbFile = os.path.join(tempdir, glbFileName)

shutil.copyfile(glbfile, tempGlbFile)

tempGltfFileName = os.path.splitext(glbFileName)[0] + '.gltf'

tempGltfFile = os.path.join(tempdir, tempGltfFileName)

subprocess.run('gltf-transform copy ' + tempGlbFile + ' ' + tempGltfFile, shell = True)

ext = ('.png', '.jpg')

for file in os.listdir(tempdirectory.name):
    tempImgFile = os.path.join(tempdir, file)
    if file.endswith(ext):
        subprocess.run('magick convert ' + tempImgFile + ' -strip ' + tempImgFile, shell = True)

os.remove(tempGlbFile)

subprocess.run('gltf-transform copy ' + tempGltfFile + ' ' + tempGlbFile, shell = True)

tempGlbFileCompKTX = os.path.splitext(tempGlbFile)[0] + '(KTX).glb'

subprocess.run('gltf-transform etc1s ' + tempGlbFile + ' ' + tempGlbFileCompKTX , shell = True)

tempGlbFileCompKTX_Draco = os.path.splitext(tempGlbFile)[0] + '(KTX_Draco).glb'

subprocess.run('gltf-transform draco ' + tempGlbFileCompKTX + ' ' + tempGlbFileCompKTX_Draco , shell = True)

shutil.copy(tempGlbFileCompKTX_Draco, glbDirName)

input('Press any key...')
