import copy as _copy

_TRIGGERS= {
'SI-Glob:TI-Corrs:': {
    'events':('MigSI','Orbit','Study'),
    'trigger_type':'PSSI',
    'channels': (
        'SI-01M1:PS-CH:RSIO', 'SI-01M1:PS-CV:RSIO', 'SI-01M2:PS-CH:RSIO', 'SI-01M2:PS-CV:RSIO', 'SI-01C1:PS-CH:RSIO', 'SI-01C1:PS-CV:RSIO', 'SI-01C2:PS-CH:RSIO', 'SI-01C2:PS-CV-1:RSIO', 'SI-01C2:PS-CV-2:RSIO', 'SI-01C3:PS-CH:RSIO', 'SI-01C3:PS-CV-1:RSIO', 'SI-01C3:PS-CV-2:RSIO', 'SI-01C4:PS-CH:RSIO', 'SI-01C4:PS-CV:RSIO',
        'SI-02M1:PS-CH:RSIO', 'SI-02M1:PS-CV:RSIO', 'SI-02M2:PS-CH:RSIO', 'SI-02M2:PS-CV:RSIO', 'SI-02C1:PS-CH:RSIO', 'SI-02C1:PS-CV:RSIO', 'SI-02C2:PS-CH:RSIO', 'SI-02C2:PS-CV-1:RSIO', 'SI-02C2:PS-CV-2:RSIO', 'SI-02C3:PS-CH:RSIO', 'SI-02C3:PS-CV-1:RSIO', 'SI-02C3:PS-CV-2:RSIO', 'SI-02C4:PS-CH:RSIO', 'SI-02C4:PS-CV:RSIO',
        'SI-03M1:PS-CH:RSIO', 'SI-03M1:PS-CV:RSIO', 'SI-03M2:PS-CH:RSIO', 'SI-03M2:PS-CV:RSIO', 'SI-03C1:PS-CH:RSIO', 'SI-03C1:PS-CV:RSIO', 'SI-03C2:PS-CH:RSIO', 'SI-03C2:PS-CV-1:RSIO', 'SI-03C2:PS-CV-2:RSIO', 'SI-03C3:PS-CH:RSIO', 'SI-03C3:PS-CV-1:RSIO', 'SI-03C3:PS-CV-2:RSIO', 'SI-03C4:PS-CH:RSIO', 'SI-03C4:PS-CV:RSIO',
        'SI-04M1:PS-CH:RSIO', 'SI-04M1:PS-CV:RSIO', 'SI-04M2:PS-CH:RSIO', 'SI-04M2:PS-CV:RSIO', 'SI-04C1:PS-CH:RSIO', 'SI-04C1:PS-CV:RSIO', 'SI-04C2:PS-CH:RSIO', 'SI-04C2:PS-CV-1:RSIO', 'SI-04C2:PS-CV-2:RSIO', 'SI-04C3:PS-CH:RSIO', 'SI-04C3:PS-CV-1:RSIO', 'SI-04C3:PS-CV-2:RSIO', 'SI-04C4:PS-CH:RSIO', 'SI-04C4:PS-CV:RSIO',
        'SI-05M1:PS-CH:RSIO', 'SI-05M1:PS-CV:RSIO', 'SI-05M2:PS-CH:RSIO', 'SI-05M2:PS-CV:RSIO', 'SI-05C1:PS-CH:RSIO', 'SI-05C1:PS-CV:RSIO', 'SI-05C2:PS-CH:RSIO', 'SI-05C2:PS-CV-1:RSIO', 'SI-05C2:PS-CV-2:RSIO', 'SI-05C3:PS-CH:RSIO', 'SI-05C3:PS-CV-1:RSIO', 'SI-05C3:PS-CV-2:RSIO', 'SI-05C4:PS-CH:RSIO', 'SI-05C4:PS-CV:RSIO',
        'SI-06M1:PS-CH:RSIO', 'SI-06M1:PS-CV:RSIO', 'SI-06M2:PS-CH:RSIO', 'SI-06M2:PS-CV:RSIO', 'SI-06C1:PS-CH:RSIO', 'SI-06C1:PS-CV:RSIO', 'SI-06C2:PS-CH:RSIO', 'SI-06C2:PS-CV-1:RSIO', 'SI-06C2:PS-CV-2:RSIO', 'SI-06C3:PS-CH:RSIO', 'SI-06C3:PS-CV-1:RSIO', 'SI-06C3:PS-CV-2:RSIO', 'SI-06C4:PS-CH:RSIO', 'SI-06C4:PS-CV:RSIO',
        'SI-07M1:PS-CH:RSIO', 'SI-07M1:PS-CV:RSIO', 'SI-07M2:PS-CH:RSIO', 'SI-07M2:PS-CV:RSIO', 'SI-07C1:PS-CH:RSIO', 'SI-07C1:PS-CV:RSIO', 'SI-07C2:PS-CH:RSIO', 'SI-07C2:PS-CV-1:RSIO', 'SI-07C2:PS-CV-2:RSIO', 'SI-07C3:PS-CH:RSIO', 'SI-07C3:PS-CV-1:RSIO', 'SI-07C3:PS-CV-2:RSIO', 'SI-07C4:PS-CH:RSIO', 'SI-07C4:PS-CV:RSIO',
        'SI-08M1:PS-CH:RSIO', 'SI-08M1:PS-CV:RSIO', 'SI-08M2:PS-CH:RSIO', 'SI-08M2:PS-CV:RSIO', 'SI-08C1:PS-CH:RSIO', 'SI-08C1:PS-CV:RSIO', 'SI-08C2:PS-CH:RSIO', 'SI-08C2:PS-CV-1:RSIO', 'SI-08C2:PS-CV-2:RSIO', 'SI-08C3:PS-CH:RSIO', 'SI-08C3:PS-CV-1:RSIO', 'SI-08C3:PS-CV-2:RSIO', 'SI-08C4:PS-CH:RSIO', 'SI-08C4:PS-CV:RSIO',
        'SI-09M1:PS-CH:RSIO', 'SI-09M1:PS-CV:RSIO', 'SI-09M2:PS-CH:RSIO', 'SI-09M2:PS-CV:RSIO', 'SI-09C1:PS-CH:RSIO', 'SI-09C1:PS-CV:RSIO', 'SI-09C2:PS-CH:RSIO', 'SI-09C2:PS-CV-1:RSIO', 'SI-09C2:PS-CV-2:RSIO', 'SI-09C3:PS-CH:RSIO', 'SI-09C3:PS-CV-1:RSIO', 'SI-09C3:PS-CV-2:RSIO', 'SI-09C4:PS-CH:RSIO', 'SI-09C4:PS-CV:RSIO',
        'SI-10M1:PS-CH:RSIO', 'SI-10M1:PS-CV:RSIO', 'SI-10M2:PS-CH:RSIO', 'SI-10M2:PS-CV:RSIO', 'SI-10C1:PS-CH:RSIO', 'SI-10C1:PS-CV:RSIO', 'SI-10C2:PS-CH:RSIO', 'SI-10C2:PS-CV-1:RSIO', 'SI-10C2:PS-CV-2:RSIO', 'SI-10C3:PS-CH:RSIO', 'SI-10C3:PS-CV-1:RSIO', 'SI-10C3:PS-CV-2:RSIO', 'SI-10C4:PS-CH:RSIO', 'SI-10C4:PS-CV:RSIO',
        'SI-11M1:PS-CH:RSIO', 'SI-11M1:PS-CV:RSIO', 'SI-11M2:PS-CH:RSIO', 'SI-11M2:PS-CV:RSIO', 'SI-11C1:PS-CH:RSIO', 'SI-11C1:PS-CV:RSIO', 'SI-11C2:PS-CH:RSIO', 'SI-11C2:PS-CV-1:RSIO', 'SI-11C2:PS-CV-2:RSIO', 'SI-11C3:PS-CH:RSIO', 'SI-11C3:PS-CV-1:RSIO', 'SI-11C3:PS-CV-2:RSIO', 'SI-11C4:PS-CH:RSIO', 'SI-11C4:PS-CV:RSIO',
        'SI-12M1:PS-CH:RSIO', 'SI-12M1:PS-CV:RSIO', 'SI-12M2:PS-CH:RSIO', 'SI-12M2:PS-CV:RSIO', 'SI-12C1:PS-CH:RSIO', 'SI-12C1:PS-CV:RSIO', 'SI-12C2:PS-CH:RSIO', 'SI-12C2:PS-CV-1:RSIO', 'SI-12C2:PS-CV-2:RSIO', 'SI-12C3:PS-CH:RSIO', 'SI-12C3:PS-CV-1:RSIO', 'SI-12C3:PS-CV-2:RSIO', 'SI-12C4:PS-CH:RSIO', 'SI-12C4:PS-CV:RSIO',
        'SI-13M1:PS-CH:RSIO', 'SI-13M1:PS-CV:RSIO', 'SI-13M2:PS-CH:RSIO', 'SI-13M2:PS-CV:RSIO', 'SI-13C1:PS-CH:RSIO', 'SI-13C1:PS-CV:RSIO', 'SI-13C2:PS-CH:RSIO', 'SI-13C2:PS-CV-1:RSIO', 'SI-13C2:PS-CV-2:RSIO', 'SI-13C3:PS-CH:RSIO', 'SI-13C3:PS-CV-1:RSIO', 'SI-13C3:PS-CV-2:RSIO', 'SI-13C4:PS-CH:RSIO', 'SI-13C4:PS-CV:RSIO',
        'SI-14M1:PS-CH:RSIO', 'SI-14M1:PS-CV:RSIO', 'SI-14M2:PS-CH:RSIO', 'SI-14M2:PS-CV:RSIO', 'SI-14C1:PS-CH:RSIO', 'SI-14C1:PS-CV:RSIO', 'SI-14C2:PS-CH:RSIO', 'SI-14C2:PS-CV-1:RSIO', 'SI-14C2:PS-CV-2:RSIO', 'SI-14C3:PS-CH:RSIO', 'SI-14C3:PS-CV-1:RSIO', 'SI-14C3:PS-CV-2:RSIO', 'SI-14C4:PS-CH:RSIO', 'SI-14C4:PS-CV:RSIO',
        'SI-15M1:PS-CH:RSIO', 'SI-15M1:PS-CV:RSIO', 'SI-15M2:PS-CH:RSIO', 'SI-15M2:PS-CV:RSIO', 'SI-15C1:PS-CH:RSIO', 'SI-15C1:PS-CV:RSIO', 'SI-15C2:PS-CH:RSIO', 'SI-15C2:PS-CV-1:RSIO', 'SI-15C2:PS-CV-2:RSIO', 'SI-15C3:PS-CH:RSIO', 'SI-15C3:PS-CV-1:RSIO', 'SI-15C3:PS-CV-2:RSIO', 'SI-15C4:PS-CH:RSIO', 'SI-15C4:PS-CV:RSIO',
        'SI-16M1:PS-CH:RSIO', 'SI-16M1:PS-CV:RSIO', 'SI-16M2:PS-CH:RSIO', 'SI-16M2:PS-CV:RSIO', 'SI-16C1:PS-CH:RSIO', 'SI-16C1:PS-CV:RSIO', 'SI-16C2:PS-CH:RSIO', 'SI-16C2:PS-CV-1:RSIO', 'SI-16C2:PS-CV-2:RSIO', 'SI-16C3:PS-CH:RSIO', 'SI-16C3:PS-CV-1:RSIO', 'SI-16C3:PS-CV-2:RSIO', 'SI-16C4:PS-CH:RSIO', 'SI-16C4:PS-CV:RSIO',
        'SI-17M1:PS-CH:RSIO', 'SI-17M1:PS-CV:RSIO', 'SI-17M2:PS-CH:RSIO', 'SI-17M2:PS-CV:RSIO', 'SI-17C1:PS-CH:RSIO', 'SI-17C1:PS-CV:RSIO', 'SI-17C2:PS-CH:RSIO', 'SI-17C2:PS-CV-1:RSIO', 'SI-17C2:PS-CV-2:RSIO', 'SI-17C3:PS-CH:RSIO', 'SI-17C3:PS-CV-1:RSIO', 'SI-17C3:PS-CV-2:RSIO', 'SI-17C4:PS-CH:RSIO', 'SI-17C4:PS-CV:RSIO',
        'SI-18M1:PS-CH:RSIO', 'SI-18M1:PS-CV:RSIO', 'SI-18M2:PS-CH:RSIO', 'SI-18M2:PS-CV:RSIO', 'SI-18C1:PS-CH:RSIO', 'SI-18C1:PS-CV:RSIO', 'SI-18C2:PS-CH:RSIO', 'SI-18C2:PS-CV-1:RSIO', 'SI-18C2:PS-CV-2:RSIO', 'SI-18C3:PS-CH:RSIO', 'SI-18C3:PS-CV-1:RSIO', 'SI-18C3:PS-CV-2:RSIO', 'SI-18C4:PS-CH:RSIO', 'SI-18C4:PS-CV:RSIO',
        'SI-19M1:PS-CH:RSIO', 'SI-19M1:PS-CV:RSIO', 'SI-19M2:PS-CH:RSIO', 'SI-19M2:PS-CV:RSIO', 'SI-19C1:PS-CH:RSIO', 'SI-19C1:PS-CV:RSIO', 'SI-19C2:PS-CH:RSIO', 'SI-19C2:PS-CV-1:RSIO', 'SI-19C2:PS-CV-2:RSIO', 'SI-19C3:PS-CH:RSIO', 'SI-19C3:PS-CV-1:RSIO', 'SI-19C3:PS-CV-2:RSIO', 'SI-19C4:PS-CH:RSIO', 'SI-19C4:PS-CV:RSIO',
        'SI-20M1:PS-CH:RSIO', 'SI-20M1:PS-CV:RSIO', 'SI-20M2:PS-CH:RSIO', 'SI-20M2:PS-CV:RSIO', 'SI-20C1:PS-CH:RSIO', 'SI-20C1:PS-CV:RSIO', 'SI-20C2:PS-CH:RSIO', 'SI-20C2:PS-CV-1:RSIO', 'SI-20C2:PS-CV-2:RSIO', 'SI-20C3:PS-CH:RSIO', 'SI-20C3:PS-CV-1:RSIO', 'SI-20C3:PS-CV-2:RSIO', 'SI-20C4:PS-CH:RSIO', 'SI-20C4:PS-CV:RSIO',
        ),
    },
'SI-Glob:TI-Quads:': {
    'events':('MigSI','Tunes','Study'),
    'trigger_type':'PSSI',
    'channels': (
        'SI-Fam:PS-QFA:RSIO', 'SI-Fam:PS-QDA:RSIO', 'SI-Fam:PS-QFB:RSIO', 'SI-Fam:PS-QDB1:RSIO', 'SI-Fam:PS-QDB2:RSIO', 'SI-Fam:PS-QFP:RSIO', 'SI-Fam:PS-QDP1:RSIO', 'SI-Fam:PS-QDP2:RSIO', 'SI-Fam:PS-Q1:RSIO', 'SI-Fam:PS-Q2:RSIO', 'SI-Fam:PS-Q3:RSIO', 'SI-Fam:PS-Q4:RSIO',
        'SI-Fam:PS-QB1:RSIO', 'SI-Fam:PS-QB2:RSIO',

        'SI-01C1:PS-Q1:RSIO', 'SI-01C1:PS-Q2:RSIO', 'SI-01C2:PS-Q3:RSIO', 'SI-01C2:PS-Q4:RSIO', 'SI-01C3:PS-Q4:RSIO', 'SI-01C3:PS-Q3:RSIO', 'SI-01C4:PS-Q2:RSIO', 'SI-01C4:PS-Q1:RSIO', 'SI-01M1:PS-QFA:RSIO', 'SI-01M1:PS-QDA:RSIO', 'SI-01M2:PS-QFA:RSIO', 'SI-01M2:PS-QDA:RSIO',
        'SI-05C1:PS-Q1:RSIO', 'SI-05C1:PS-Q2:RSIO', 'SI-05C2:PS-Q3:RSIO', 'SI-05C2:PS-Q4:RSIO', 'SI-05C3:PS-Q4:RSIO', 'SI-05C3:PS-Q3:RSIO', 'SI-05C4:PS-Q2:RSIO', 'SI-05C4:PS-Q1:RSIO', 'SI-05M1:PS-QFA:RSIO', 'SI-05M1:PS-QDA:RSIO', 'SI-05M2:PS-QFA:RSIO', 'SI-05M2:PS-QDA:RSIO',
        'SI-09C1:PS-Q1:RSIO', 'SI-09C1:PS-Q2:RSIO', 'SI-09C2:PS-Q3:RSIO', 'SI-09C2:PS-Q4:RSIO', 'SI-09C3:PS-Q4:RSIO', 'SI-09C3:PS-Q3:RSIO', 'SI-09C4:PS-Q2:RSIO', 'SI-09C4:PS-Q1:RSIO', 'SI-09M1:PS-QFA:RSIO', 'SI-09M1:PS-QDA:RSIO', 'SI-09M2:PS-QFA:RSIO', 'SI-09M2:PS-QDA:RSIO',
        'SI-13C1:PS-Q1:RSIO', 'SI-13C1:PS-Q2:RSIO', 'SI-13C2:PS-Q3:RSIO', 'SI-13C2:PS-Q4:RSIO', 'SI-13C3:PS-Q4:RSIO', 'SI-13C3:PS-Q3:RSIO', 'SI-13C4:PS-Q2:RSIO', 'SI-13C4:PS-Q1:RSIO', 'SI-13M1:PS-QFA:RSIO', 'SI-13M1:PS-QDA:RSIO', 'SI-13M2:PS-QFA:RSIO', 'SI-13M2:PS-QDA:RSIO',
        'SI-17C1:PS-Q1:RSIO', 'SI-17C1:PS-Q2:RSIO', 'SI-17C2:PS-Q3:RSIO', 'SI-17C2:PS-Q4:RSIO', 'SI-17C3:PS-Q4:RSIO', 'SI-17C3:PS-Q3:RSIO', 'SI-17C4:PS-Q2:RSIO', 'SI-17C4:PS-Q1:RSIO', 'SI-17M1:PS-QFA:RSIO', 'SI-17M1:PS-QDA:RSIO', 'SI-17M2:PS-QFA:RSIO', 'SI-17M2:PS-QDA:RSIO',

        'SI-02C1:PS-Q1:RSIO', 'SI-02C1:PS-Q2:RSIO', 'SI-02C2:PS-Q3:RSIO', 'SI-02C2:PS-Q4:RSIO', 'SI-02C3:PS-Q4:RSIO', 'SI-02C3:PS-Q3:RSIO', 'SI-02C4:PS-Q2:RSIO', 'SI-02C4:PS-Q1:RSIO', 'SI-02M1:PS-QFB:RSIO', 'SI-02M1:PS-QDB1:RSIO', 'SI-02M1:PS-QDB2:RSIO', 'SI-02M2:PS-QFB:RSIO', 'SI-02M2:PS-QDB1:RSIO', 'SI-02M2:PS-QDB2:RSIO',
        'SI-04C1:PS-Q1:RSIO', 'SI-04C1:PS-Q2:RSIO', 'SI-04C2:PS-Q3:RSIO', 'SI-04C2:PS-Q4:RSIO', 'SI-04C3:PS-Q4:RSIO', 'SI-04C3:PS-Q3:RSIO', 'SI-04C4:PS-Q2:RSIO', 'SI-04C4:PS-Q1:RSIO', 'SI-04M1:PS-QFB:RSIO', 'SI-04M1:PS-QDB1:RSIO', 'SI-04M1:PS-QDB2:RSIO', 'SI-04M2:PS-QFB:RSIO', 'SI-04M2:PS-QDB1:RSIO', 'SI-04M2:PS-QDB2:RSIO',
        'SI-06C1:PS-Q1:RSIO', 'SI-06C1:PS-Q2:RSIO', 'SI-06C2:PS-Q3:RSIO', 'SI-06C2:PS-Q4:RSIO', 'SI-06C3:PS-Q4:RSIO', 'SI-06C3:PS-Q3:RSIO', 'SI-06C4:PS-Q2:RSIO', 'SI-06C4:PS-Q1:RSIO', 'SI-06M1:PS-QFB:RSIO', 'SI-06M1:PS-QDB1:RSIO', 'SI-06M1:PS-QDB2:RSIO', 'SI-06M2:PS-QFB:RSIO', 'SI-06M2:PS-QDB1:RSIO', 'SI-06M2:PS-QDB2:RSIO',
        'SI-08C1:PS-Q1:RSIO', 'SI-08C1:PS-Q2:RSIO', 'SI-08C2:PS-Q3:RSIO', 'SI-08C2:PS-Q4:RSIO', 'SI-08C3:PS-Q4:RSIO', 'SI-08C3:PS-Q3:RSIO', 'SI-08C4:PS-Q2:RSIO', 'SI-08C4:PS-Q1:RSIO', 'SI-08M1:PS-QFB:RSIO', 'SI-08M1:PS-QDB1:RSIO', 'SI-08M1:PS-QDB2:RSIO', 'SI-08M2:PS-QFB:RSIO', 'SI-08M2:PS-QDB1:RSIO', 'SI-08M2:PS-QDB2:RSIO',
        'SI-10C1:PS-Q1:RSIO', 'SI-10C1:PS-Q2:RSIO', 'SI-10C2:PS-Q3:RSIO', 'SI-10C2:PS-Q4:RSIO', 'SI-10C3:PS-Q4:RSIO', 'SI-10C3:PS-Q3:RSIO', 'SI-10C4:PS-Q2:RSIO', 'SI-10C4:PS-Q1:RSIO', 'SI-10M1:PS-QFB:RSIO', 'SI-10M1:PS-QDB1:RSIO', 'SI-10M1:PS-QDB2:RSIO', 'SI-10M2:PS-QFB:RSIO', 'SI-10M2:PS-QDB1:RSIO', 'SI-10M2:PS-QDB2:RSIO',
        'SI-12C1:PS-Q1:RSIO', 'SI-12C1:PS-Q2:RSIO', 'SI-12C2:PS-Q3:RSIO', 'SI-12C2:PS-Q4:RSIO', 'SI-12C3:PS-Q4:RSIO', 'SI-12C3:PS-Q3:RSIO', 'SI-12C4:PS-Q2:RSIO', 'SI-12C4:PS-Q1:RSIO', 'SI-12M1:PS-QFB:RSIO', 'SI-12M1:PS-QDB1:RSIO', 'SI-12M1:PS-QDB2:RSIO', 'SI-12M2:PS-QFB:RSIO', 'SI-12M2:PS-QDB1:RSIO', 'SI-12M2:PS-QDB2:RSIO',
        'SI-14C1:PS-Q1:RSIO', 'SI-14C1:PS-Q2:RSIO', 'SI-14C2:PS-Q3:RSIO', 'SI-14C2:PS-Q4:RSIO', 'SI-14C3:PS-Q4:RSIO', 'SI-14C3:PS-Q3:RSIO', 'SI-14C4:PS-Q2:RSIO', 'SI-14C4:PS-Q1:RSIO', 'SI-14M1:PS-QFB:RSIO', 'SI-14M1:PS-QDB1:RSIO', 'SI-14M1:PS-QDB2:RSIO', 'SI-14M2:PS-QFB:RSIO', 'SI-14M2:PS-QDB1:RSIO', 'SI-14M2:PS-QDB2:RSIO',
        'SI-16C1:PS-Q1:RSIO', 'SI-16C1:PS-Q2:RSIO', 'SI-16C2:PS-Q3:RSIO', 'SI-16C2:PS-Q4:RSIO', 'SI-16C3:PS-Q4:RSIO', 'SI-16C3:PS-Q3:RSIO', 'SI-16C4:PS-Q2:RSIO', 'SI-16C4:PS-Q1:RSIO', 'SI-16M1:PS-QFB:RSIO', 'SI-16M1:PS-QDB1:RSIO', 'SI-16M1:PS-QDB2:RSIO', 'SI-16M2:PS-QFB:RSIO', 'SI-16M2:PS-QDB1:RSIO', 'SI-16M2:PS-QDB2:RSIO',
        'SI-18C1:PS-Q1:RSIO', 'SI-18C1:PS-Q2:RSIO', 'SI-18C2:PS-Q3:RSIO', 'SI-18C2:PS-Q4:RSIO', 'SI-18C3:PS-Q4:RSIO', 'SI-18C3:PS-Q3:RSIO', 'SI-18C4:PS-Q2:RSIO', 'SI-18C4:PS-Q1:RSIO', 'SI-18M1:PS-QFB:RSIO', 'SI-18M1:PS-QDB1:RSIO', 'SI-18M1:PS-QDB2:RSIO', 'SI-18M2:PS-QFB:RSIO', 'SI-18M2:PS-QDB1:RSIO', 'SI-18M2:PS-QDB2:RSIO',
        'SI-20C1:PS-Q1:RSIO', 'SI-20C1:PS-Q2:RSIO', 'SI-20C2:PS-Q3:RSIO', 'SI-20C2:PS-Q4:RSIO', 'SI-20C3:PS-Q4:RSIO', 'SI-20C3:PS-Q3:RSIO', 'SI-20C4:PS-Q2:RSIO', 'SI-20C4:PS-Q1:RSIO', 'SI-20M1:PS-QFB:RSIO', 'SI-20M1:PS-QDB1:RSIO', 'SI-20M1:PS-QDB2:RSIO', 'SI-20M2:PS-QFB:RSIO', 'SI-20M2:PS-QDB1:RSIO', 'SI-20M2:PS-QDB2:RSIO',

        'SI-03C1:PS-Q1:RSIO', 'SI-03C1:PS-Q2:RSIO', 'SI-03C2:PS-Q3:RSIO', 'SI-03C2:PS-Q4:RSIO', 'SI-03C3:PS-Q4:RSIO', 'SI-03C3:PS-Q3:RSIO', 'SI-03C4:PS-Q2:RSIO', 'SI-03C4:PS-Q1:RSIO', 'SI-03M1:PS-QFP:RSIO', 'SI-03M1:PS-QDP1:RSIO', 'SI-03M1:PS-QDP2:RSIO', 'SI-03M2:PS-QFP:RSIO', 'SI-03M2:PS-QDP1:RSIO', 'SI-03M2:PS-QDP2:RSIO',
        'SI-07C1:PS-Q1:RSIO', 'SI-07C1:PS-Q2:RSIO', 'SI-07C2:PS-Q3:RSIO', 'SI-07C2:PS-Q4:RSIO', 'SI-07C3:PS-Q4:RSIO', 'SI-07C3:PS-Q3:RSIO', 'SI-07C4:PS-Q2:RSIO', 'SI-07C4:PS-Q1:RSIO', 'SI-07M1:PS-QFP:RSIO', 'SI-07M1:PS-QDP1:RSIO', 'SI-07M1:PS-QDP2:RSIO', 'SI-07M2:PS-QFP:RSIO', 'SI-07M2:PS-QDP1:RSIO', 'SI-07M2:PS-QDP2:RSIO',
        'SI-11C1:PS-Q1:RSIO', 'SI-11C1:PS-Q2:RSIO', 'SI-11C2:PS-Q3:RSIO', 'SI-11C2:PS-Q4:RSIO', 'SI-11C3:PS-Q4:RSIO', 'SI-11C3:PS-Q3:RSIO', 'SI-11C4:PS-Q2:RSIO', 'SI-11C4:PS-Q1:RSIO', 'SI-11M1:PS-QFP:RSIO', 'SI-11M1:PS-QDP1:RSIO', 'SI-11M1:PS-QDP2:RSIO', 'SI-11M2:PS-QFP:RSIO', 'SI-11M2:PS-QDP1:RSIO', 'SI-11M2:PS-QDP2:RSIO',
        'SI-15C1:PS-Q1:RSIO', 'SI-15C1:PS-Q2:RSIO', 'SI-15C2:PS-Q3:RSIO', 'SI-15C2:PS-Q4:RSIO', 'SI-15C3:PS-Q4:RSIO', 'SI-15C3:PS-Q3:RSIO', 'SI-15C4:PS-Q2:RSIO', 'SI-15C4:PS-Q1:RSIO', 'SI-15M1:PS-QFP:RSIO', 'SI-15M1:PS-QDP1:RSIO', 'SI-15M1:PS-QDP2:RSIO', 'SI-15M2:PS-QFP:RSIO', 'SI-15M2:PS-QDP1:RSIO', 'SI-15M2:PS-QDP2:RSIO',
        'SI-19C1:PS-Q1:RSIO', 'SI-19C1:PS-Q2:RSIO', 'SI-19C2:PS-Q3:RSIO', 'SI-19C2:PS-Q4:RSIO', 'SI-19C3:PS-Q4:RSIO', 'SI-19C3:PS-Q3:RSIO', 'SI-19C4:PS-Q2:RSIO', 'SI-19C4:PS-Q1:RSIO', 'SI-19M1:PS-QFP:RSIO', 'SI-19M1:PS-QDP1:RSIO', 'SI-19M1:PS-QDP2:RSIO', 'SI-19M2:PS-QFP:RSIO', 'SI-19M2:PS-QDP1:RSIO', 'SI-19M2:PS-QDP2:RSIO',
        ),
    },
'SI-Glob:TI-Skews:': {
    'events':('MigSI','Coupl','Study'),
    'trigger_type':'PSSI',
    'channels': (
        'SI-01M1:PS-QS:RSIO', 'SI-01M2:PS-QS:RSIO', 'SI-01C1:PS-QS:RSIO', 'SI-01C2:PS-QS:RSIO', 'SI-01C3:PS-QS:RSIO',
        'SI-02M1:PS-QS:RSIO', 'SI-02M2:PS-QS:RSIO', 'SI-02C1:PS-QS:RSIO', 'SI-02C2:PS-QS:RSIO', 'SI-02C3:PS-QS:RSIO',
        'SI-03M1:PS-QS:RSIO', 'SI-03M2:PS-QS:RSIO', 'SI-03C1:PS-QS:RSIO', 'SI-03C2:PS-QS:RSIO', 'SI-03C3:PS-QS:RSIO',
        'SI-04M1:PS-QS:RSIO', 'SI-04M2:PS-QS:RSIO', 'SI-04C1:PS-QS:RSIO', 'SI-04C2:PS-QS:RSIO', 'SI-04C3:PS-QS:RSIO',
        'SI-05M1:PS-QS:RSIO', 'SI-05M2:PS-QS:RSIO', 'SI-05C1:PS-QS:RSIO', 'SI-05C2:PS-QS:RSIO', 'SI-05C3:PS-QS:RSIO',
        'SI-06M1:PS-QS:RSIO', 'SI-06M2:PS-QS:RSIO', 'SI-06C1:PS-QS:RSIO', 'SI-06C2:PS-QS:RSIO', 'SI-06C3:PS-QS:RSIO',
        'SI-07M1:PS-QS:RSIO', 'SI-07M2:PS-QS:RSIO', 'SI-07C1:PS-QS:RSIO', 'SI-07C2:PS-QS:RSIO', 'SI-07C3:PS-QS:RSIO',
        'SI-08M1:PS-QS:RSIO', 'SI-08M2:PS-QS:RSIO', 'SI-08C1:PS-QS:RSIO', 'SI-08C2:PS-QS:RSIO', 'SI-08C3:PS-QS:RSIO',
        'SI-09M1:PS-QS:RSIO', 'SI-09M2:PS-QS:RSIO', 'SI-09C1:PS-QS:RSIO', 'SI-09C2:PS-QS:RSIO', 'SI-09C3:PS-QS:RSIO',
        'SI-10M1:PS-QS:RSIO', 'SI-10M2:PS-QS:RSIO', 'SI-10C1:PS-QS:RSIO', 'SI-10C2:PS-QS:RSIO', 'SI-10C3:PS-QS:RSIO',
        'SI-11M1:PS-QS:RSIO', 'SI-11M2:PS-QS:RSIO', 'SI-11C1:PS-QS:RSIO', 'SI-11C2:PS-QS:RSIO', 'SI-11C3:PS-QS:RSIO',
        'SI-12M1:PS-QS:RSIO', 'SI-12M2:PS-QS:RSIO', 'SI-12C1:PS-QS:RSIO', 'SI-12C2:PS-QS:RSIO', 'SI-12C3:PS-QS:RSIO',
        'SI-13M1:PS-QS:RSIO', 'SI-13M2:PS-QS:RSIO', 'SI-13C1:PS-QS:RSIO', 'SI-13C2:PS-QS:RSIO', 'SI-13C3:PS-QS:RSIO',
        'SI-14M1:PS-QS:RSIO', 'SI-14M2:PS-QS:RSIO', 'SI-14C1:PS-QS:RSIO', 'SI-14C2:PS-QS:RSIO', 'SI-14C3:PS-QS:RSIO',
        'SI-15M1:PS-QS:RSIO', 'SI-15M2:PS-QS:RSIO', 'SI-15C1:PS-QS:RSIO', 'SI-15C2:PS-QS:RSIO', 'SI-15C3:PS-QS:RSIO',
        'SI-16M1:PS-QS:RSIO', 'SI-16M2:PS-QS:RSIO', 'SI-16C1:PS-QS:RSIO', 'SI-16C2:PS-QS:RSIO', 'SI-16C3:PS-QS:RSIO',
        'SI-17M1:PS-QS:RSIO', 'SI-17M2:PS-QS:RSIO', 'SI-17C1:PS-QS:RSIO', 'SI-17C2:PS-QS:RSIO', 'SI-17C3:PS-QS:RSIO',
        'SI-18M1:PS-QS:RSIO', 'SI-18M2:PS-QS:RSIO', 'SI-18C1:PS-QS:RSIO', 'SI-18C2:PS-QS:RSIO', 'SI-18C3:PS-QS:RSIO',
        'SI-19M1:PS-QS:RSIO', 'SI-19M2:PS-QS:RSIO', 'SI-19C1:PS-QS:RSIO', 'SI-19C2:PS-QS:RSIO', 'SI-19C3:PS-QS:RSIO',
        'SI-20M1:PS-QS:RSIO', 'SI-20M2:PS-QS:RSIO', 'SI-20C1:PS-QS:RSIO', 'SI-20C2:PS-QS:RSIO', 'SI-20C3:PS-QS:RSIO',
        ),
    },
'SI-Glob:TI-Dips:': {
    'events':('MigSI','Study'),
    'trigger_type':'PSSI',
    'channels': (
        'SI-Fam:PS-B1B2-1:RSIO', 'SI-Fam:PS-B1B2-2:RSIO',
        ),
    },
'SI-Glob:TI-Sexts:': {
    'events':('MigSI','Study'),
    'trigger_type':'PSSI',
    'channels': (
        'SI-Fam:PS-SFA0:RSIO', 'SI-Fam:PS-SFA1:RSIO', 'SI-Fam:PS-SFA2:RSIO', 'SI-Fam:PS-SDA0:RSIO', 'SI-Fam:PS-SDA1:RSIO', 'SI-Fam:PS-SDA2:RSIO', 'SI-Fam:PS-SDA3:RSIO',
        'SI-Fam:PS-SFB0:RSIO', 'SI-Fam:PS-SFB1:RSIO', 'SI-Fam:PS-SFB2:RSIO', 'SI-Fam:PS-SDB0:RSIO', 'SI-Fam:PS-SDB1:RSIO', 'SI-Fam:PS-SDB2:RSIO', 'SI-Fam:PS-SDB3:RSIO',
        'SI-Fam:PS-SFP0:RSIO', 'SI-Fam:PS-SFP1:RSIO', 'SI-Fam:PS-SFP2:RSIO', 'SI-Fam:PS-SDP0:RSIO', 'SI-Fam:PS-SDP1:RSIO', 'SI-Fam:PS-SDP2:RSIO', 'SI-Fam:PS-SDP3:RSIO',
        ),
    },
'BO-Glob:TI-Mags:': {
    'events':('RmpBO','Study'),
    'trigger_type':'rmpbo',
    'channels': (
        'BO-Fam:PS-B-1:RSIO', 'BO-Fam:PS-B-2:RSIO',
        'BO-Fam:PS-QF:RSIO', 'BO-Fam:PS-QD:RSIO',
        'BO-Fam:PS-SF:RSIO', 'BO-Fam:PS-SD:RSIO',
        'BO-01U:PS-CH:RSIO', 'BO-01U:PS-CV:RSIO', 'BO-03U:PS-CH:RSIO', 'BO-03U:PS-CV:RSIO', 'BO-05U:PS-CH:RSIO', 'BO-05U:PS-CV:RSIO', 'BO-07U:PS-CH:RSIO', 'BO-07U:PS-CV:RSIO', 'BO-09U:PS-CH:RSIO', 'BO-09U:PS-CV:RSIO',
        'BO-11U:PS-CH:RSIO', 'BO-11U:PS-CV:RSIO', 'BO-13U:PS-CH:RSIO', 'BO-13U:PS-CV:RSIO', 'BO-15U:PS-CH:RSIO', 'BO-15U:PS-CV:RSIO', 'BO-17U:PS-CH:RSIO', 'BO-17U:PS-CV:RSIO', 'BO-19U:PS-CH:RSIO', 'BO-19U:PS-CV:RSIO',
        'BO-21U:PS-CH:RSIO', 'BO-21U:PS-CV:RSIO', 'BO-23U:PS-CH:RSIO', 'BO-23U:PS-CV:RSIO', 'BO-25U:PS-CH:RSIO', 'BO-25U:PS-CV:RSIO', 'BO-27U:PS-CH:RSIO', 'BO-27U:PS-CV:RSIO', 'BO-29U:PS-CH:RSIO', 'BO-29U:PS-CV:RSIO',
        'BO-31U:PS-CH:RSIO', 'BO-31U:PS-CV:RSIO', 'BO-33U:PS-CH:RSIO', 'BO-33U:PS-CV:RSIO', 'BO-35U:PS-CH:RSIO', 'BO-35U:PS-CV:RSIO', 'BO-37U:PS-CH:RSIO', 'BO-37U:PS-CV:RSIO', 'BO-39U:PS-CH:RSIO', 'BO-39U:PS-CV:RSIO',
        'BO-41U:PS-CH:RSIO', 'BO-41U:PS-CV:RSIO', 'BO-43U:PS-CH:RSIO', 'BO-43U:PS-CV:RSIO', 'BO-45U:PS-CH:RSIO', 'BO-45U:PS-CV:RSIO', 'BO-47U:PS-CH:RSIO', 'BO-47U:PS-CV:RSIO', 'BO-49U:PS-CH:RSIO', 'BO-49U:PS-CV:RSIO',
        'BO-02D:PS-QS:RSIO',
        ),
    },
'LI-01:TI-EGun:MultBun':{
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:EGun-Trig-1:HVEI',
        ),
    },
'LI-01:TI-EGun:SglBun':{
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:EGun-Trig-2:HVEI',
        ),
    },
'LI-01:TI-Modltr-1:': {
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:RF-Modltr-1:HVEI',
        ),
    },
'LI-01:TI-Modltr-2:': {
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:RF-Modltr-2:HVEI',
        ),
    },
'LI-Glob:TI-SHAmp:': {
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:RF-SSA-1:HVEI',
        ),
    },
'LI-Glob:TI-RFAmp-1:': {
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:RF-SSA-2:HVEI',
        ),
    },
'LI-Glob:TI-RFAmp-2:': {
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:RF-SSA-3:HVEI',
        ),
    },
'LI-Glob:TI-LLRF-1:': {
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:RF-LLRF-1:HVEI',
        ),
    },
'LI-Glob:TI-LLRF-2:': {
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:RF-LLRF-2:HVEI',
        ),
    },
'LI-Glob:TI-LLRF-3:': {
    'events':('Linac','Study'),
    'trigger_type':'simple',
    'channels':(
        'LI-01:RF-LLRF-3:HVEI',
        ),
    },
'TB-04:TI-InjS:': {
    'events':('InjBO','Study'),
    'trigger_type':'simple',
    'channels':(
        'TB-04:PU-InjS:HVEI',
        ),
    },
'BO-01D:TI-InjK:': {
    'events':('InjBO','Study'),
    'trigger_type':'simple',
    'channels':(
        'BO-01D:PU-InjK:HVEI',
        ),
    },
'BO-05D:TI-P5Cav:': {
    'events':('InjBO','RmpBO','Study'),
    'trigger_type':'cavity',
    'channels':(
        'BO-05D:RF-P5Cav:HVEI',
        ),
    },
'BO-48D:TI-EjeK:': {
    'events':('InjSI','Study'),
    'trigger_type':'simple',
    'channels':(
        'BO-48D:PU-EjeK:HVEI',
        ),
    },
'TS-01:TI-EjeSF:': {
    'events':('InjSI','Study'),
    'trigger_type':'simple',
    'channels':(
        'TS-01:PU-EjeSF:HVEI',
        ),
    },
'TS-01:TI-EjeSG:': {
    'events':('InjSI','Study'),
    'trigger_type':'simple',
    'channels':(
        'TS-01:PU-EjeSG:HVEI',
        ),
    },
'TS-Fam:TI-InjSG:': {
    'events':('InjSI','Study'),
    'trigger_type':'simple',
    'channels':(
        'TS-Fam:PU-InjSG:HVEI',
        ),
    },
'TS-04:TI-InjSF:': {
    'events':('InjSI','Study'),
    'trigger_type':'simple',
    'channels':(
        'TS-04:PU-InjSF:HVEI',
        ),
    },
'SI-01SA:TI-InjK:': {
    'events':('InjSI','Study'),
    'trigger_type':'simple',
    'channels':(
        'SI-01SA:PU-InjK:HVEI',
        ),
    },
'LI-Fam:TI-BPM:': {
    'events':('DigLI','Study'),
    'trigger_type':'generic',
    'channels':(
        'LI-Fam:DI-BPM:LVEI',
        ),
    },
'LI-Fam:TI-Scrn:': {
    'events':('DigLI','Study'),
    'trigger_type':'generic',
    'channels':(
        'LI-Fam:DI-Scrn:LVEI',
        ),
    },
'LI-01:TI-ICT-1:': {
    'events':('DigLI','Study'),
    'trigger_type':'generic',
    'channels':(
        'LI-01:DI-ICT-1:LVEI',
        ),
    },
'LI-01:TI-ICT-2:': {
    'events':('DigLI','Study'),
    'trigger_type':'generic',
    'channels':(
        'LI-01:DI-ICT-2:LVEI',
        ),
    },
'TB-Fam:TI-BPM:': {
    'events':('DigTB','Study'),
    'trigger_type':'generic',
    'channels':(
        'TB-01:DI-BPM-1:LVEIO7', 'TB-01:DI-BPM-2:LVEIO7', 'TB-02:DI-BPM-1:LVEIO7',  'TB-02:DI-BPM-2:LVEIO7',  'TB-03:DI-BPM:LVEIO7',  'TB-04:DI-BPM:LVEIO7',
        ),
    },
'TB-Fam:TI-Scrn:': {
    'events':('DigTB','Study'),
    'trigger_type':'generic',
    'channels':(
        'TB-01:DI-Scrn-1:LVEI', 'TB-01:DI-Scrn-2:LVEI', 'TB-02:DI-Scrn-1:LVEI',  'TB-02:DI-Scrn-2:LVEI',  'TB-03:DI-Scrn:LVEI',  'TB-04:DI-Scrn:LVEI',
        ),
    },
'TB-02:TI-ICT:': {
    'events':('DigTB','Study'),
    'trigger_type':'generic',
    'channels':(
        'TB-02:DI-ICT:LVEI',
        ),
    },
'TB-04:TI-ICT:': {
    'events':('DigTB','Study'),
    'trigger_type':'generic',
    'channels':(
        'TB-04:DI-ICT:LVEI',
        ),
    },
'TB-04:TI-FCT:': {
    'events':('DigTB','Study'),
    'trigger_type':'generic',
    'channels':(
        'TB-04:DI-FCT:LVEI',
        ),
    },
'BO-Fam:TI-BPM:': {
    'events':('DigBO','Study'),
    'trigger_type':'generic',
    'channels':(
        'BO-01U:DI-BPM:LVEIO7', 'BO-02U:DI-BPM:LVEIO7', 'BO-03U:DI-BPM:LVEIO7', 'BO-04U:DI-BPM:LVEIO7', 'BO-05U:DI-BPM:LVEIO7', 'BO-06U:DI-BPM:LVEIO7', 'BO-07U:DI-BPM:LVEIO7', 'BO-08U:DI-BPM:LVEIO7', 'BO-09U:DI-BPM:LVEIO7', 'BO-10U:DI-BPM:LVEIO7',
        'BO-11U:DI-BPM:LVEIO7', 'BO-12U:DI-BPM:LVEIO7', 'BO-13U:DI-BPM:LVEIO7', 'BO-14U:DI-BPM:LVEIO7', 'BO-15U:DI-BPM:LVEIO7', 'BO-16U:DI-BPM:LVEIO7', 'BO-17U:DI-BPM:LVEIO7', 'BO-18U:DI-BPM:LVEIO7', 'BO-19U:DI-BPM:LVEIO7', 'BO-20U:DI-BPM:LVEIO7',
        'BO-21U:DI-BPM:LVEIO7', 'BO-22U:DI-BPM:LVEIO7', 'BO-23U:DI-BPM:LVEIO7', 'BO-24U:DI-BPM:LVEIO7', 'BO-25U:DI-BPM:LVEIO7', 'BO-26U:DI-BPM:LVEIO7', 'BO-27U:DI-BPM:LVEIO7', 'BO-28U:DI-BPM:LVEIO7', 'BO-29U:DI-BPM:LVEIO7', 'BO-30U:DI-BPM:LVEIO7',
        'BO-31U:DI-BPM:LVEIO7', 'BO-32U:DI-BPM:LVEIO7', 'BO-33U:DI-BPM:LVEIO7', 'BO-34U:DI-BPM:LVEIO7', 'BO-35U:DI-BPM:LVEIO7', 'BO-36U:DI-BPM:LVEIO7', 'BO-37U:DI-BPM:LVEIO7', 'BO-38U:DI-BPM:LVEIO7', 'BO-39U:DI-BPM:LVEIO7', 'BO-40U:DI-BPM:LVEIO7',
        'BO-41U:DI-BPM:LVEIO7', 'BO-42U:DI-BPM:LVEIO7', 'BO-43U:DI-BPM:LVEIO7', 'BO-44U:DI-BPM:LVEIO7', 'BO-45U:DI-BPM:LVEIO7', 'BO-46U:DI-BPM:LVEIO7', 'BO-47U:DI-BPM:LVEIO7', 'BO-48U:DI-BPM:LVEIO7', 'BO-49U:DI-BPM:LVEIO7', 'BO-50U:DI-BPM:LVEIO7',
        ),
    },
'BO-Fam:TI-Scrn:': {
    'events':('DigBO','Study'),
    'trigger_type':'generic',
    'channels':(
        'BO-01D:DI-Scrn-1:LVEI', 'BO-01D:DI-Scrn-2:LVEI', 'BO-02U:DI-Scrn:LVEI',
        ),
    },
'BO-04U:TI-GSL:': {
    'events':('DigBO','Study'),
    'trigger_type':'generic',
    'channels':(
        'BO-04U:DI-GSL:LVEI',
        ),
    },
'BO-02D:TI-TuneS:': {
    'events':('DigBO','Study'),
    'trigger_type':'generic',
    'channels':(
        'BO-02D:DI-TuneS:LVEI',
        ),
    },
'BO-04D:TI-TuneP:': {
    'events':('DigBO','Study'),
    'trigger_type':'generic',
    'channels':(
        'BO-04D:DI-TuneP:LVEI',
        ),
    },
'BO-35D:TI-DCCT:': {
    'events':('DigBO','Study'),
    'trigger_type':'generic',
    'channels':(
        'BO-35D:DI-DCCT:LVEI',
        ),
    },
'TS-Fam:TI-BPM:': {
    'events':('DigTS','Study'),
    'trigger_type':'generic',
    'channels':(
        'TS-01:DI-BPM:LVEIO6', 'TS-02:DI-BPM:LVEIO6',  'TS-03:DI-BPM:LVEIO6',  'TS-04:DI-BPM-1:LVEIO6', 'TS-04:DI-BPM-2:LVEIO6',
        ),
    },
'TS-Fam:TI-Scrn:': {
    'events':('DigTS','Study'),
    'trigger_type':'generic',
    'channels':(
        'TS-01:DI-Scrn:LVEI', 'TS-02:DI-Scrn:LVEI',  'TS-03:DI-Scrn:LVEI',  'TS-04:DI-Scrn-1:LVEI', 'TS-04:DI-Scrn-2:LVEI', 'TS-04:DI-Scrn-3:LVEI',
        ),
    },
'TS-01:TI-ICT:': {
    'events':('DigTS','Study'),
    'trigger_type':'generic',
    'channels':(
        'TS-01:DI-ICT:LVEI',
        ),
    },
'TS-04:TI-ICT:': {
    'events':('DigTS','Study'),
    'trigger_type':'generic',
    'channels':(
        'TS-04:DI-ICT:LVEI',
        ),
    },
'TS-04:TI-FCT:': {
    'events':('DigTS','Study'),
    'trigger_type':'generic',
    'channels':(
        'TS-04:DI-FCT:LVEI',
        ),
    },
'SI-19SP:TI-GSL15:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-19SP:DI-GSL15:LVEI',
        ),
    },
'SI-20SB:TI-GSL07:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-20SB:DI-GSL07:LVEI',
        ),
    },
'SI-13C4:TI-DCCT:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-13C4:DI-DCCT:LVEI',
        ),
    },
'SI-14C4:TI-DCCT:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-14C4:DI-DCCT:LVEI',
        ),
    },
'SI-01SA:TI-HTuneS:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-01SA:DI-HTuneS:LVEI',
        ),
    },
'SI-17SA:TI-HTuneP:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-17SA:DI-HTuneP:LVEI',
        ),
    },
'SI-18C4:TI-VTuneS:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-18C4:DI-VTuneS:LVEI',
        ),
    },
'SI-17C4:TI-VTuneP:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-17C4:DI-VTuneP:LVEI',
        ),
    },
'SI-19C4:TI-VPing:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-19C4:PU-VPing:HVEI',
        ),
    },
'SI-01SA:TI-HPing:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-01SA:PU-HPing:HVEI',
        ),
    },
'SI-16C4:TI-GBPM:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-16C4:DI-GBPM:LVEIO5',
        ),
    },
'SI-Fam:TI-BPM:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-01M1:DI-BPM:LVEIO6', 'SI-01M2:DI-BPM:LVEIO6', 'SI-01C1:DI-BPM-1:LVEIO6', 'SI-01C1:DI-BPM-2:LVEIO6', 'SI-01C2:DI-BPM:LVEIO6', 'SI-01C3:DI-BPM-1:LVEIO6', 'SI-01C3:DI-BPM-2:LVEIO6', 'SI-01C4:DI-BPM:LVEIO6',
        'SI-02M1:DI-BPM:LVEIO6', 'SI-02M2:DI-BPM:LVEIO6', 'SI-02C1:DI-BPM-1:LVEIO6', 'SI-02C1:DI-BPM-2:LVEIO6', 'SI-02C2:DI-BPM:LVEIO6', 'SI-02C3:DI-BPM-1:LVEIO6', 'SI-02C3:DI-BPM-2:LVEIO6', 'SI-02C4:DI-BPM:LVEIO6',
        'SI-03M1:DI-BPM:LVEIO6', 'SI-03M2:DI-BPM:LVEIO6', 'SI-03C1:DI-BPM-1:LVEIO6', 'SI-03C1:DI-BPM-2:LVEIO6', 'SI-03C2:DI-BPM:LVEIO6', 'SI-03C3:DI-BPM-1:LVEIO6', 'SI-03C3:DI-BPM-2:LVEIO6', 'SI-03C4:DI-BPM:LVEIO6',
        'SI-04M1:DI-BPM:LVEIO6', 'SI-04M2:DI-BPM:LVEIO6', 'SI-04C1:DI-BPM-1:LVEIO6', 'SI-04C1:DI-BPM-2:LVEIO6', 'SI-04C2:DI-BPM:LVEIO6', 'SI-04C3:DI-BPM-1:LVEIO6', 'SI-04C3:DI-BPM-2:LVEIO6', 'SI-04C4:DI-BPM:LVEIO6',
        'SI-05M1:DI-BPM:LVEIO6', 'SI-05M2:DI-BPM:LVEIO6', 'SI-05C1:DI-BPM-1:LVEIO6', 'SI-05C1:DI-BPM-2:LVEIO6', 'SI-05C2:DI-BPM:LVEIO6', 'SI-05C3:DI-BPM-1:LVEIO6', 'SI-05C3:DI-BPM-2:LVEIO6', 'SI-05C4:DI-BPM:LVEIO6',
        'SI-06M1:DI-BPM:LVEIO6', 'SI-06M2:DI-BPM:LVEIO6', 'SI-06C1:DI-BPM-1:LVEIO6', 'SI-06C1:DI-BPM-2:LVEIO6', 'SI-06C2:DI-BPM:LVEIO6', 'SI-06C3:DI-BPM-1:LVEIO6', 'SI-06C3:DI-BPM-2:LVEIO6', 'SI-06C4:DI-BPM:LVEIO6',
        'SI-07M1:DI-BPM:LVEIO6', 'SI-07M2:DI-BPM:LVEIO6', 'SI-07C1:DI-BPM-1:LVEIO6', 'SI-07C1:DI-BPM-2:LVEIO6', 'SI-07C2:DI-BPM:LVEIO6', 'SI-07C3:DI-BPM-1:LVEIO6', 'SI-07C3:DI-BPM-2:LVEIO6', 'SI-07C4:DI-BPM:LVEIO6',
        'SI-08M1:DI-BPM:LVEIO6', 'SI-08M2:DI-BPM:LVEIO6', 'SI-08C1:DI-BPM-1:LVEIO6', 'SI-08C1:DI-BPM-2:LVEIO6', 'SI-08C2:DI-BPM:LVEIO6', 'SI-08C3:DI-BPM-1:LVEIO6', 'SI-08C3:DI-BPM-2:LVEIO6', 'SI-08C4:DI-BPM:LVEIO6',
        'SI-09M1:DI-BPM:LVEIO6', 'SI-09M2:DI-BPM:LVEIO6', 'SI-09C1:DI-BPM-1:LVEIO6', 'SI-09C1:DI-BPM-2:LVEIO6', 'SI-09C2:DI-BPM:LVEIO6', 'SI-09C3:DI-BPM-1:LVEIO6', 'SI-09C3:DI-BPM-2:LVEIO6', 'SI-09C4:DI-BPM:LVEIO6',
        'SI-10M1:DI-BPM:LVEIO6', 'SI-10M2:DI-BPM:LVEIO6', 'SI-10C1:DI-BPM-1:LVEIO6', 'SI-10C1:DI-BPM-2:LVEIO6', 'SI-10C2:DI-BPM:LVEIO6', 'SI-10C3:DI-BPM-1:LVEIO6', 'SI-10C3:DI-BPM-2:LVEIO6', 'SI-10C4:DI-BPM:LVEIO6',
        'SI-11M1:DI-BPM:LVEIO6', 'SI-11M2:DI-BPM:LVEIO6', 'SI-11C1:DI-BPM-1:LVEIO6', 'SI-11C1:DI-BPM-2:LVEIO6', 'SI-11C2:DI-BPM:LVEIO6', 'SI-11C3:DI-BPM-1:LVEIO6', 'SI-11C3:DI-BPM-2:LVEIO6', 'SI-11C4:DI-BPM:LVEIO6',
        'SI-12M1:DI-BPM:LVEIO6', 'SI-12M2:DI-BPM:LVEIO6', 'SI-12C1:DI-BPM-1:LVEIO6', 'SI-12C1:DI-BPM-2:LVEIO6', 'SI-12C2:DI-BPM:LVEIO6', 'SI-12C3:DI-BPM-1:LVEIO6', 'SI-12C3:DI-BPM-2:LVEIO6', 'SI-12C4:DI-BPM:LVEIO6',
        'SI-13M1:DI-BPM:LVEIO6', 'SI-13M2:DI-BPM:LVEIO6', 'SI-13C1:DI-BPM-1:LVEIO6', 'SI-13C1:DI-BPM-2:LVEIO6', 'SI-13C2:DI-BPM:LVEIO6', 'SI-13C3:DI-BPM-1:LVEIO6', 'SI-13C3:DI-BPM-2:LVEIO6', 'SI-13C4:DI-BPM:LVEIO6',
        'SI-14M1:DI-BPM:LVEIO6', 'SI-14M2:DI-BPM:LVEIO6', 'SI-14C1:DI-BPM-1:LVEIO6', 'SI-14C1:DI-BPM-2:LVEIO6', 'SI-14C2:DI-BPM:LVEIO6', 'SI-14C3:DI-BPM-1:LVEIO6', 'SI-14C3:DI-BPM-2:LVEIO6', 'SI-14C4:DI-BPM:LVEIO6',
        'SI-15M1:DI-BPM:LVEIO6', 'SI-15M2:DI-BPM:LVEIO6', 'SI-15C1:DI-BPM-1:LVEIO6', 'SI-15C1:DI-BPM-2:LVEIO6', 'SI-15C2:DI-BPM:LVEIO6', 'SI-15C3:DI-BPM-1:LVEIO6', 'SI-15C3:DI-BPM-2:LVEIO6', 'SI-15C4:DI-BPM:LVEIO6',
        'SI-16M1:DI-BPM:LVEIO6', 'SI-16M2:DI-BPM:LVEIO6', 'SI-16C1:DI-BPM-1:LVEIO6', 'SI-16C1:DI-BPM-2:LVEIO6', 'SI-16C2:DI-BPM:LVEIO6', 'SI-16C3:DI-BPM-1:LVEIO6', 'SI-16C3:DI-BPM-2:LVEIO6', 'SI-16C4:DI-BPM:LVEIO6',
        'SI-17M1:DI-BPM:LVEIO6', 'SI-17M2:DI-BPM:LVEIO6', 'SI-17C1:DI-BPM-1:LVEIO6', 'SI-17C1:DI-BPM-2:LVEIO6', 'SI-17C2:DI-BPM:LVEIO6', 'SI-17C3:DI-BPM-1:LVEIO6', 'SI-17C3:DI-BPM-2:LVEIO6', 'SI-17C4:DI-BPM:LVEIO6',
        'SI-18M1:DI-BPM:LVEIO6', 'SI-18M2:DI-BPM:LVEIO6', 'SI-18C1:DI-BPM-1:LVEIO6', 'SI-18C1:DI-BPM-2:LVEIO6', 'SI-18C2:DI-BPM:LVEIO6', 'SI-18C3:DI-BPM-1:LVEIO6', 'SI-18C3:DI-BPM-2:LVEIO6', 'SI-18C4:DI-BPM:LVEIO6',
        'SI-19M1:DI-BPM:LVEIO6', 'SI-19M2:DI-BPM:LVEIO6', 'SI-19C1:DI-BPM-1:LVEIO6', 'SI-19C1:DI-BPM-2:LVEIO6', 'SI-19C2:DI-BPM:LVEIO6', 'SI-19C3:DI-BPM-1:LVEIO6', 'SI-19C3:DI-BPM-2:LVEIO6', 'SI-19C4:DI-BPM:LVEIO6',
        'SI-20M1:DI-BPM:LVEIO6', 'SI-20M2:DI-BPM:LVEIO6', 'SI-20C1:DI-BPM-1:LVEIO6', 'SI-20C1:DI-BPM-2:LVEIO6', 'SI-20C2:DI-BPM:LVEIO6', 'SI-20C3:DI-BPM-1:LVEIO6', 'SI-20C3:DI-BPM-2:LVEIO6', 'SI-20C4:DI-BPM:LVEIO6',
        ),
    },
'SI-Glob:TI-BbB:': {
    'events':('DigSI','Study'),
    'trigger_type':'generic',
    'channels':(
        'SI-Glob:DI-BbB:LVEI',
        ),
    },
}

def get_triggers():
    return _copy.deepcopy(_TRIGGERS)