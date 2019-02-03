import struct
import numpy as np

def getSome(want, buff, offset):
  fmt = "<" + want
  newoffset = offset + struct.calcsize(fmt)
  return struct.unpack_from(fmt, buff, offset)[0], newoffset

def decodeStatusAnswer(data):

  state = {}
  
  ok, offset = getSome("I", data, 0)
  #print("ok: {}".format(ok))

  freezeMode, offset = getSome("B", data, offset)
  #print("freezeMode: {}".format(freezeMode))

  remotes, offset = getSome("B", data, offset)
  #print("remotes: {}".format(remotes))

  poolDelay, offset = getSome("B", data, offset)
  #print("poolDelay: {}".format(poolDelay))

  spaDelay, offset = getSome("B", data, offset)
  #print("spaDelay: {}".format(spaDelay))

  cleanerDelay, offset = getSome("B", data, offset)
  #print("cleanerDelay: {}".format(cleanerDelay))

  # fast forward 3 bytes. why? because.
  #offset = offset + struct.calcsize("3B")
  ff1, offset = getSome("B", data, offset)
  #print("fastForward1: {}".format(ff1))
  ff2, offset = getSome("B", data, offset)
  #print("fastForward2: {}".format(ff2))
  ff3, offset = getSome("B", data, offset)
  #print("fastForward3: {}".format(ff3))

  airTemp, offset = getSome("i", data, offset)
  #print("airTemp: {}".format(airTemp))
  state['airTemp'] = airTemp

  bodiesCount, offset = getSome("I", data, offset)
  bodiesCount = min(bodiesCount, 2)
  #print("bodiesCount: {}".format(bodiesCount))
  
  currentTemp  = np.zeros(bodiesCount+1, dtype=int)
  heatStatus   = np.zeros(bodiesCount+1, dtype=int)
  heatSetPoint = np.zeros(bodiesCount+1, dtype=int)
  coolSetPoint = np.zeros(bodiesCount+1, dtype=int)
  heatMode     = np.zeros(bodiesCount+1, dtype=int)

  state['bodies'] = {}
  state['bodies']['names'] = {}
  state['bodies']['data'] = [{} for x in range(bodiesCount)]

  for i in range(bodiesCount):
    bodyType, offset = getSome("I", data, offset)
    if(bodyType not in range(2)): bodyType = 0

    currentTemp[bodyType], offset = getSome("i", data, offset)
    #print("  currentTemp[{}]: {}".format(bodyType, currentTemp[bodyType]))
    state['bodies']['data'][i]['currentTemp'] = currentTemp

    heatStatus[bodyType], offset = getSome("i", data, offset)
    #print("  heatStatus[{}]: {}".format(bodyType, heatStatus[bodyType]))
    state['bodies']['data'][i]['heatStatus'] = heatStatus

    heatSetPoint[bodyType], offset = getSome("i", data, offset)
    #print("  setPoint[{}]: {}".format(bodyType, heatSetPoint[bodyType]))
    state['bodies']['data'][i]['heatSetPoint'] = heatSetPoint

    coolSetPoint[bodyType], offset = getSome("i", data, offset)
    #print("  coolSetPoint[{}]: {}".format(bodyType, coolSetPoint[bodyType]))
    state['bodies']['data'][i]['coolSetPoint'] = coolSetPoint

    heatMode[bodyType], offset = getSome("i", data, offset)
    #print("  heatMode[{}]: {}".format(bodyType, heatMode[bodyType]))
    state['bodies']['data'][i]['heatMode'] = heatMode
    #print("")
  
  circuitCount, offset = getSome("I", data, offset)
  #print("circuitCount: {}".format(circuitCount))
  #print()
  circuitName = ["" for x in range(circuitCount)]

  circuitID  = np.zeros(circuitCount, dtype=int)
  circuitState  = np.zeros(circuitCount, dtype=int)
  circuitColorSet  = np.zeros(circuitCount, dtype=int)
  circuitColorPos  = np.zeros(circuitCount, dtype=int)
  circuitColorStagger  = np.zeros(circuitCount, dtype=int)
  circuitDelay  = np.zeros(circuitCount, dtype=int)

  state['circuits'] = {}
  state['circuits']['states'] = {}
  state['circuits']['data'] = [{} for x in range(circuitCount)]

  for i in range(circuitCount):
    circuitID[i], offset = getSome("I", data, offset)
    #print("  circuitID: {}".format(circuitID[i]))
    state['circuits']['data'][i]['id'] = circuitID[i]

    circuitState[i], offset = getSome("I", data, offset)
    #print("  circuitState: {}".format(circuitState[i]))
    state['circuits']['data'][i]['state'] = circuitState[i]

    state['circuits']['states']['%s' % circuitID[i]] = circuitState[i]
    
    circuitColorSet[i], offset = getSome("B", data, offset)
    #print("  circuitColorSet: {}".format(circuitColorSet[i]))

    circuitColorPos[i], offset = getSome("B", data, offset)
    #print("  circuitColorPos: {}".format(circuitColorPos[i]))

    circuitColorStagger[i], offset = getSome("B", data, offset)
    #print("  circuitColorStagger: {}".format(circuitColorStagger[i]))

    circuitDelay[i], offset = getSome("B", data, offset)
    #print("  circuitDelay: {}".format(circuitDelay[i]))
    #print()

  state['chemistry'] = {}
  pH, offset = getSome("i", data, offset)
  #print("pH: {}".format(pH / 100))
  state['chemistry']['pH'] = (pH / 100)
  
  orp, offset = getSome("i", data, offset)
  #print("orp: {}".format(orp))
  state['chemistry']['orp'] = orp

  saturation, offset = getSome("i", data, offset)
  #print("saturation: {}".format(saturation / 100))
  state['chemistry']['saturation'] = (saturation / 100)

  saltPPM, offset = getSome("i", data, offset)
  #print("saltPPM: {}".format(saltPPM))
  state['chemistry']['saltPPM'] = saltPPM

  pHTank, offset = getSome("i", data, offset)
  #print("pHTank: {}".format(pHTank))
  state['chemistry']['pHTankLevel'] = pHTank

  orpTank, offset = getSome("i", data, offset)
  #print("orpTank: {}".format(orpTank))
  state['chemistry']['orpTankLevel'] = orpTank

  alarms, offset = getSome("i", data, offset)
  #print("alarms: {}".format(alarms))
  state['chemistry']['alarms'] = alarms

  return state
