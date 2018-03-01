import os, csv, re
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
from collections import defaultdict
def readFile(fileName):
    input_data = defaultdict(list)
    def conv(s):
        try:
            s = float(s)
        except ValueError:
            pass
        return s

    with open(fileName,'rU') as file:
        reader = csv.reader(file, delimiter=',')

        for row in reader:
            data = [conv(cell) for cell in row]
    return data




def get_data_info(data_filename):
    name_regex = re.compile(r"""(
    (\w{4})             # Test
    (\d{2})             # Velocity
    (ms)                # Units
    (\-)?               # Possible dash
    (\d)?               # possible Number
    (\.txt)             # Suffix
                        )""", re.VERBOSE)
    regex_matches = name_regex.findall(data_filename)
    for match in regex_matches:
        if match[-2] == '':
            test = '1'
        else:
            test = match[-2]
        velocity = match[2]
        title = 'Filtered Butterworth Plot Data\nVelocity : {} m/s, Trial : {}'.format(velocity, test)
    return title, test, velocity

def get_pitot_info(data_filename):
    name_regex = re.compile(r"""(
    (\w{5}\_)            # pitot
    (\d{2})             # Velocity
    (mx\_)               # Units
    (\d)                # Trial number
    (\.csv)             # Suffix
                        )""", re.VERBOSE)
    regex_matches = name_regex.findall(data_filename)
    for match in regex_matches:

        velocity = match[2]
        test = match[4]
        title = 'Pitot Tube Data\nVelocity : {} m/s, Trial : {}'.format(velocity, test)
    return title, test, velocity

def butterworth_filter():
    # Plots text files using butterworth filter
    fs = 15000 # Sampling Frequency
    fc = 20 # Cutoff Frequency
    W_n = 2 * fc / fs # Natural Frequency
    b, a = signal.butter(3, W_n)

    load_cell_output = {'10': [],'20': [],'30': [],}

    pitot_tube_data = defaultdict(list)

    for file_name in os.listdir('.'):

        if file_name.lower().startswith('pitot'):

            label, trial, wind_vel = get_pitot_info(file_name)

            # print(label)
            file_data = readFile(file_name)
            pitot_tube_data[wind_vel].append(file_data)
            # print(file_data)
            # print(np.mean(file_data))
        # if file_name.lower().startswith('drag'):
        #     time, lift, drag = np.loadtxt(open(file_name), delimiter='\t', unpack=True)
        #     # x_values, y_values = readFile(file_name)
        #     # max_y = max(y_values)
        #     # max_y_loc = y_values.index(max_y)
        #     # max_x = x_values[max_y_loc]
        #     print(file_name)
        #     # print(get_graph_title(file_name))
        #     label, trial, wind_vel = get_data_info(file_name)
        #     # print(x_values)
        #     # for point in y_values:
        #     filtered_data = signal.filtfilt(b,a,drag)
        #     print('Success! Filtered {} elements!'.format(len(filtered_data)))
        #     plt.plot(time, filtered_data)
        #     plt.title(label)
        #     plt.xlabel('Time (s)')
        #     plt.ylabel('Signal Detected')
        #     plt.grid(which='both', axis='both')
        #     # plt.savefig('{}.pdf'.format(file_name[:-4]), bbox_inches='tight')
        #     plt.show()
        #     t_start = ''
        #     while t_start == '':
        #         t_start = int(input('Mean Data Start Collection Time (s) : '))
        #     t_end = ''
        #     while t_end == '':
        #         t_end = int(input('Mean Data End Collection Time (s) : '))
        #     i_start = t_start * 5000
        #     i_end = t_end * 5000
        #     data_range = filtered_data[i_start:i_end]
        #     data_point = np.mean(data_range)
        #     n_samples = len(data_range)
        #     load_cell_output[wind_vel].append(data_point)

        #     out_string = 'Velocity : {} m/s\nTrial : {}\nMean signal between {}s and {}s = {}\nSamples Collected : {}\n'.format(wind_vel, trial, t_start, t_end, data_point,n_samples)
        #     print(out_string)
        #     # with open('savefile.txt', 'a') as savefile:
        #     #     savefile.write(out_string)
    # for velocity in load_cell_output:
    #     print('Mean {} Voltage Measured : {}'.format(velocity, np.mean(load_cell_output[velocity])))
    tube_stats = {}
    tube_data = defaultdict(list)
    for tunnel_velocity in pitot_tube_data:
        for trial_no in range(len(pitot_tube_data[tunnel_velocity])):
            for tube in range(len(pitot_tube_data[tunnel_velocity][trial_no])):
                tube_data[tube].append(pitot_tube_data[tunnel_velocity][trial_no][tube])
                value_by_tube = tube_data[tube]
                # print(value_by_tube)
                n_samples = len(value_by_tube)
                # print('N-Samples : {}'.format(n_samples))
                t_crit = 2.776
                accuracy = 0.0625
                min_volt = 0.5
                max_volt = 4.5
                volt_span = max_volt - min_volt
                min_reading = -2
                max_reading = 2
                rho_air = 1.1695
                press_span = max_reading - min_reading
                acc_volt_err = accuracy * volt_span
                acc_press_err = (acc_volt_err * press_span/volt_span)
                # print(acc_press_err)
                tube_mean = np.mean(value_by_tube)
                tube_stDev = np.std(value_by_tube)
                rand_un = t_crit * tube_stDev/np.sqrt(n_samples)
                tot_err = np.sqrt(acc_press_err**2 + rand_un**2)
                tube_stats['{} m/s Tube {} Mean'.format(tunnel_velocity, int(tube)+1)] = tube_mean
                tube_stats['{} m/s Tube {} Uncertainty'.format(tunnel_velocity, int(tube)+1)] = tot_err



    for line in tube_stats:
        print('{} : {}'.format(line, tube_stats[line]))
    # return load_cell_output
    # print(pitot_tube_data)









butterworth_filter()
