import numpy
import quandl

def test_code():
       data = quandl.get("EIA/PET_RWTC_D")
       print (data)

quandl.ApiConfig.api_key = "RnTDibGJFhuxmfvjGBuU"
test_code()
