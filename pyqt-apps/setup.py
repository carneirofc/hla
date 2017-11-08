#!/usr/bin/env python-sirius

from setuptools import setup

with open('VERSION', 'r') as _f:
    __version__ = _f.read().strip()

setup(
    name='siriushla',
    version=__version__,
    author='lnls-sirius',
    description='Client Applications for Sirius',
    url='https://github.com/lnls-sirius/hla/pyqt-apps',
    download_url='https://github.com/lnls-sirius/hla',
    license='GNU GPLv3',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
        ],
    packages=['siriushla'],
    package_data={'siriushla': ['VERSION', '*/*.py']},
    scripts=[
        'scripts/sirius-hla-as-launcher.py',
        'scripts/sirius-hla-as-ti-control.py',
        'scripts/sirius-hla-as-ps-cycle.py',
        'scripts/sirius-hla-bo-ap-chromcorr.py',
        'scripts/sirius-hla-bo-ap-tunecorr.py',
        'scripts/sirius-hla-bo-config-manager.py',
        'scripts/sirius-hla-bo-ma-control.py',
        'scripts/sirius-hla-si-ap-currlt.py',
        'scripts/sirius-hla-si-ap-chromcorr.py',
        'scripts/sirius-hla-si-ap-tunecorr.py',
        'scripts/sirius-hla-si-config-manager.py',
        'scripts/sirius-hla-si-ap-sofb.py',
        'scripts/sirius-hla-si-ma-control.py',
        'scripts/sirius-hla-tb-ap-control.py',
        'scripts/sirius-hla-tb-ap-posang.py',
        'scripts/sirius-hla-tb-ma-control.py',
        'scripts/sirius-hla-ts-ap-control.py',
        'scripts/sirius-hla-ts-ap-posang.py',
        'scripts/sirius-hla-ts-ma-control.py',
        ],
    zip_safe=False
    )
