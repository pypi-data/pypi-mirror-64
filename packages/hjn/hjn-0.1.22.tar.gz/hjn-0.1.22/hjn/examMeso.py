
import numpy as np

def getPoint(pre,df,lat0,lon0,resolution,decimal=1):
   
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[:, latIdx, lonIdx].round(decimals=decimal)

def getPointBilinear(preData,df1,latArr,lonArr,decimal=2):
    df=df1
    resolution=np.abs((latArr[0]-latArr[-1])/(len(latArr)-1))
    latIdxN = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)
    lonIdxW = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)

    latIdxS = ((latArr[0] - df["Lat"]) / resolution).astype(np.int64)+1
    lonIdxE = ((df["Lon"] - lonArr[0]) / resolution).astype(np.int64)+1

    df["LatN"] = latArr[latIdxN]
    df["LonW"] = lonArr[lonIdxW]
    df["valNW"] = preData[:, latIdxN, lonIdxW]

    df["LatS"] = latArr[latIdxS]
    df["LonE"] = lonArr[lonIdxE]
    df["valSE"] = preData[:, latIdxS, lonIdxE]
    df["valNE"] = preData[:, latIdxN, lonIdxE]
    df["valSW"] = preData[:, latIdxS, lonIdxW]
    return df.apply(
                lambda x:np.round(bilinear(x["Lat"], x["Lon"], x["LatN"], x["LonW"], x["valNW"], x["LatN"], x["LonE"], x["valNE"], x["LatS"],
                                   x["LonW"], x["valSW"], x["LatS"], x["LonE"], x["valSE"]),decimals=decimal), axis=1)


