
MPS_PREFIX = 'LA-CN:H1MPS-1:'

SEC_2_POS = {
    'General': (1, 0, 2, 1),
    'Egun': (1, 1, 1, 1),
    'Modulators': (2, 1, 1, 1),
    'Klystrons': (3, 0, 1, 2),
    'VA': (5, 0, 1, 2),
    'Compressed Air': (6, 0, 1, 1),
    'Water Conductivity': (6, 1, 1, 1),
    'Water': (7, 0, 1, 2),
}

SEC_2_STATUS = {
    'General': {
        'MPS Heartbeat': ('HeartBeat', 0),
        'MPS Alarm': ('LAAlarm', 1),
        'MPS Warn': ('LAWarn', 1),
        'PPS - Gate': ('PPState7_L', 0),
        'PPS - Dose': ('PPState8_L', 0),
        'BS and SR Intlk 1': ('BSState1_L', 0),
        'BS and SR Intlk 2': ('BSState2_L', 0),
        'Emergency 1': ('Emergency1_L', 0),
        'Emergency 2': ('Emergency2_L', 0),
    },
    'Egun': {
        'Trigger Permit': ('GunPermit', 1),
        'Vacuum Alarm': ('GunVacState', 1),
        'Gate Valve': ('GunGvalState', 1),
    },
    'Modulators': {
        'Header': ['Status', 'Trigger\nPermit'],
        'Mod 1':  [('Mod1State_L', 0), ('Mod1Permit', 1)],
        'Mod 2':  [('Mod2State_L', 0), ('Mod2Permit', 1)],
    },
    'Klystrons': {
        'Header':     ['Status', 'Oil-tank\nWT alarm', 'Focus-coil\nWT alarm',
                       'Refl. PW\nIntlk'],
        'Klystron 1': [('K1PsState_L', 0), ('K1TempState1', 1),
                       ('K1TempState2', 1),
                       ('LA-RF:LLRF:KLY1:GET_INTERLOCK', 0)],
        'Klystron 2': [('K2PsState_L', 0), ('K2TempState1', 1),
                       ('K2TempState2', 1),
                       ('LA-RF:LLRF:KLY2:GET_INTERLOCK', 0)],
    },
    'VA': {
        'Header':  ['IP\nWarn',         'CCG\nWarn',         'CCG\nAlarm',
                    'PRG\nWarn'],
        'EGUN':    [('IP1Warn_L', 0),  ('CCG1Warn_L', 0),  ('CCG1Alarm_L', 0),
                    ('PRG1Warn_L', 0)],
        'SBUN':    [('IP2Warn_L', 0),  ('CCG2Warn_L', 0),  ('CCG2Alarm_L', 0),
                    ''],
        'A0WG':    [('IP5Warn_L', 0),  ('CCG4Warn_L', 0),  ('CCG4Alarm_L', 0),
                    ''],
        'K1-A0WG': [('IP6Warn_L', 0),  '', '', ''],
        'A1WG':    [('IP7Warn_L', 0),  '', '', ''],
        'K1-A1WG': [('IP8Warn_L', 0),  ('CCG5Warn_L', 0),  ('CCG5Alarm_L', 0),
                    ''],
        'A2WG':    [('IP9Warn_L', 0),  ('CCG6Warn_L', 0),  ('CCG6Alarm_L', 0),
                    ('PRG3Warn_L', 0)],
        'K1-A2WG': [('IP10Warn_L', 0), '',  '', ''],
        'K1':      [('IP11Warn_L', 0), ('CCG7Warn_L', 0),  ('CCG7Alarm_L', 0),
                    ('PRG4Warn_L', 0)],
        'A3WG':    [('IP12Warn_L', 0), '', '', ''],
        'K2-A3WG': [('IP13Warn_L', 0), ('CCG8Warn_L', 0),  ('CCG8Warn_L', 0),
                    ''],
        'A4WG':    [('IP14Warn_L', 0), ('CCG9Warn_L', 0),  ('CCG9Alarm_L', 0),
                    ''],
        'K2-A4WG': [('IP15Warn_L', 0), '', '', ''],
        'K2':      [('IP16Warn_L', 0), ('CCG10Warn_L', 0), ('CCG10Alarm_L', 0),
                    ('PRG5Warn_L', 0)],
        'A4END':   [('IP3Warn_L', 0),  '', '', ''],
        'BEND':    [('IP4Warn_L', 0),  ('CCG3Warn_L', 0),  ('CCG3Alarm_L', 0),
                    ('PRG2Warn_L', 0)],
    },
    'Compressed Air': [[('GPS1_L', 0), ], ],
    'Water Conductivity': [[('WaterState_L', 0), ], ],
    'Water': [
        [('WFS1_L', 0), ('WFS2_L', 0), ('WFS3_L', 0), ('WFS4_L', 0)],
        [('WFS5_L', 0), ('WFS6_L', 0), ('WFS7_L', 0), ('WFS8_L', 0)],
        [('WFS9_L', 0), ('WFS10_L', 0), ('WFS11_L', 0), ('WFS12_L', 0)],
        [('WFS13_L', 0), ('WFS14_L', 0), ('WFS15_L', 0), ('WFS16_L', 0)]
    ],
}
