import os
import subprocess
import shutil
import tempfile

glbfile = 'F:\\Desktop\\New folder\\x.glb'

glbFileName = os.path.basename(glbfile)

tempdirectory = tempfile.TemporaryDirectory()

tempdir = tempdirectory.name

tempGlbFile = os.path.join(tempdir, glbFileName)

shutil.copyfile(glbfile, tempGlbFile)

subprocess.run('glb-unpack ' + tempGlbFile, shell = True)

ext = ('.png', '.jpg')

for file in os.listdir(tempdirectory.name):
    tempImgFile = os.path.join(tempdir, file)
    if file.endswith(ext):
        subprocess.run('magick convert ' + tempImgFile + ' -strip ' + tempImgFile, shell = True)
        tmpKtxFile = os.path.splitext(tempImgFile)[0] + '.ktx'
        subprocess.run('toktx --t2 ' + tmpKtxFile + ' ' + tempImgFile)
        
os.remove(tempGlbFile)

gltffile = os.path.splitext(tempGlbFile)[0] + '.gltf'

subprocess.run('glb-pack ' + gltffile, shell = True)

tempGlbFileDraco = os.path.splitext(tempGlbFile)[0] + '_w_KTX_Draco.glb'

print(tempGlbFileDraco)

subprocess.run('gltf-transform draco ' + tempGlbFile + ' ' + tempGlbFileDraco, shell = True)

shutil.copyfile(tempGlbFileDraco, glbfile)

input('Press any key...')
