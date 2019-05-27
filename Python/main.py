import json
import paho.mqtt.client as mqtt
from keras.models import load_model
from sklearn.externals import joblib
import requests


def aqiPm25(pm25):
    i = 0
    for x in pm25:
        i+=x
    i = i / len(pm25)
    if i >= 0 and i <= 25:
        aqipm2 = i
    elif i > 25 and i <= 37:
        aqipm2 = ((50-26)/(37-26))*(i-26)+26
    elif i > 37 and i <= 50:
        aqipm2 = ((100-51)/(50-38))*(i-38)+51
    elif i > 50 and i <= 90:
        aqipm2 = ((200-101)/(90-51))*(i-51)+101
    else:
        aqipm2 = 201
    return round(aqipm2,0)

def aqiPm10(pm10):
    i = 0
    for x in pm10:
        i = i+x
    i = i / len(pm10)
    if i >= 0 and i <= 50:
        aqipm10 = ((25)/(50))*(i-0)+0
    elif i > 50 and i <= 80:
        aqipm10 = ((50-26)/(80-51))*(i-51)+26
    elif i > 80 and i <= 120:
        aqipm10 = ((100-51)/(120-81))*(i-81)+51
    elif i > 120 and i <= 180:
        aqipm10 = ((200-101)/(180-121))*(i-121)+101
    else:
        aqipm10 = 201
    return round(aqipm10,0)

def aqiNo2(no2):
    i = 0
    for x in no2:
        i = i+x
    i = i / len(no2)
    if i >= 0 and i <= 60:
        aqino2 = ((25)/(60))*(i-0)+0
    elif i > 60 and i <= 106:
        aqino2 = ((50-26)/(106-61))*(i-61)+26
    elif i > 106 and i <= 170:
        aqino2 = ((100-51)/(170-107))*(i-107)+51
    elif i > 170 and i <= 340:
        aqino2 = ((200-101)/(340-171))*(i-171)+101
    else:
        aqino2 = 201
    return round(aqino2,0)

def aqiSo2(so2):
    i = 0
    for x in so2:
        i = i+x
    i = i / len(so2)
    if i >= 0 and i <= 100:
        aqiso2 = ((25)/(100))*(i-0)+0
    elif i > 100 and i <= 200:
        aqiso2 = ((50-26)/(200-101))*(i-101)+26
    elif i > 200 and i <= 300:
        aqiso2 = ((100-51)/(300-201))*(i-201)+51
    elif i > 300 and i <= 400:
        aqiso2 = ((200-101)/(400-301))*(i-301)+101
    else:
        aqiso2 = 201
    return round(aqiso2,0)

def aqiO3(o3):
    i = 0
    for x in o3:
        i = i+x
    i = i / len(o3)
    if i >= 0 and i <= 35:
        aqio3 = ((25)/(35))*(i-0)+0
    elif i > 35 and i <= 50:
        aqio3 = ((50-26)/(50-36))*(i-36)+26
    elif i > 50 and i <= 70:
        aqio3 = ((100-51)/(70-51))*(i-51)+51
    elif i > 70 and i <= 120:
        aqio3 = ((200-101)/(120-71))*(i-71)+101
    else:
        aqio3 = 201
    return round(aqio3,0)

def aqiCo(co):
    i = 0
    for x in co:
        i = i+x
    i = i / len(co)
    if i >= 0 and i <= 4.4:
        aqico = ((25)/(4.4))*(i-0)+0
    elif i > 4.4 and i <= 6.4:
        aqico = ((50-26)/(6.4-4.5))*(i-4.5)+26
    elif i > 6.4 and i <= 9:
        aqico = ((100-51)/(9-6.5))*(i-6.5)+51
    elif i > 9 and i <= 30:
        aqico = ((200-101)/(30-9.1))*(i-9.1)+101
    else:
        aqico = 201
    return round(aqico,0)  
    
def avg(val):
    i = 0
    for x in val:
        i = i+x
    i = i / len(val)
    return i

def shift(value,data):
    for x in range(len(data)):
        if(x < len(data)-1):
            data[x] = data[x+1]
        else:
            data[len(data)-1] = value
    return data

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("application/Newmsg")

def on_message(client, userdata,msg):
    print('start')
    datas = json.loads(msg.payload.decode("utf-8", "strict"))
    device = datas["deviceName"]
    print(device)

    AQINOW=[]
    temperature=[] 
    humidity=[]
    air=[]
    dustpm25=[] 
    dustpm10=[]
    o3temp=[]
    cotemp=[]
    no2temp=[]
    so2temp=[]
    AQI=[]
    AQINOW=[]
    timeAQI=[]
    timedata=[]

    URLdata = "http://161.246.6.158:1880/datanewest?deviceName="+device
    URLaqi = "http://161.246.6.158:1880/AQInewest?deviceName="+device
    rdata = requests.get(url = URLdata)
    raqi = requests.get(url = URLaqi)
    data = rdata.json()
    aqi = raqi.json()

    for x in range(96-len(data)):
        temperature.append(0) 
        humidity.append(0)
        air.append(0)
        dustpm25.append(0)
        dustpm10.append(0)
        o3temp.append(0)
        cotemp.append(0)
        no2temp.append(0)
        so2temp.append(0)
        timedata.append(0)
    for x in range(len(data)-1,-1,-1):
        temperature.append(data[x]["temperature"]) 
        humidity.append(data[x]["humidity"])
        air.append(data[x]["pressure"])
        dustpm25.append(data[x]["PM25"])
        dustpm10.append(data[x]["PM10"])
        o3temp.append(data[x]["O3"])
        cotemp.append(data[x]["CO"])
        no2temp.append(data[x]["NO2"])
        so2temp.append(data[x]["SO2"])
        timedata.append(data[x]["date"])
    if len(aqi)==0:
        for x in range(7):
            AQI.append(0)
            timeAQI.append(0)
    elif len(aqi) <= 7:
        for x in range(7-len(aqi)):
            AQI.append(0)
            timeAQI.append(0)
        for x in range(len(aqi)-1,-1,-1):
            AQI.append(aqi[x]["AQINOW"])
            timeAQI.append(aqi[x]["time"])
    else:
        for x in range(7):
            AQI.append(aqi[x]["AQINOW"])
            timeAQI.append(aqi[x]["time"])
    AQINOW.append(aqiPm25(dustpm25[len(dustpm25)-96:]))
    AQINOW.append(aqiPm10(dustpm10[len(dustpm10)-96:]))
    AQINOW.append(aqiO3(o3temp[len(o3temp)-32:]))
    AQINOW.append(aqiCo(o3temp[len(o3temp)-32:]))
    AQINOW.append(aqiNo2(no2temp[len(no2temp)-4:]))
    AQINOW.append(aqiSo2(so2temp[len(so2temp)-4:]))
    shift(max(AQINOW),AQI)
    dataForPredict1hr=[]
    for x in range(23): #[avg(dustpm25[x*4:x*4+4]
        dataForPredict1hr.append([avg(dustpm25[(x+1)*4:(x+1)*4+4]),
                                  avg(dustpm10[(x+1)*4:(x+1)*4+4]),
                                  avg(o3temp[(x+1)*4:(x+1)*4+4]),
                                  avg(cotemp[(x+1)*4:(x+1)*4+4]),
                                  avg(no2temp[(x+1)*4:(x+1)*4+4]),
                                  avg(so2temp[(x+1)*4:(x+1)*4+4])])
    result1 = prediction1hr(dataForPredict1hr)
    dataForPredict24hr=[]
    for x in range(24): #[avg(dustpm25[x*4:x*4+4]
        dataForPredict24hr.append([avg(dustpm25[(x)*4:(x)*4+4]),
                                  avg(dustpm10[(x)*4:(x)*4+4]),
                                  avg(o3temp[(x)*4:(x)*4+4]),
                                  avg(cotemp[(x)*4:(x)*4+4]),
                                  avg(no2temp[(x)*4:(x)*4+4]),
                                  avg(so2temp[(x)*4:(x)*4+4])])
    result24 = prediction24hr(dataForPredict24hr)
    try:
        dataaqi = json.dumps({"deviceName":datas["deviceName"],"timenow":datas["date"],
        "temp1":temperature[-7],"temp2":temperature[-6],"temp3":temperature[-5],"temp4":temperature[-4],"temp5":temperature[-3],"temp6":temperature[-2],"tempnow":temperature[-1],
        "air1":air[-7],"air2":air[-6],"air3":air[-5],"air4":air[-4],"air5":air[-3],"air6":air[-2],"airnow":air[-1],
        "hu1":humidity[-7],"hu2":humidity[-6],"hu3":humidity[-5],"hu4":humidity[-4],"hu5":humidity[-3],"hu6":humidity[-2],"hunow":humidity[-1],
        "pm251":dustpm25[-7],"pm252":dustpm25[-6],"pm253":dustpm25[-5],"pm254":dustpm25[-4],"pm255":dustpm25[-3],"pm256":dustpm25[-2],"pm25now":dustpm25[-1],
        "pm101":dustpm10[-7],"pm102":dustpm10[-6],"pm103":dustpm10[-5],"pm104":dustpm10[-4],"pm105":dustpm10[-3],"pm106":dustpm10[-2],"pm10now":dustpm10[-1],
        "o31":o3temp[-7],"o32":o3temp[-6],"o33":o3temp[-5],"o34":o3temp[-4],"o35":o3temp[-3],"o36":o3temp[-2],"o3now":o3temp[-1],
        "co1":cotemp[-7],"co2":cotemp[-6],"co3":cotemp[-5],"co4":cotemp[-4],"co5":cotemp[-3],"co6":cotemp[-2],"conow":cotemp[-1],
        "no21":no2temp[-7],"no22":no2temp[-6],"no23":no2temp[-5],"no24":no2temp[-4],"no25":no2temp[-3],"no26":no2temp[-2],"no2now":no2temp[-1],
        "so21":so2temp[-7],"so22":so2temp[-6],"so23":so2temp[-5],"so24":so2temp[-4],"so25":so2temp[-3],"so26":so2temp[-2],"so2now":so2temp[-1],
        "aqi1":AQI[-7],"aqi2":AQI[-6],"aqi3":AQI[-5],"aqi4":AQI[-4],"aqi5":AQI[-3],"aqi6":AQI[-2],
        "timeaqi1":timeAQI[-7],"timeaqi2":timeAQI[-6],"timeaqi3":timeAQI[-5],"timeaqi4":timeAQI[-4],"timeaqi5":timeAQI[-3],"timeaqi6":timeAQI[-2],"timeaqi7":timeAQI[-1],
        "timedata1":timedata[-7],"timedata2":timedata[-6],"timedata3":timedata[-5],"timedata4":timedata[-4],"timedata5":timedata[-3],"timedata6":timedata[-2],"timedata7":timedata[-1],
        "AQINOW":AQI[-1],"AQI1hrNOW":int(result1),"AQI24hrNOW":int(result24)})
    except(Exception) as e:
        print(e)
    print(dataaqi)
    client.publish("application/aqi",dataaqi)
    print('done')

def prediction1hr(predict1hr1):
    predict1hr2=[]
    predict1hr=[]
    predict1hr1 = scaler1hr.transform(predict1hr1)
    predict1hr2.append(predict1hr1)
    predict1hr.append(predict1hr2)
    return model1hr.predict_classes(predict1hr)

def prediction24hr(predict24hr1):
    predict24hr2=[]
    predict24hr=[]
    predict24hr1 = scaler24hr.transform(predict24hr1)
    predict24hr2.append(predict24hr1)
    predict24hr.append(predict24hr2)
    return model24hr.predict_classes(predict24hr)


if __name__ == "__main__":
    model1hr = load_model('my.modelLSTM1.h5')
    scaler1hr = joblib.load('model_norm1hr.pkl')
    scaler24hr = joblib.load('model_norm24hr.pkl')
    model24hr = load_model('my.modelLSTM24hr.h5')
        

    host = "161.246.6.158"
    port = 8083
    client = mqtt.Client() 
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host)
    client.loop_forever()


    