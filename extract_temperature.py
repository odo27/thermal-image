import subprocess
import json
import io
import re
from PIL import Image
from math import sqrt, exp, log
import numpy as np

# extract raw flir temperature values of cameras in metadata of a jpg file
# deform the data of flir format to a celcius unit
def extract_temperature(filename: str):
    # use exiftool.exe for importing metadata of jpg files
    # subprocess can take cmd's output to python scripts
    # -j tag take them in a json format
    # various tags in a parameter used for defomation to a celcius unit
    meta_json = subprocess.check_output(
        ['exiftool', filename, '-Emissivity', '-SubjectDistance', '-AtmosphericTemperature',
        '-ReflectedApparentTemperature', '-IRWindowTemperature', '-IRWindowTransmission', '-RelativeHumidity',
        '-PlanckR1', '-PlanckB', '-PlanckF', '-PlanckO', '-PlanckR2', '-j'])
    meta = json.loads(meta_json.decode())[0]

    # -RawThermalImage have flir's temperature values
    # reading them with binary format
    thermal_img_bytes = subprocess.check_output(['exiftool', '-RawThermalImage', '-b', filename])
    thermal_img_stream = io.BytesIO(thermal_img_bytes)

    # reading binary files using PIL module and deform to np.array
    thermal_img = Image.open(thermal_img_stream)
    thermal_np = np.array(thermal_img)

    # If metadata has a value of -SubjectDistance tag
    # select important datas using regular expression in module 're'
    subject_distance = 1.0
    if 'SubjectDistance' in meta:
        subject_distance = extract_float(meta['SubjectDistance'])
    
    # deform flir's raw datas to a celcius unit
    fix_endian = True
    if fix_endian:
        thermal_np = np.vectorize(lambda x: (x >> 8) + ((x & 0x00ff) << 8))(thermal_np)
    
    raw2tempfunc = np.vectorize(lambda x: raw2temp(x, E=meta['Emissivity'], OD=subject_distance,
                                                    RTemp=extract_float(meta['ReflectedApparentTemperature']),
                                                    ATemp=extract_float(meta['AtmosphericTemperature']),
                                                    IRWTemp = extract_float(meta['IRWindowTemperature']),
                                                    IRT = meta['IRWindowTransmission'],
                                                    RH = extract_float(meta['RelativeHumidity']),
                                                    PR1 = meta['PlanckR1'],
                                                    PB = meta['PlanckB'],
                                                    PF = meta['PlanckF'],
                                                    PO = meta['PlanckO'],
                                                    PR2 = meta['PlanckR2']))

    
    thermal_np = raw2tempfunc(thermal_np)
    # return np array having values in a celcius unit
    return thermal_np

# It is a function of flir's transformation algorithm
# considering enviroments of taking pictures
def raw2temp(raw, E=1, OD=1, RTemp=20, ATemp=20, IRWTemp=20, IRT=1, RH=50, PR1=21106.77, PB=1501, PF=1, PO=-7340, PR2=0.012545258):
    # constants
    ATA1 = 0.006569
    ATA2 = 0.01262
    ATB1 = -0.002276
    ATB2 = -0.00667
    ATX = 1.9

    # transmission through window (calibrated)
    emiss_wind = 1 - IRT
    refl_wind = 0

    
    # transmission through the air
    h2o = (RH / 100) * exp(1.5587 + 0.06939 * (ATemp) - 0.00027816 * (ATemp) ** 2 + 0.00000068455 * (ATemp) ** 3)
    tau1 = ATX * exp(-sqrt(OD / 2) * (ATA1 + ATB1 * sqrt(h2o))) + (1 - ATX) * exp(-sqrt(OD / 2) * (ATA2 + ATB2 * sqrt(h2o)))
    tau2 = ATX * exp(-sqrt(OD / 2) * (ATA1 + ATB1 * sqrt(h2o))) + (1 - ATX) * exp(-sqrt(OD / 2) * (ATA2 + ATB2 * sqrt(h2o)))


    # radiance from the environment
    raw_refl1 = PR1 / (PR2 * (exp(PB / (RTemp + 273.15)) - PF)) - PO
    raw_refl1_attn = (1 - E) / E * raw_refl1
    raw_atm1 = PR1 / (PR2 * (exp(PB / (ATemp + 273.15)) - PF)) - PO
    raw_atm1_attn = (1 - tau1) / E / tau1 * raw_atm1
    raw_wind = PR1 / (PR2 * (exp(PB / (IRWTemp + 273.15)) - PF)) - PO
    raw_wind_attn = emiss_wind / E / tau1 / IRT * raw_wind
    raw_refl2 = PR1 / (PR2 * (exp(PB / (RTemp + 273.15)) - PF)) - PO
    raw_refl2_attn = refl_wind / E / tau1 / IRT * raw_refl2
    raw_atm2 = PR1 / (PR2 * (exp(PB / (ATemp + 273.15)) - PF)) - PO
    raw_atm2_attn = (1 - tau2) / E / tau1 / IRT / tau2 * raw_atm2
    raw_obj = (raw / E / tau1 / IRT / tau2 - raw_atm1_attn - raw_atm2_attn - raw_wind_attn - raw_refl1_attn - raw_refl2_attn)

    # temperature from radiance
    temp_celcius = PB / log(PR1 / (PR2 * (raw_obj + PO)) + PF) - 273.15
    return temp_celcius

# extract the float value of a string, helpful for parsing the exiftool data
def extract_float(dirtystr):
    digits = re.findall(r"[-+]?\d*\.\d+|\d+", dirtystr)
    return float(digits[0])