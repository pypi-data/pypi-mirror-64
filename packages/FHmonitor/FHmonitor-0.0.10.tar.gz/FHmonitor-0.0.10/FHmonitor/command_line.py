from FHmonitor.monitor import Monitor  # noqa
from FHmonitor.calibrate import Calibrate  # noqa
import textwrap
import pathlib
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


def _modify_shell_script_with_proj_path():
    """Modify run_FHmonitor_main.sh's PROJ_PATH line to
    represent the path to where the systemd files are
    located.

    :return: systemd_path.  The absolute path to the systemd files.
    This is used by subsequent functions.

    """
    package_path = pathlib.Path(__file__).parent.absolute()
    project_path = os.path.dirname(package_path)
    systemd_path = os.path.join(package_path, 'systemd')
    # The shell file is called by FHmonitor_main.service to
    # execute FHmonitor_main.py
    shell_filename = systemd_path+'/run_FHmonitor_main.sh'
    with open(shell_filename) as f:
        # Get the contents of the shell file as a list of text.
        contents = f.readlines()
        f.close()
        # Find and replace the ProjPath line
    for i, c in enumerate(contents):
        if "ProjPath" in c:
            contents[i] = "ProjPath="+project_path+"\n"
            break
    with open(shell_filename, "w") as f:
        contents = "".join(contents)
        f.write(contents)
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


def install_service():
    """Install FHmonitor_main.service by doing all the steps that
    would be necessary to do by hand.  The name of the functions
    should provide enough of a clue as to what is going on.
    """
    systemd_path = _modify_shell_script_with_proj_path()
    _modify_service_file_with_systemd_path(systemd_path)
    _change_perms_on_files(systemd_path)
    _copy_systemd_files(systemd_path)
    start_service()


def start_service():
    """Get the systemd service up and running that runs FHmonitor_main.py

    """
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
    pass


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
