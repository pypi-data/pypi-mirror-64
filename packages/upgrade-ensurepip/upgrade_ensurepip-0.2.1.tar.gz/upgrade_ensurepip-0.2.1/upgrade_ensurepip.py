# coding: utf-8

import sys
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from hashlib import sha256
from subprocess import check_output, CalledProcessError

version_line = '_{}_VERSION = '
version_line_out = version_line + '"{}"'


def intify(s):
    segments = []
    for segment in s.split('.'):
        try:
            segments.append(int(segment))
        except ValueError:
            segments.append(segment)
    return tuple(segments)


class PackageInfo:
    def __init__(self, name):
        self.name = name
        self.up_name = self.name.upper()
        self.line_number = None
        self.version = None
        self.new_version = None

    def __str__(self):
        return 'PackageInfo(up_name={}, line_number={}, version={}, new_version={})'.format(
            self.up_name, self.line_number, self.version, self.new_version
        )


def download_package_json(pkg, wheel_dir, verbose=0):
    """this extracts the latest version number and URL from the JSON description,
    then downloads from the URL if there is a newer version"""
    try:
        with urlopen('https://pypi.org/pypi/{}/json'.format(pkg.name)) as response:
            data = json.load(response)
            latest_version_str = data['info']['version']
            latest_version = intify(latest_version_str)
            if latest_version == pkg.version:
                return False
            for dl in data['urls']:
                # setuptools now is a py3 only wheel
                if dl['packagetype'] != 'bdist_wheel' or dl['python_version'] not in [
                    'py2.py3',
                    'py3',
                ]:
                    continue
                if verbose > 1:
                    json.dump(dl, sys.stdout, indent=2)
                file_name = wheel_dir / dl['filename']
                if file_name.exists():
                    pkg.new_version = latest_version_str
                    continue
                if verbose > 0:
                    print('\ndownloading', dl['url'])
                with urlopen(dl['url']) as response:
                    wheel_data = response.read()
                    assert sha256(wheel_data).hexdigest() == dl['digests']['sha256']
                    file_name.write_bytes(wheel_data)
                    pkg.new_version = latest_version_str
            if verbose > 1:
                json.dump(data, sys.stdout, indent=2)
    except HTTPError:
        print('JSON package information for {} not found'.format(package))
        return False
    return True


def filtered_checkoutput(cmd, start_match):
    result = None
    for line in check_output(cmd).decode('utf-8').splitlines():
        if not line.startswith(start_match):
            continue
        if result is not None:
            print('cannot find unique version number filtering on [{}]'.format(start_match))
            return None
        result = line[len(start_match) :].split(')')[0]
    return result


def download_package_pip(pkg, wheel_dir, verbose=0):
    """this extracts the latest version number and URL from the JSON description,
    then downloads from the URL if there is a newer version"""
    pip = str(Path(sys.executable).parent / 'pip')
    latest_version_str = filtered_checkoutput([pip, 'search', pkg.name], pkg.name + ' (')
    if latest_version_str is None:
        return False
    latest_version = intify(latest_version_str)
    if latest_version == pkg.version:
        return True
    cmd = [pip, 'download', '--dest', wheel_dir, '--only-binary=:all:', pkg.name]
    try:
        if verbose > 0:
            print('\ndownloading', pkg.name, 'using', pip)
        res = check_output(cmd).decode('utf-8')
    except CalledProcessError:
        return False
    pkg.new_version = latest_version_str
    return True

_py2py3_pattern = '-py2.py3-none-any.whl'

def main(use_pip=None, verbose=0):
    import ensurepip

    if use_pip is None:
        use_pip = '--pip' in sys.argv
    expects_py2py3 = False
    ep_path = Path(ensurepip.__file__)
    if verbose > 0:
        print('ep_path', ep_path)
    wheel_dir = ep_path.parent / '_bundled'
    if verbose > 0:
        for whl in wheel_dir.glob('*.whl'):
            print('found', whl)  # wheels for pip, setuptools
    package_infos = dict()
    for package in ['pip', 'setuptools']:
        package_infos[package] = PackageInfo(package)
    lines = ep_path.read_text().splitlines()
    found = 0
    for idx, line in enumerate(lines):
        if not expects_py2py3 and _py2py3_pattern in line:
            # wheel_name = "{}-{}-py2.py3-none-any.whl".format(project, version)
            # but setuptools no longer is py2 starting with 45.1.0
            expects_py2py3 = True
        for package_info in package_infos.values():
            if package_info.line_number is not None:
                continue
            if line.startswith(version_line.format(package_info.up_name)):
                package_info.line_number = idx
                quoted_version = line.split(' = ')[1].strip()
                package_info.version = intify(quoted_version.split(quoted_version[0])[1])
                found += 1
    assert found == len(package_infos)
    for package in package_infos:
        package_info = package_infos[package]
        if use_pip:
            download_package_pip(package_info, wheel_dir, verbose=verbose)
        else:
            download_package_json(package_info, wheel_dir, verbose=verbose)
    update = False
    for package in package_infos:
        pi = package_infos[package]
        if pi.new_version:
            lines[pi.line_number] = version_line_out.format(pi.up_name, pi.new_version)
            update = True
            print('{:<11} updated to {}'.format(package + ':', pi.new_version))
        if expects_py2py3:
            whl = list(wheel_dir.glob('{}-{}-*.whl'.format(pi.name, pi.new_version)))
            if len(whl) == 1 and _py2py3_pattern not in whl[0].name:
                whl = whl[0]
                alt_name = whl.parent / whl.name.replace('-py3-none-any', '-py2.py3-none-any')
                if verbose > 0:
                    print('renaming', whl, '->', alt_name)
                if alt_name.exists():
                    whl.remove()
                else:
                    whl.rename(alt_name)
    if update:
        org = ep_path.with_suffix('.py.org')
        if not org.exists():
            ep_path.rename(org)
        ep_path.write_text('\n'.join(lines) + '\n')
    else:
        for package in package_infos:
            pi = package_infos[package]
            print('{} already at: {}'.format(package, '.'.join(str(x) for x in pi.version)))


if __name__ == '__main__':
    main()
