import matplotlib.pyplot as plt
import numpy as np
import tmm

samples = 500  # Amount of samples around the desired wavelength
wave_length_delta = 5  # Wavelength range around the target wavelength

polarization = 'p'  # Polarization of incident light
target_wave_length = 13.5  # Target wavelength in vacuum
theta0 = np.deg2rad(0)  # Angle of incidence

n_high = 0.999 + 0.0018j  # Si
n_low = 0.9227 + 0.0062j  # Mo
n_vacuum = 1  # Refractive index of vacuum

pairs = 50  # Amount of thin film layer pairs

# Create the mirror
distance_list = [np.inf]
n_list = [n_vacuum]

for i in range(pairs):
    distance_list.append(target_wave_length / n_low / 4.0)
    n_list.append(n_low)
    distance_list.append(target_wave_length / n_high / 4.0)
    n_list.append(n_high)

distance_list.append(np.inf)
n_list.append(n_vacuum)

distance_list = np.real(distance_list)  # Avoids an error that distances have imaginary component

# The wavelengths we want to analyse
wave_length_list = np.linspace(target_wave_length - wave_length_delta, target_wave_length + wave_length_delta, samples)

# These arrays will contain the results of our calculations
reflection_list = []
transmission_list = []
absorption_list = []

for wave_length in wave_length_list:
    coh_tmm_result = tmm.coh_tmm(polarization, n_list, distance_list, theta0, wave_length)
    tmm_absorption_result = np.sum(tmm.absorp_in_each_layer(coh_tmm_result)[1:-1])

    reflection_list.append(coh_tmm_result['R'])
    transmission_list.append(coh_tmm_result['T'])
    absorption_list.append(tmm_absorption_result)

# Plot RT
plt.title('Transmission and reflection for various wave lengths')
plt.plot(wave_length_list, transmission_list, label="T")
plt.plot(wave_length_list, reflection_list, label="R")

plt.xlabel('Wavelength (nm)')
plt.ylabel('Fraction of incoming power')

plt.legend()
plt.grid()

plt.savefig('figures/RT.svg')

plt.show()

# Plot absorption
plt.title('Total absorption for various wave lengths')
plt.plot(wave_length_list, np.abs(absorption_list), label="Absorption")

plt.xlabel('Wavelength (nm)')
plt.ylabel('Fraction of incoming power')

plt.grid()

plt.savefig('figures/absorption.svg')

plt.show()
