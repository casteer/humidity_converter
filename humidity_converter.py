# -*- coding: utf-8 -*-


# Class to convert from relative humidity to absolute humidity
#  - Uses info from here: https://www.cactus2000.de/js/calchum.pdf
class humidity_converter:

    def __init__(self, relative_humidity, temperature, pressure):
        self.air_density = pressure*100.0/(8.31447215*(temperature+273.15))

        self.vapour_pressure = self.calculate_vapour_pressure(temperature)
        self.partial_pressure = (float(relative_humidity)/100.0)*self.vapour_pressure
        self.volume_mixing_ratio =  self.partial_pressure / pressure

        self.dry_air_molar_mass = 28.9644 # in g/mol
        self.water_molar_mass = 18.01534 # in g/mol

        self.specific_humidity = (self.volume_mixing_ratio*self.water_molar_mass)/(self.volume_mixing_ratio*self.water_molar_mass + (1.0-self.volume_mixing_ratio)*self.dry_air_molar_mass)
        self.mass_mixing_ratio = (self.specific_humidity/(1.0 - self.specific_humidity))
        self.mass_concentration = self.volume_mixing_ratio * self.air_density * self.water_molar_mass
        self.molecular_concentration = self.volume_mixing_ratio*self.air_density*6.0221415e23*1.0e-6

    def prettify_print(self):
        print("Air Density (mol/m^3): ", self.air_density)
        print("Vapour Pressure (hPa): ", self.vapour_pressure)
        print("Specific Humidity (kg/kg): ", self.specific_humidity)
        print("Mixing Ratio (kg/kg): ", self.mass_mixing_ratio)
        print("Mass Concentration (g/m^3): ", self.mass_concentration)

    # Calculate the vapour pressure in hPa
    #  - Temperature is in Celsius
    def calculate_vapour_pressure(self,T):

        if((T<-50) or (T>100)):
            print("WARNING : Temperature outside range of vapour pressure fit")

        # Parameters of empirical fit
        a_water =[6.107799961, 4.436518521e-1,1.428945805e-2, 2.650648471e-4, 3.031240396e-6, 2.034080948e-8, 6.136820929e-11]
        a_ice =[6.109177956, 5.034698970e-1, 1.886013408e-2, 4.176223716e-4, 5.824720280e-6, 4.838803174e-8, 1.838826904e-10]

        # Create a vector of powers of T
        Tpoly = []
        for i,a in enumerate(a_water):
            Tpoly.append(T**i);

        # Calculate the vapour pressure for liquid water at T
        e_water = 0;
        for i,a in enumerate(a_water):
            e_water += Tpoly[i]*a

        # Calculate the vapour pressure for liquid water at T
        e_ice = 0;
        for i,a in enumerate(a_water):
            e_ice += Tpoly[i]*a

        return min(e_water,e_ice)


