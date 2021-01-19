import os
import random
import io
import zipfile
import sys
import json

dataPack = 'RandomizedLoot'
dataPackFilename = dataPack + '.zip'
dataPackDescription = 'Loot table randomizer for Minecraft'
inputFiles = []
remainingFiles = []
fileDirectory = {}

for path, directories, files in os.walk('loot_tables'):
  for name in files:
    inputFiles.append(os.path.join(path, name))
    remainingFiles.append(os.path.join(path,name))
    
for file in inputFiles:
  i = random.randint(0, len(remainingFiles) - 1)
  fileDirectory[file] = remainingFiles[i]
  del remainingFiles[i]
  
data = io.BytesIO()
zipData = zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED, False)
i = 0

for newFiles in fileDirectory:
  print(i)
  i = i+1
  with open(newFiles, encoding = "cp850") as file:
    contents = file.read()
  zipData.writestr(os.path.join('data/minecraft/', fileDirectory[newFiles]), contents)

zipData.writestr('pack.mcmeta', json.dumps({'pack':{'pack_format':1, 'description':dataPackDescription}}, indent=4))
zipData.writestr('data/minecraft/tags/functions/load.json', json.dumps({'values':['{}:reset'.format(dataPack)]}))
zipData.writestr('data/{}/functions/reset.mcfunction'.format(dataPack), 'tellraw @a ["",{"text":"8 Foot Gamer Loot Table Randomizer","color":"green"}]')
zipData.close()

with open(dataPackFilename, 'wb') as file:
  file.write(data.getvalue())
  
print('Created datapack "{}"'.format(dataPack))
