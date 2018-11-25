import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# pvlib imports
import pvlib
import datetime

from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP
from pvlib.pvsystem import PVSystem
from pvlib.location import Location
from pvlib.modelchain import ModelChain

# load some module and inverter specifications
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')

sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
cec_inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208_208V__CEC_2014_']


location = Location(latitude=36.430536, longitude=27.371117)
system = PVSystem(surface_tilt=20, surface_azimuth=200,
                  module_parameters=sandia_module,
                  inverter_parameters=cec_inverter)
mc = ModelChain(system, location)

latitude=36.430536
longitude=27.371117
tz='Europe/Athens'



start_date = pd.Timestamp(datetime.date.today(),tz = tz)
end_date = start_date + pd.Timedelta(days=7)
#model = GFS()
#raw_data = model.get_data(latitude,longitude,start_date, end_date)
#data = model.rename(raw_data)
#data['temp_air'] = model.kelvin_to_celsius(data['temp_air'])
#data['wind_speed'] = model.uv_to_speed(data)

#irrad_data = model.cloud_cover_to_irradiance(data['total_clouds'])
#data = data.join(irrad_data, how  = 'outer')

#data = data[model.output_variables]
#data = model.process_data(raw_data)

#print(mc)
weather = pd.DataFrame([[1050, 1000, 100, 30, 5]], columns=['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed'],
 index=[pd.Timestamp('20180101 1400', tz='Europe/Athens')])

mc.run_model(times=weather.index, weather=weather)

print(mc.ac)


mc.ac.fillna(0).plot()
plt.ylim(0,None)
plt.show()