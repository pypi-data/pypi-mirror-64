#!/home/pi/projects/FHmonitor/venv/bin/python3
from FHmonitor.monitor import Monitor  # noqa
from FHmonitor.calibrate import Calibrate  # noqa
import pdb
import textwrap
import os
import stat
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)
init_class_text_list = textwrap.wrap(("1) Create an instance of the "
                                      "Monitor class."), 50)
init_sensor_text_list = textwrap.wrap(("2) Initialize the energy meter..."
                                       "This can be tricky because accurate "
                                       "readings are dependent on calibrating "
                                       "params to init_sensor().  The param "
                                       " values depend on the Power "
                                       "Transformer and Current Transformers "
                                       "you are using.  "), 50)


def _create_shell_script():
    """ Creates the shell script (run_FHmonitor_main.sh) that
    starts up the python script that endlessly reads and stores
    power readings.  The venv is activated prior to running the
    python script.

    The absolute path to the location of the systemd files is
    returned for subsequent function calls to use.
    """
    package_path = os.path.abspath(os.path.dirname(__file__))
    systemd_path = os.path.join(package_path, 'systemd')
    shell_filename = systemd_path+'/run_FHmonitor_main.sh'
    with open(shell_filename, "w") as f:
        # Write the bin/bash line.
        f.write("#!/bin/bash\n")
        # Write the line to activate the venv.
        activate_venv = ". " + \
            package_path[:package_path.find("/lib")]+"/bin/activate\n"
        f.write(activate_venv)
        # Write the line to start up the python script that gathers
        # power readings.
        python_cmd = "python3 "+systemd_path+"/FHmonitor_main.py\n"
        f.write(python_cmd)
        f.close()
    return systemd_path


def _modify_service_file_with_systemd_path(systemd_path):
    """Change the ExecStart line to include the absolute path
    to the shell file (run_FHmonitor_main.sh).

    :param systemd_path: The directory where the files used to
    setup, start, and manage the systemd files are located.
    **The template service file MUST INCLUDE the ExecStart line.**
    """
    service_filename = systemd_path+'/FHmonitor_main.service'
    shell_filename = systemd_path+'/run_FHmonitor_main.sh'
    with open(service_filename) as f:
        contents = f.readlines()
        f.close()
    # Find and replace the ExecStart line
    for i, c in enumerate(contents):
        if "ExecStart" in c:
            contents[i] = "ExecStart="+shell_filename+"\n"
            break
    with open(service_filename, "w") as f:
        contents = "".join(contents)
        f.write(contents)
        f.close()


def _change_perms_on_files(systemd_path):
    filenames = ["/FHmonitor_main.py",
                 "/FHmonitor_main.service", "/run_FHmonitor_main.sh"]
    # Set perms so systemd can run the python file.
    for f in filenames:
        filename = systemd_path+f
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)


def _copy_systemd_files(systemd_path):
    # Copy service file where systemd expects it to be.
    service_path = systemd_path + '/FHmonitor_main.service'
    cmd_str = 'sudo cp ' + service_path + ' /lib/systemd/system/.'
    os.system(cmd_str)


def hello_monitor():
    """Checks to see if the monitor is hooked up properly and can
    give us power readings.
    """
    print(*(init_class_text_list[i]
            for i in range(len(init_class_text_list))), sep='\n')
    m = Monitor()
    print('==================================================')
    print('Success! Created an instance of the Monitor class.')
    print('==================================================')
    print(*(init_sensor_text_list[i]
            for i in range(len(init_sensor_text_list))), sep='\n')
    m.init_sensor()  # Using defaults, You may need to change settings.
    pA, pR = m.take_reading()
    print('==================================================')
    print('Success! Took a reading.')
    print('==================================================')
    print(f'Active Power: {pA:.2f}, Reactive Power: {pR:.2f}')
    print('==================================================')


def start_service():
    """Get the FHmonitor_main.service up set up correctly and started.


    """
    systemd_path = _create_shell_script()
    _modify_service_file_with_systemd_path(systemd_path)
    _change_perms_on_files(systemd_path)
    _copy_systemd_files(systemd_path)
    # Enable the service
    os.system('sudo systemctl enable FHmonitor_main')
    print('============================')
    print('FHmonitor_main service is...')
    os.system('systemctl is-enabled FHmonitor_main')
    print('============================')
    # Start the service
    os.system('sudo systemctl start FHmonitor_main')
    print('...status...')
    status_service()
    print('============================')


def stop_service():
    os.system('sudo systemctl stop FHmonitor_main')
    print('FHmonitor_main service has been stopped.')


def status_service():
    os.system('systemctl status FHmonitor_main')


def calibrate_voltage():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', action="store_true",
                        help='Save new gain.')
    args = parser.parse_args()
    c = Calibrate()
    c.calibrate_voltage(save_new_gain=args.save)


def calibrate_current():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', action="store_true",
                        help='Save new gain.')
    args = parser.parse_args()
    c = Calibrate()
    c.calibrate_current(save_new_gain=args.save)


# Executing scripts, not the module.


def main():
    pass


if __name__ == "__main__":
    main()
