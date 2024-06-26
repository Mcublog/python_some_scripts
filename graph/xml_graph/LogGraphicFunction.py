#! /bin/env python3

import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import os, numpy
import pathlib


def get_datetime_from_report(report, datetime):
    timestamp = report.find('timestamp')
    return (timestamp.find(datetime).text)


def get_float_from_dev_report(report, device, param):
    dev = report.find(device)
    return get_float_from_report(dev, param)


def get_float_from_report(report, param):
    temp = report.find(param).text
    if ',' in temp:
        temp = temp.replace(',', '.')
    return (float(temp))


def set_plt_title_and_ylabel(plt, title, label):
    plt.title(title, fontsize=14)
    plt.ylabel(label, fontsize=12)


def get_acc_setting(report, param):
    header = report.find('header')
    settings = header.find('settings')
    try:
        return settings.find(param)
    except:
        return


def get_acc_time(report):
    header = report.find('header')
    try:
        return header.find('time').text
    except:
        return


def get_list_files(file_name):
    # Set path to data file
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = pathlib.Path(current_path).joinpath('data')
    dir_list = os.listdir(data_path)
    file_list = os.listdir(data_path.joinpath(dir_list[0]))

    file_list.sort()
    idx = 0
    for (i, file) in enumerate(file_list):
        if (file_name in file):
            print('file: ' + file)
            idx = i
            break
    print(idx)
    del file_list[0:idx]
    return file_list


def show_tph_graph(path, type='Temperature'):
    tree = ET.parse(path)
    reports = tree.getroot()
    if reports.tag != 'tph_report':
        return

    x_tick = []  # x ticks like 10:42:30:513, 10:42:31:513 and etc
    hdc_temp = []  # temperature from hdc1080
    hdc_hum = []  # hummidity from hdc1080
    lps_temp = []  # temperature from lps331
    lps_p = []  # pressure from lps331

    for report in reports:
        # Get node timestamp for x_ticks
        x_tick.append(get_datetime_from_report(report, 'time')[:-4])
        # Get data from hdc1080 node
        hdc_temp.append(get_float_from_dev_report(report, 'hdc1080', 't'))
        hdc_hum.append(get_float_from_dev_report(report, 'hdc1080', 'hum'))
        # Get data from lps331 node
        lps_temp.append(get_float_from_dev_report(report, 'lps331', 't'))
        lps_p.append(get_float_from_dev_report(report, 'lps331', 'p'))

    # Create plots
    fig, ax = plt.subplots()
    plt.xlabel("Time", fontsize=8)
    # Generate a list from 0 to report number
    x = [++i for i in range(len(reports))]
    if type == 'Humidity':
        set_plt_title_and_ylabel(plt, 'Humidity graphic', 'Humidity')
        ax.plot(x, hdc_hum, 'b-', label='hdc1080 humidity')
        y_mean = numpy.mean(hdc_hum)
    elif type == 'Pressure':
        set_plt_title_and_ylabel(plt, 'Pressure graphic', 'Pressure')
        ax.plot(x, lps_p, 'r-', label='lps331 pressure')
        y_mean = numpy.mean(lps_p)
    else:
        set_plt_title_and_ylabel(plt, 'Temperature graphic', 'Temperature')
        ax.plot(x, hdc_temp, 'r-', label='hdc_temp')
        ax.plot(x, lps_temp, 'y-', label='lps331')
        y_mean = numpy.mean(hdc_temp)

    # Create x_tick, grid and legend
    plt.xticks(x, x_tick, rotation=90)
    plt.grid(linestyle='dashed')
    legend = ax.legend(loc='best')

    # Set the origin
    ax.axhline(y=y_mean - y_mean * 0.1, color='k')
    ax.axvline(x=0, color='k')

    # Set fig to fullscreen
    mng = plt.get_current_fig_manager()
    mng.window.state('normal')

    plt.show()


def show_acc_graph(path):
    tree = ET.parse(path)
    root = tree.getroot()
    if root.tag != 'acc_report':
        return

    x_tick = [
    ]  # x ticks like 10:42:30:513, 0.25 us, 0.5 us and etc depends of freq
    accx = []  # acc for axis
    accy = []  # acc for axis
    accz = []  # acc for axis

    # get node data
    freq = float(get_acc_setting(root, 'freq').text)
    reports = root.find('report')
    for i, report in enumerate(reports):
        x_tick.append(i / freq * 1000)
        accx.append(get_float_from_report(report, 'x'))
        accy.append(get_float_from_report(report, 'y'))
        accz.append(get_float_from_report(report, 'z'))

    # Create plots
    fig, ax = plt.subplots()
    set_plt_title_and_ylabel(plt, 'ACC graphic', 'g')
    plt.xlabel("Time", fontsize=8)

    # Generate a list from 0 to report number
    x = [++i for i in range(len(reports))]
    ax.plot(x, accx, 'r-', label='x')
    ax.plot(x, accy, 'y-', label='y')
    ax.plot(x, accz, 'g-', label='z')

    # Create x_tick, grid and legend
    x_tick[0] = get_acc_time(root)
    plt.xticks(x, x_tick, rotation=90)
    plt.grid(linestyle='dashed')
    ax.legend(loc='best')

    # Set the origin
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    # Set fig to fullscreen
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()


def show_jrnl_graph(path, type='Voltage'):
    tree = ET.parse(path)
    journal = tree.getroot()
    if journal.tag != 'jornal':
        return

    accx = []  # acc for axis
    accy = []  # acc for axis
    accz = []  # acc for axis

    x_tick = []  # x ticks like 10:42:30:513, 10:42:31:513 and etc
    hdc_temp = []  # temperature from hdc1080
    hdc_hum = []  # hummidity from hdc1080
    lps_temp = []  # temperature from lps331
    lps_p = []  # pressure from lps331

    volt = []  # voltage

    for record in journal:
        # Get node timestamp for x_ticks
        x_tick.append(get_datetime_from_report(record, 'time')[:-4])
        # Get data from hdc1080 node
        hdc_temp.append(get_float_from_dev_report(record, 'hdc1080', 't'))
        hdc_hum.append(get_float_from_dev_report(record, 'hdc1080', 'hum'))
        # Get data from lps331 node
        lps_temp.append(get_float_from_dev_report(record, 'lps331', 't'))
        lps_p.append(get_float_from_dev_report(record, 'lps331', 'p'))
        #Get battary voltage
        volt.append(get_float_from_dev_report(record, 'battary_voltage', 'v'))
        #Get acc
        acc_record = record.find('acc_record')
        accx.append(get_float_from_report(acc_record, 'x'))
        accy.append(get_float_from_report(acc_record, 'y'))
        accz.append(get_float_from_report(acc_record, 'z'))

    # Create plots
    fig, ax = plt.subplots()
    plt.xlabel("Time", fontsize=8)
    # Generate a list from 0 to report number
    x = [++i for i in range(len(journal))]
    y_mean = 0
    if type == 'Humidity':
        set_plt_title_and_ylabel(plt, 'Humidity graphic', 'Humidity')
        ax.plot(x, hdc_hum, 'b-', label='hdc1080 humidity')
        y_mean = numpy.mean(hdc_hum)

    elif type == 'Pressure':
        set_plt_title_and_ylabel(plt, 'Pressure graphic', 'Pressure')
        ax.plot(x, lps_p, 'r-', label='lps331 pressure')
        y_mean = numpy.mean(lps_p)

    elif type == 'Temperature':
        set_plt_title_and_ylabel(plt, 'Temperature graphic', 'Temperature')
        ax.plot(x, hdc_temp, 'r-', label='hdc_temp')
        ax.plot(x, lps_temp, 'y-', label='lps331')
        y_mean = numpy.mean(hdc_temp)

    elif type == 'Voltage':
        set_plt_title_and_ylabel(plt, 'Battery voltage graphic', 'V')
        ax.plot(x, volt, 'b-', label='Voltage')
        y_mean = numpy.mean(volt)

    elif type == 'Acc':
        set_plt_title_and_ylabel(plt, 'ACC graphic', 'g')
        ax.plot(x, accx, 'r-', label='x')
        ax.plot(x, accy, 'y-', label='y')
        ax.plot(x, accz, 'g-', label='z')

    else:
        return

    # Create x_tick, grid and legend
    plt.xticks(x, x_tick, rotation=90)
    plt.grid(linestyle='dashed')
    legend = ax.legend(loc='best')

    # Set the origin
    if y_mean:
        ax.axhline(y=y_mean - y_mean * 0.1, color='k')
        ax.axvline(x=0, color='k')
    else:
        ax.axhline(y=0, color='k')
        ax.axvline(x=0, color='k')

    # Set fig to fullscreen
    mng = plt.get_current_fig_manager()
    mng.window.state('normal')

    plt.show()


def show_graph(path):
    if not os.path.isfile(path):
        return
    if 'acc_report' in f"{path}":
        show_acc_graph(path)
    if 'tph_report' in f"{path}":
        show_tph_graph(path)
    if 'jornal' in f"{path}":
        show_jrnl_graph(path)


def main():
    # fl = get_list_files('tph_report')
    # fl = get_list_files('acc_report')
    fl = get_list_files('jornal')
    #print(fl)
    current_path = os.path.dirname(os.path.realpath(__file__))
    data_path = pathlib.Path(current_path).joinpath('data')
    dir_list = os.listdir(data_path)
    path = data_path.joinpath(dir_list[0]).joinpath(fl[0])
    print(path)
    show_graph(path)


if __name__ == '__main__':
    main()
