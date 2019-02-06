from decodeData import getSome, getString

def decodeStatusAnswer(buff, data):

  #{ name="", state= }
  if('sensors' not in data):
    data['sensors'] = {}
  
  ok, offset = getSome("I", buff, 0)

  freezeMode, offset = getSome("B", buff, offset)

  remotes, offset = getSome("B", buff, offset)

  poolDelay, offset = getSome("B", buff, offset)

  spaDelay, offset = getSome("B", buff, offset)

  cleanerDelay, offset = getSome("B", buff, offset)

  # fast forward 3 bytes. why? because.
  ff1, offset = getSome("B", buff, offset)
  ff2, offset = getSome("B", buff, offset)
  ff3, offset = getSome("B", buff, offset)

  airTemp, offset = getSome("i", buff, offset)
  data['sensors']['airTemp'] = dict(name="Air Temperature", state=airTemp)

  bodiesCount, offset = getSome("I", buff, offset)
  bodiesCount = min(bodiesCount, 2)

  if('bodies' not in data):
    data['bodies'] = [{} for x in range(bodiesCount)]

  for i in range(bodiesCount):
    bodyType, offset = getSome("I", buff, offset)
    if(bodyType not in range(2)): bodyType = 0
    data['bodies'][i]['bodyType'] = dict(name="Type of body of water", state=bodyType)

    currentTemp, offset = getSome("i", buff, offset)
    data['bodies'][i]['currentTemp'] = dict(name="Current Temperature", state=currentTemp)

    heatStatus, offset = getSome("i", buff, offset)
    data['bodies'][i]['heatStatus'] = dict(name="Heater", state=heatStatus)

    heatSetPoint, offset = getSome("i", buff, offset)
    data['bodies'][i]['heatSetPoint'] = dict(name="Heat Set Point", state=heatSetPoint)

    coolSetPoint, offset = getSome("i", buff, offset)
    data['bodies'][i]['coolSetPoint'] = dict(name="Cool Set Point", state=coolSetPoint)

    heatMode, offset = getSome("i", buff, offset)
    data['bodies'][i]['heatMode'] = dict(name="Heater Mode", state=heatMode)
  
  circuitCount, offset = getSome("I", buff, offset)

  if('circuits' not in data):
    data['circuits'] = {}

  for i in range(circuitCount):
    circuitID, offset = getSome("I", buff, offset)

    if(circuitID not in data['circuits']):
      data['circuits'][circuitID] = {}

    if('id' not in data['circuits'][circuitID]):
      data['circuits'][circuitID]['id'] = circuitID

    circuitstate, offset = getSome("I", buff, offset)
    data['circuits'][circuitID]['state'] = circuitstate
 
    circuitColorSet, offset = getSome("B", buff, offset)
    circuitColorPos, offset = getSome("B", buff, offset)
    circuitColorStagger, offset = getSome("B", buff, offset)
    circuitDelay, offset = getSome("B", buff, offset)

  if('chemistry' not in data):
    data['chemistry'] = {}
    
  pH, offset = getSome("i", buff, offset)
  data['chemistry']['pH'] = dict(name="pH", state=(pH / 100))
  
  orp, offset = getSome("i", buff, offset)
  data['chemistry']['orp'] = dict(name="ORP", state=orp)

  saturation, offset = getSome("i", buff, offset)
  data['chemistry']['saturation'] = dict(name="Saturation Index", state=(saturation / 100))

  saltPPM, offset = getSome("i", buff, offset)
  data['chemistry']['saltPPM'] = dict(name="Salt", state=saltPPM)

  pHTank, offset = getSome("i", buff, offset)
  data['chemistry']['pHTankLevel'] = dict(name="pH Tank Level", state=pHTank)

  orpTank, offset = getSome("i", buff, offset)
  data['chemistry']['orpTankLevel'] = dict(name="ORP Tank Level", state=orpTank)

  alarms, offset = getSome("i", buff, offset)
  data['chemistry']['alarms'] = dict(name="Chemistry Alarm", state=alarms)

