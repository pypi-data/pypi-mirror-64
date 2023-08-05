# coding: utf-8

import sys
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from hashlib import sha256

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
        self.up_name = name.upper()
        self.line_number = None
        self.version = None
        self.new_version = None

    def __str__(self):
        return 'PackageInfo(up_name={}, line_number={}, version={}, new_version={})'.format(
            self.up_name, self.line_number, self.version, self.new_version
        )


def main(verbose=0):
    import ensurepip

    ep_path = Path(ensurepip.__file__)
    if verbose > 0:
        print('ep_path', ep_path)
    wheel_dir = ep_path.parent / '_bundled'
    if verbose > 0:
        for whl in wheel_dir.glob('*.whl'):
            print('found', whl)
    package_infos = dict()
    for package in ['pip', 'setuptools']:
        package_infos[package] = PackageInfo(package)
    lines = ep_path.read_text().splitlines()
    found = 0
    for idx, line in enumerate(lines):
        for package_info in package_infos.values():
            if package_info.line_number is not None:
                continue
            if line.startswith(version_line.format(package_info.up_name)):
                package_info.line_number = idx
                quoted_version = line.split(' = ')[1].strip()
                package_info.version = intify(quoted_version.split(quoted_version[0])[1])
                found += 1
                if found >= len(package_infos):
                    break
    assert found == len(package_infos)
    for package in package_infos:
        package_info = package_infos[package]
        try:
            with urlopen('https://pypi.python.org/pypi/{}/json'.format(package)) as response:
                data = json.load(response)
                latest_version_str = data['info']['version']
                latest_version = intify(latest_version_str)
                if latest_version == package_info.version:
                    continue
                for dl in data['urls']:
                    if dl['packagetype'] != 'bdist_wheel' or dl['python_version'] != 'py2.py3':
                        continue
                    if verbose > 0:
                        json.dump(dl, sys.stdout, indent=2)
                    file_name = wheel_dir / dl['filename']
                    if file_name.exists():
                        package_info.new_version = latest_version_str
                        continue
                    if verbose > 1:
                        print('\ndownloading', dl['url'])
                    with urlopen(dl['url']) as response:
                        wheel_data = response.read()
                        assert sha256(wheel_data).hexdigest() == dl['digests']['sha256']
                        file_name.write_bytes(wheel_data)
                        package_info.new_version = latest_version_str
                if verbose > 1:
                    json.dump(data, sys.stdout, indent=2)
        except HTTPError:
            print('JSON package information for {} not found'.format(package))
            continue
    update = False
    for package in package_infos:
        pi = package_infos[package]
        if pi.new_version:
            lines[pi.line_number] = version_line_out.format(pi.up_name, pi.new_version)
            update = True
            print('{:<11} updated to {}'.format(package + ':', pi.new_version))
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
