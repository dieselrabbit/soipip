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
  #print(sLen)
  if sLen % 4 != 0:
      sLen += 4 - sLen % 4
  
  fmt = "<{}{}".format(sLen, "s")
  #print(fmt)
  newoffset = offsetLen + struct.calcsize(fmt)
  return struct.unpack_from(fmt, buff, offsetLen)[0], newoffset

def decodeConfigAnswer(data):

  controlerID, offset = getSome("I", data, 0)
  print("controlerID: {}".format(controlerID))

  minSetPoint, offset = getSome("B", data, offset)
  print("minSetPoint: {}".format(minSetPoint))
  maxSetPoint, offset = getSome("B", data, offset)
  print("maxSetPoint: {}".format(maxSetPoint))
  minSetPoint, offset = getSome("B", data, offset)
  print("minSetPoint: {}".format(minSetPoint))
  maxSetPoint, offset = getSome("B", data, offset)
  print("maxSetPoint: {}".format(maxSetPoint))

  degC, offset = getSome("B", data, offset)
  print("degC: {}".format(degC != 0))
  controllerType, offset = getSome("B", data, offset)
  print("controllerType: {}".format(controllerType))
  hwType, offset = getSome("B", data, offset)
  print("hwType: {}".format(hwType))
  controllerData, offset = getSome("B", data, offset)
  print("controllerData: {}".format(controllerData))
  equipFlags, offset = getSome("i", data, offset)
  print("equipFlags: {}".format(equipFlags))

  #offset = offset + struct.calcsize("2B")
  #sLen, offset = getSome("I", data, offset)
  #print(sLen)
  genCircuitName, offset = getString(data, offset)#"255s", data, offset)#
  print("genCircuitName: {}".format(genCircuitName.decode("utf-8")))

  #offset = offset + struct.calcsize("2B")

  circuitCount , offset = getSome("I", data, offset)
  print("circuitCount : {}".format(circuitCount))

  circuitID = np.zeros(circuitCount+1, dtype=int)
  circuitName = ["" for x in range(circuitCount+1)]
  cNameIndex = np.zeros(circuitCount+1, dtype=int)
  cFunction = np.zeros(circuitCount+1, dtype=int)
  cInterface = np.zeros(circuitCount+1, dtype=int)
  cFlags = np.zeros(circuitCount+1, dtype=int)
  cColorSet = np.zeros(circuitCount+1, dtype=int)
  cColorPos = np.zeros(circuitCount+1, dtype=int)
  cColorStagger = np.zeros(circuitCount+1, dtype=int)
  cDeviceID = np.zeros(circuitCount+1, dtype=int)
  cDefaultRT = np.zeros(circuitCount+1, dtype=int)

  for i in range(circuitCount):
    circuitID[i], offset = getSome("i", data, offset)
    print("  circuitID[{}]: {}".format(i, circuitID[i]))
    circuitName[i], offset = getString(data, offset)#"255s", data, offset)#
    print("  circuitName[{}]: {}".format(i, circuitName[i].decode("utf-8").strip('\0')))
    cNameIndex[i], offset = getSome("B", data, offset)
    print("  cNameIndex[{}]: {}".format(i, cNameIndex[i]))
    cFunction[i], offset = getSome("B", data, offset)
    print("  cFunction[{}]: {}".format(i, cFunction[i]))
    cInterface[i], offset = getSome("B", data, offset)
    print("  cInterface[{}]: {}".format(i, cInterface[i]))
    cFlags[i], offset = getSome("B", data, offset)
    print("  cFlags[{}]: {}".format(i, cFlags[i]))
    cColorSet[i], offset = getSome("B", data, offset)
    print("  cColorSet[{}]: {}".format(i, cColorSet[i]))
    cColorPos[i], offset = getSome("B", data, offset)
    print("  cColorPos[{}]: {}".format(i, cColorPos[i]))
    cColorStagger[i], offset = getSome("B", data, offset)
    print("  cColorStagger[{}]: {}".format(i, cColorStagger[i]))
    cDeviceID[i], offset = getSome("B", data, offset)
    print("  cDeviceID[{}]: {}".format(i, cDeviceID[i]))
    cDefaultRT[i], offset = getSome("H", data, offset)
    print("  cDefaultRT[{}]: {}".format(i, cDefaultRT[i]))
    print()
    offset = offset + struct.calcsize("2B")

  colorCount , offset = getSome("I", data, offset)
  print("colorCount : {}".format(colorCount))

  colorName = ["" for x in range(colorCount)]
  rgbR = np.zeros(circuitCount+1, dtype=int)
  rgbG = np.zeros(circuitCount+1, dtype=int)
  rgbB = np.zeros(circuitCount+1, dtype=int)

  for i in range(colorCount):
    colorName[i], offset = getString(data, offset)#"255s", data, offset)#
    print("  colorName[{}]: {}".format(i, colorName[i].decode("utf-8").strip('\0')))
    rgbR[i], offset = getSome("I", data, offset)
    print("  rgbR[{}]: {}".format(i, rgbR[i]))
    rgbG[i], offset = getSome("I", data, offset)
    print("  rgbG[{}]: {}".format(i, rgbG[i]))
    rgbB[i], offset = getSome("I", data, offset)
    print("  rgbB[{}]: {}".format(i, rgbB[i]))
    print()

  next1 , offset = getSome("I", data, offset)
  print("next1 : {}".format(next1))
  next2 , offset = getSome("I", data, offset)
  print("next2 : {}".format(next2))
  next3 , offset = getSome("I", data, offset)
  print("next3 : {}".format(next3))

  remainder, offset = getSome("I", data, offset)
  print("remainder: {}".format(remainder))
