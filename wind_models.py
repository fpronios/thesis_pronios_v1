"""
The ``basic_example`` module shows a simple usage of the windpowerlib.

"""

__copyright__ = "Copyright oemof developer group"
__license__ = "GPLv3"

import os
import pandas as pd

try:
    from matplotlib import pyplot as plt
except ImportError:
    plt = None

from windpowerlib import modelchain
from windpowerlib import wind_turbine

# You can use the logging package to get logging messages from the windpowerlib
# Change the logging level if you want more or less messages
import logging
logging.getLogger().setLevel(logging.DEBUG)


def get_weather_data(filename='weather.csv', **kwargs):
    r"""
    Imports weather data from a file.

    The data include wind speed at two different heights in m/s, air
    temperature in two different heights in K, surface roughness length in m
    and air pressure in Pa. The file is located in the example folder of the
    windpowerlib. The height in m for which the data applies is specified in
    the second row.

    Parameters
    ----------
    filename : string
        Filename of the weather data file. Default: 'weather.csv'.

    Other Parameters
    ----------------
    datapath : string, optional
        Path where the weather data file is stored.
        Default: 'windpowerlib/example'.

    Returns
    -------
    weather_df : pandas.DataFrame
            DataFrame with time series for wind speed `wind_speed` in m/s,
            temperature `temperature` in K, roughness length `roughness_length`
            in m, and pressure `pressure` in Pa.
            The columns of the DataFrame are a MultiIndex where the first level
            contains the variable name as string (e.g. 'wind_speed') and the
            second level contains the height as integer at which it applies
            (e.g. 10, if it was measured at a height of 10 m).

    """

    if 'datapath' not in kwargs:
        kwargs['datapath'] = os.path.join(os.path.split(
            os.path.dirname(__file__))[0], 'example')
    file = os.path.join(kwargs['datapath'], filename)
    # read csv file
    weather_df = pd.read_csv(file, index_col=0, header=[0, 1])
    # change type of index to datetime and set time zone
    weather_df.index = pd.to_datetime(weather_df.index).tz_localize(
        'UTC').tz_convert('Europe/Berlin')
    # change type of height from str to int by resetting columns
    weather_df.columns = [weather_df.axes[1].levels[0][
                              weather_df.axes[1].labels[0]],
                          weather_df.axes[1].levels[1][
                              weather_df.axes[1].labels[1]].astype(int)]
    return weather_df


def initialise_wind_turbines():
    r"""
    Initialises two :class:`~.wind_turbine.WindTurbine` objects.

    Function shows two ways to initialise a WindTurbine object. You can either
    specify your own turbine, as done below for 'myTurbine', or fetch power
    and/or power coefficient curve data from data files provided by the
    windpowerlib, as done for the 'enerconE126'.
    Execute ``windpowerlib.wind_turbine.get_turbine_types()`` or
    ``windpowerlib.wind_turbine.get_turbine_types(
    filename='power_coefficient_curves.csv')`` to get a list of all wind
    turbines for which power and power coefficient curves respectively are
    provided.

    Returns
    -------
    Tuple (WindTurbine, WindTurbine)

    """

    # specification of own wind turbine (Note: power coefficient values and
    # nominal power have to be in Watt)
    myTurbine = {
        'name': 'myTurbine',
        'nominal_power': 3e6,  # in W
        'hub_height': 105,  # in m
        'rotor_diameter': 90,  # in m
        'power_curve': pd.DataFrame(
            data={'power': [p * 1000 for p in [
                      0.0, 26.0, 180.0, 1500.0, 3000.0, 3000.0]],  # in W
                  'wind_speed': [0.0, 3.0, 5.0, 10.0, 15.0, 25.0]})  # in m/s
    }
    # initialise WindTurbine object
    my_turbine = wind_turbine(**myTurbine)

    # specification of wind turbine where power curve is provided
    # if you want to use the power coefficient curve change the value of
    # 'fetch_curve' to 'power_coefficient_curve'
    enerconE126 = {
        'name': 'ENERCON E 126 7500',  # turbine name as in register
        'hub_height': 135,  # in m
        'rotor_diameter': 127,  # in m
        'fetch_curve': 'power_curve'  # fetch power curve
    }
    # initialise WindTurbine object
    e126 = wind_turbine(**enerconE126)

    return my_turbine, e126


def calculate_power_output(weather, my_turbine, e126):
    r"""
    Calculates power output of wind turbines using the
    :class:`~.modelchain.ModelChain`.

    The :class:`~.modelchain.ModelChain` is a class that provides all necessary
    steps to calculate the power output of a wind turbine. You can either use
    the default methods for the calculation steps, as done for 'my_turbine',
    or choose different methods, as done for the 'e126'.

    Parameters
    ----------
    weather : pd.DataFrame
        Contains weather data time series.
    my_turbine : WindTurbine
        WindTurbine object with self provided power curve.
    e126 : WindTurbine
        WindTurbine object with power curve from data file provided by the
        windpowerlib.

    """

    # power output calculation for my_turbine
    # initialise ModelChain with default parameters and use run_model method
    # to calculate power output
    mc_my_turbine = modelchain(my_turbine).run_model(weather)
    # write power output timeseries to WindTurbine object
    my_turbine.power_output = mc_my_turbine.power_output

    # power output calculation for e126
    # own specifications for ModelChain setup
    modelchain_data = {
        'wind_speed_model': 'logarithmic',  # 'logarithmic' (default),
                                            # 'hellman' or
                                            # 'interpolation_extrapolation'
        'density_model': 'ideal_gas',  # 'barometric' (default), 'ideal_gas' or
                                       # 'interpolation_extrapolation'
        'temperature_model': 'linear_gradient',  # 'linear_gradient' (def.) or
                                                 # 'interpolation_extrapolation'
        'power_output_model': 'power_curve',  # 'power_curve' (default) or
                                              # 'power_coefficient_curve'
        'density_correction': True,  # False (default) or True
        'obstacle_height': 0,  # default: 0
        'hellman_exp': None}  # None (default) or None
    # initialise ModelChain with own specifications and use run_model method
    # to calculate power output
    mc_e126 = modelchain(e126, **modelchain_data).run_model(weather)
    # write power output timeseries to WindTurbine object
    e126.power_output = mc_e126.power_output

    return


def plot_or_print(my_turbine, e126):
    r"""
    Plots or prints power output and power (coefficient) curves.

    Parameters
    ----------
    my_turbine : WindTurbine
        WindTurbine object with self provided power curve.
    e126 : WindTurbine
        WindTurbine object with power curve from data file provided by the
        windpowerlib.

    """

    # plot or print turbine power output
    if plt:
        e126.power_output.plot(legend=True, label='Enercon E126')
        my_turbine.power_output.plot(legend=True, label='myTurbine')
        plt.show()
    else:
        print(e126.power_output)
        print(my_turbine.power_output)

    # plot or print power (coefficient) curve
    if plt:
        if e126.power_coefficient_curve is not None:
            e126.power_coefficient_curve.plot(
                x='wind_speed', y='values', style='*',
                title='Enercon E126 power coefficient curve')
            plt.show()
        if e126.power_curve is not None:
            e126.power_curve.plot(x='wind_speed', y='values', style='*',
                                  title='Enercon E126 power curve')
            plt.show()
        if my_turbine.power_coefficient_curve is not None:
            my_turbine.power_coefficient_curve.plot(
                x='wind_speed', y='values', style='*',
                title='myTurbine power coefficient curve')
            plt.show()
        if my_turbine.power_curve is not None:
            my_turbine.power_curve.plot(x='wind_speed', y='values', style='*',
                                        title='myTurbine power curve')
            plt.show()
    else:
        if e126.power_coefficient_curve is not None:
            print(e126.power_coefficient_curve)
        if e126.power_curve is not None:
            print(e126.power_curve)


def run_basic_example():
    r"""
    Run the basic example.

    """
    weather = get_weather_data('weather.csv')
    my_turbine, e126 = initialise_wind_turbines()
    calculate_power_output(weather, my_turbine, e126)
    plot_or_print(my_turbine, e126)


if __name__ == "__main__":
    run_basic_example()