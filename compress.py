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

print('finish unpack...\n')

ext = ('.png', '.jpg')

for file in os.listdir(tempdirectory.name):
    tempImgFile = os.path.join(tempdir, file)
    print(tempImgFile)
    if file.endswith(ext):
        subprocess.run('magick convert ' + tempImgFile + ' -strip ' + tempImgFile, shell = True)
        subprocess.run('toktx --t2 ' + tempImgFile + ' ' + tempImgFile)
        
print('Finish removing ICC profile...\n')
print('Finish converting to KTX...\n')

os.remove(tempGlbFile)

gltffile = os.path.splitext(tempGlbFile)[0] + '.gltf'

subprocess.run('glb-pack ' + gltffile, shell = True)

print('Finish update GLB...\n')

input('Press any key...')