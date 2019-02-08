import struct
from decodeData import getSome, getString

def decodeConfigAnswer(buff, data):

  #{ name="", state= }
  if('config' not in data):
    data['config'] = {}
    
  controlerID, offset = getSome("I", buff, 0)
  data['config']['controlerID'] = dict(name="Controler ID", state=controlerID)

  minSetPoint0, offset = getSome("B", buff, offset)
  maxSetPoint0, offset = getSome("B", buff, offset)
  minSetPoint1, offset = getSome("B", buff, offset)
  maxSetPoint1, offset = getSome("B", buff, offset)

  #if('bodies' not in data):
  #  data['bodies'] = {}
    
  data['config']['minSetPoint'] = dict(name="Minimum Temperature", state=[minSetPoint0, minSetPoint1])
  data['config']['maxSetPoint'] = dict(name="Maximum Temperature", state=[maxSetPoint0, maxSetPoint1])

  degC, offset = getSome("B", buff, offset)
  data['config']['degC'] = dict(name="Is Celcius", state=degC)
  
  controllerType, offset = getSome("B", buff, offset)
  hwType, offset = getSome("B", buff, offset)
  controllerbuff, offset = getSome("B", buff, offset)
  equipFlags, offset = getSome("i", buff, offset)

  paddedGenName, offset = getString(buff, offset)
  genCircuitName = paddedGenName.decode("utf-8").strip('\0')
  data['config']['genCircuitName'] = dict(name="Default Circuit Name", state=genCircuitName)
         
  circuitCount , offset = getSome("I", buff, offset)
  data['config']['circuitCount'] = dict(name="Number of Circuits", state=circuitCount)
         
  if('circuits' not in data):
    data['circuits'] = {}
     
  for i in range(circuitCount):

    circuitID, offset = getSome("i", buff, offset)

    if(circuitID not in data['circuits']):
      data['circuits'][circuitID] = {}
      
    data['circuits'][circuitID]['id'] = circuitID
    
    paddedName, offset = getString(buff, offset)
    circuitName = paddedName.decode("utf-8").strip('\0')
    data['circuits'][circuitID]['name'] = circuitName
    
    cNameIndex, offset = getSome("B", buff, offset)
    cFunction, offset = getSome("B", buff, offset)
    cInterface, offset = getSome("B", buff, offset)
    cFlags, offset = getSome("B", buff, offset)
    cColorSet, offset = getSome("B", buff, offset)
    cColorPos, offset = getSome("B", buff, offset)
    cColorStagger, offset = getSome("B", buff, offset)
    cDeviceID, offset = getSome("B", buff, offset)
    cDefaultRT, offset = getSome("H", buff, offset)
    offset = offset + struct.calcsize("2B")

  colorCount , offset = getSome("I", buff, offset)
  data['config']['colorCount'] = dict(name="Number of Colors", state=colorCount)
  
  if('colors' not in data['config'] or len(data['config']['colors']) != colorCount):
    data['config']['colors'] = [{} for x in range(colorCount)]
  
  for i in range(colorCount):
    paddedColorName, offset = getString(buff, offset)
    colorName = paddedColorName.decode("utf-8").strip('\0')
    rgbR, offset = getSome("I", buff, offset)
    rgbG, offset = getSome("I", buff, offset)
    rgbB, offset = getSome("I", buff, offset)
    data['config']['colors'][i] = dict(name=colorName, state=[ rgbR, rgbG, rgbB])
    
  pumpData1 , offset = getSome("I", buff, offset)
  pumpData2 , offset = getSome("I", buff, offset)
  pumpData3 , offset = getSome("I", buff, offset)
  pumpData4 , offset = getSome("I", buff, offset)
