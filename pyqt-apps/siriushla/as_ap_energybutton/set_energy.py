"""."""
from siriuspy.search import PSSearch as _PSSearch
from siriuspy.namesys import SiriusPVName as _SiriusPVName


_TIMEOUT = 0.05
DIPNAMES = {
    'TB': [_SiriusPVName('TB-Fam:PS-B'), ],
    'BO': [_SiriusPVName('BO-Fam:PS-B-1'), _SiriusPVName('BO-Fam:PS-B-2')],
    'TS': [_SiriusPVName('TS-Fam:PS-B'), ],
    'SI': [
        _SiriusPVName('SI-Fam:PS-B1B2-1'),
        _SiriusPVName('SI-Fam:PS-B1B2-2')]}


def init_section(section):
    """."""
    dipoles, magnets = _create_objects(section)
    dipoles, magnets = _create_pvs(dipoles, magnets)
    return dipoles, magnets


def _create_objects(section):
    """."""
    dipnames = DIPNAMES[section]
    psnames = _PSSearch.get_psnames({'sec': section})
    magnets = []
    dipoles = []
    for psname in psnames:
        if psname.dev.startswith('FC'):
            continue
        mfunc = _PSSearch.conv_psname_2_magfunc(psname)
        if mfunc == 'dipole':
            dipoles.append({'psname': psname, 'mafunc': mfunc})
            continue
        magnets.append({'psname': psname, 'mafunc': mfunc})
    return dipoles, magnets


def _create_pvs(dipoles, magnets):
    """."""
    dips = []
    for dipole in dipoles:
        dips.append(dipole['psname'].substitute(
            propty_name='Energy', propty_suffix='SP'))
    mags = set()
    for d in magnets:
        psname = d['psname']
        magf = d['mafunc']
        if 'corrector' in magf:
            mags.add(psname.substitute(
                propty_name='Kick', propty_suffix='SP'))
        elif 'quadrupole' in magf:
            mags.add(psname.substitute(
                propty_name='KL', propty_suffix='SP'))
        elif 'sextupole' in magf:
            mags.add(psname.substitute(
                propty_name='SL', propty_suffix='SP'))
    return dips, sorted(mags)
