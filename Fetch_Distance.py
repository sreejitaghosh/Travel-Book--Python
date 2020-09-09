from math import radians ,sin, cos, sqrt, atan2

def Fetch_Distance(Lat1,Lon1,Lat2,Lon2):
    Radius_Of_Earth = 6373
    Diff_Lat = radians(Lat2 - Lat1)
    Diff_Lon = radians(Lon2 - Lon1)
    SubCalculation = (sin(Diff_Lat/2)*sin(Diff_Lat/2)) + cos(radians(Lat1)) * cos(radians(Lat2)) * (sin(Diff_Lon/2)*sin(Diff_Lon/2))
    Final_Calculation = 2*Radius_Of_Earth*atan2(sqrt(SubCalculation), sqrt(1-SubCalculation))
    # Dist = round(Final_Calculation,2)
    Dist = Final_Calculation
    return Dist
