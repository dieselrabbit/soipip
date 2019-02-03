import struct
import numpy as np
import binascii
import codecs

def getSome(want, buff, offset):
  fmt = "<" + want
  newoffset = offset + struct.calcsize(fmt)
  return struct.unpack_from(fmt, buff, offset)[0], newoffset

def getString(buff, offset):
  fmtLen = "<I"
  offsetLen = offset + struct.calcsize(fmtLen)
  sLen = struct.unpack_from(fmtLen, buff, offset)[0]
  if sLen % 4 != 0:
      sLen += 4 - sLen % 4
  
  fmt = "<{}{}".format(sLen, "s")
  newoffset = offsetLen + struct.calcsize(fmt)
  return struct.unpack_from(fmt, buff, offsetLen)[0], newoffset

def decodeConfigAnswer(data):

  config = {}
  
  controlerID, offset = getSome("I", data, 0)
  #print("controlerID: {}".format(controlerID))
  config['controlerID'] = controlerID

  minSetPoint1, offset = getSome("B", data, offset)
  #print("minSetPoint1: {}".format(minSetPoint1))
  maxSetPoint1, offset = getSome("B", data, offset)
  #print("maxSetPoint1: {}".format(maxSetPoint1))
  minSetPoint2, offset = getSome("B", data, offset)
  #print("minSetPoint2: {}".format(minSetPoint2))
  maxSetPoint2, offset = getSome("B", data, offset)
  #print("maxSetPoint2: {}".format(maxSetPoint2))

  config['minSetPoint'] = [minSetPoint1, minSetPoint2]
  config['maxSetPoint'] = [maxSetPoint1, maxSetPoint2]

  degC, offset = getSome("B", data, offset)
  #print("degC: {}".format(degC != 0))
  config['degC'] = (degC != 0)
  
  controllerType, offset = getSome("B", data, offset)
  #print("controllerType: {}".format(controllerType))
  hwType, offset = getSome("B", data, offset)
  #print("hwType: {}".format(hwType))
  controllerData, offset = getSome("B", data, offset)
  #print("controllerData: {}".format(controllerData))
  equipFlags, offset = getSome("i", data, offset)
  #print("equipFlags: {}".format(equipFlags))

  paddedGenName, offset = getString(data, offset)
  genCircuitName = paddedGenName.decode("utf-8").strip('\0')
  #print("genCircuitName: {}".format(genCircuitName))
  config['genericCircuitName'] = genCircuitName
         
  circuitCount , offset = getSome("I", data, offset)
  #print("circuitCount : {}".format(circuitCount))
  config['circuitCount'] = circuitCount
         
  circuitID = np.zeros(circuitCount, dtype=int)
  circuitName = ["" for x in range(circuitCount)]
  cNameIndex = np.zeros(circuitCount, dtype=int)
  cFunction = np.zeros(circuitCount, dtype=int)
  cInterface = np.zeros(circuitCount, dtype=int)
  cFlags = np.zeros(circuitCount, dtype=int)
  cColorSet = np.zeros(circuitCount, dtype=int)
  cColorPos = np.zeros(circuitCount, dtype=int)
  cColorStagger = np.zeros(circuitCount, dtype=int)
  cDeviceID = np.zeros(circuitCount, dtype=int)
  cDefaultRT = np.zeros(circuitCount, dtype=int)

  config['circuits'] = {}
  config['circuits']['names'] = {}
  config['circuits']['data'] = [{} for x in range(circuitCount)]
         
  for i in range(circuitCount):
    circuit = {}
    circuitID[i], offset = getSome("i", data, offset)
    #print("  circuitID[{}]: {}".format(i, circuitID[i]))
    config['circuits']['data'][i]['id'] = circuitID[i]
    
    paddedName, offset = getString(data, offset)
    circuitName[i] = paddedName.decode("utf-8").strip('\0')
    #print("  circuitName[{}]: {}".format(i, circuitName[i]))
    config['circuits']['data'][i]['name'] = circuitName[i]

    config['circuits']['names']['%s' % circuitID[i]] = circuitName[i]

    cNameIndex[i], offset = getSome("B", data, offset)
    #print("  cNameIndex[{}]: {}".format(i, cNameIndex[i]))
    cFunction[i], offset = getSome("B", data, offset)
    #print("  cFunction[{}]: {}".format(i, cFunction[i]))
    cInterface[i], offset = getSome("B", data, offset)
    #print("  cInterface[{}]: {}".format(i, cInterface[i]))
    cFlags[i], offset = getSome("B", data, offset)
    #print("  cFlags[{}]: {}".format(i, cFlags[i]))
    cColorSet[i], offset = getSome("B", data, offset)
    #print("  cColorSet[{}]: {}".format(i, cColorSet[i]))
    cColorPos[i], offset = getSome("B", data, offset)
    #print("  cColorPos[{}]: {}".format(i, cColorPos[i]))
    cColorStagger[i], offset = getSome("B", data, offset)
    #print("  cColorStagger[{}]: {}".format(i, cColorStagger[i]))
    cDeviceID[i], offset = getSome("B", data, offset)
    #print("  cDeviceID[{}]: {}".format(i, cDeviceID[i]))
    cDefaultRT[i], offset = getSome("H", data, offset)
    #print("  cDefaultRT[{}]: {}".format(i, cDefaultRT[i]))
    #print()
    offset = offset + struct.calcsize("2B")

  colorCount , offset = getSome("I", data, offset)
  #print("colorCount : {}".format(colorCount))
  config['colorCount'] = colorCount
  
  colorName = ["" for x in range(colorCount)]
  rgbR = np.zeros(circuitCount, dtype=int)
  rgbG = np.zeros(circuitCount, dtype=int)
  rgbB = np.zeros(circuitCount, dtype=int)
  config['colors'] = {} #[{} for x in range(colorCount)]
  
  for i in range(colorCount):
    paddedColorName, offset = getString(data, offset)
    colorName[i] = paddedColorName.decode("utf-8").strip('\0')
    #print("  colorName[{}]: {}".format(i, colorName[i]))
    rgbR[i], offset = getSome("I", data, offset)
    #print("  rgbR[{}]: {}".format(i, rgbR[i]))
    rgbG[i], offset = getSome("I", data, offset)
    #print("  rgbG[{}]: {}".format(i, rgbG[i]))
    rgbB[i], offset = getSome("I", data, offset)
    #print("  rgbB[{}]: {}".format(i, rgbB[i]))
    config['colors']['%s' % colorName[i]] = [ rgbR[i], rgbG[i], rgbB[i]]
    
    #print()

  pump1 , offset = getSome("I", data, offset)
  #print("pump1 : {}".format(pump1))
  pump2 , offset = getSome("I", data, offset)
  #print("pump2 : {}".format(pump2))
  pump3 , offset = getSome("I", data, offset)
  #print("pump3 : {}".format(pump3))
  pump4 , offset = getSome("I", data, offset)
  #print("pump4 : {}".format(pump4))

  return config
