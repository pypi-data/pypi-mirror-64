import pathlib
import os


def _modify_service_file_with_systemd_path(systemd_path):
    service_filename = systemd_path+'/FHmonitor_main.service'
    with open(service_filename) as f:
        contents = f.readlines()
        f.close()
    # Find and replace the ExecStart line
    for i, c in enumerate(contents):
        if "ExecStart" in c:
            contents[i] = "ExecStart="+service_filename+"\n"
            break
    print(contents)


def main():
    package_path = pathlib.Path(__file__).parent.absolute()
    systemd_path = os.path.join(package_path, 'systemd')
    _modify_service_file_with_systemd_path(systemd_path)


if __name__ == "__main__":
    main()
