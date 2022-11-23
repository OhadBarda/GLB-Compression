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

print('Unpack...Done\n')

ext = ('.png', '.jpg')

for file in os.listdir(tempdirectory.name):
    tempImgFile = os.path.join(tempdir, file)
    if file.endswith(ext):
        subprocess.run('magick convert ' + tempImgFile + ' -strip ' + tempImgFile, shell = True)
        tmpKtxFile = os.path.splitext(tempImgFile)[0] + '.ktx'
        subprocess.run('toktx --t2 ' + tmpKtxFile + ' ' + tempImgFile)
        
print('Fix ICC & Convert to KTX ...Done\n')

os.remove(tempGlbFile)

print('Delete temp GLB...Done\n')

gltffile = os.path.splitext(tempGlbFile)[0] + '.gltf'

subprocess.run('glb-pack ' + gltffile, shell = True)

print('Pack to GLB...Done\n')

shutil.copyfile(tempGlbFile, glbfile)

print('Update GLB...Done\n')

input('Press any key...')
