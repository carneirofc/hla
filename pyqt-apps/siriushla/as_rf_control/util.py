
SEC_2_CHANNELS = {
    'BO': {
        'Emergency': 'BO-05D:RF-Intlk:EStop-Mon',
        'Sirius Intlk': 'BO-05D:RF-Intlk:BO-Mon',
        'LLRF Intlk': 'BO-05D:RF-LLRF:Status-Mon',
        'Intlk Details': {
            'Input': {
                'PV': 'BR-RF-DLLRF-01:Intlk-Mon',
                'Labels': (
                    'Rev Out SSA',
                    'Not Used (RevSSA2)',
                    'Not Used (RefSSA3)',
                    'Not Used (RevSSA4)',
                    'Rev Cavity',
                    'Not Used (Ext LLRF1)',
                    'Not Used (Ext LLRF2)',
                    'Not Used (Ext LLRF3)',
                    'Manual',
                    'PLC',
                    'Plunger 1 End Sw Up',
                    'Plunger 1 End Sw Down',
                    'Plunger 2 End Sw Up',
                    'Plunger 2 End Sw Down',
                ),
            },
            'Fast Input': {
                'PV': 'BR-RF-DLLRF-01:FASTINLK-MON',
                'Labels': (
                    'Cavity Voltage',
                    'Cavity Fwd',
                    'SSA 1 Out Fwd',
                    'Cell 2 Voltage (RFIN7)',
                    'Cell 4 Voltage (RFIN8)',
                    'Cell 1 Voltage (RFIN9)',
                    'Cell 5 Voltage (RFIN10)',
                    'Pre-Drive In (RFIN11)',
                    'Pre-Drive Out Fwd (RFIN12)',
                    'Pre-Drive Out Rev (RFIN13)',
                    'Circulator Out Fwd (RFIN14)',
                    'Circulator Out Rev (RFIN15)',
                    'LLRF Beam Trip',
                ),
            }
        },
        'Reset': {
            'Global': 'BO-05D:RF-Intlk:Reset-Sel',
            'LLRF': 'BR-RF-DLLRF-01:Reset-Cmd',
        },
        'Cav Sts': {
            'Geral': 'BO-05D:RF-P5Cav:Sts-Mon',
            'Temp': {
                'Cells': (
                    ('BO-05D:RF-P5Cav:Cylin1T-Mon', 'blue'),
                    ('BO-05D:RF-P5Cav:Cylin2T-Mon', 'red'),
                    ('BO-05D:RF-P5Cav:Cylin3T-Mon', 'darkGreen'),
                    ('BO-05D:RF-P5Cav:Cylin4T-Mon', 'magenta'),
                    ('BO-05D:RF-P5Cav:Cylin5T-Mon', 'darkCyan'),
                ),
                'Coupler': ('BO-05D:RF-P5Cav:CoupT-Mon', 'black'),
                'Discs': (
                    'BO-05D:RF-P5Cav:Disc1Tms-Mon',
                    'BO-05D:RF-P5Cav:Disc2Tms-Mon',
                    'BO-05D:RF-P5Cav:Disc3Tms-Mon',
                    'BO-05D:RF-P5Cav:Disc4Tms-Mon',
                    'BO-05D:RF-P5Cav:Disc5Tms-Mon',
                    'BO-05D:RF-P5Cav:Disc6Tms-Mon',
                ),
            },
            'FlwRt': (
                'BO-05D:RF-P5Cav:Hd1FlwRt-Mon',
                'BO-05D:RF-P5Cav:Hd2FlwRt-Mon',
                'BO-05D:RF-P5Cav:Hd3FlwRt-Mon',
            ),
            'Vac': {
                'Cells': 'BO-05D:VA-CCG-RFC:Pressure-Mon',
                'Cond': 'BR-RF-DLLRF-01:VACUUM',
                'Cells ok': 'BO-05D:RF-P5Cav:Pressure-Mon',
                'Coupler ok': 'BO-05D:RF-P5Cav:CoupPressure-Mon',
            }
        },
        'TL Sts': {
            'Geral': 'RA-TL:RF-TrLine-BO:Sts-Mon',
            'Circ TIn': 'RA-TL:RF-Circulator-BO:Tin-Mon',
            'Circ TOut': 'RA-TL:RF-Circulator-BO:Tout-Mon',
            'Circ Arc': 'RA-TL:RF-Circulator-BO:Arc-Mon',
            'Circ FlwRt': 'RA-TL:RF-Circulator-BO:FlwRt-Mon',
            'Load FlwRt': 'RA-TL:RF-Load-BO:FlwRt-Mon',
            'Circ Intlk': 'RA-TL:RF-Circulator-BO:IntlkOp-Mon',
        },
        'SSA': {
            'Name': 'SSA',
            'Status': 'RA-ToBO:RF-SSAmpTower:Sts-Mon',
            'Power': 'RA-ToBO:RF-SSAmpTower:PwrFwdOutLLRF-Mon',
            'SRC 1': {
                'Label': '300VDC',
                'PV': 'RA-ToBO:RF-ACDCPanel:300Vdc-Sts',
            },
            'SRC 2': {
                'Label': 'DC/DC',
                'PV': 'RA-ToBO:RF-SSAmpTower:PwrCnv-Sts',
            },
            'PinSw': 'RA-RaBO01:RF-LLRFPreAmp:PinSw-Mon',
            'PreDrive': 'BR-RF-DLLRF-01:INPRE:AMP',
        },
        'SL': {
            'Enbl': 'BR-RF-DLLRF-01:SL',
            'Mode': 'BR-RF-DLLRF-01:MODE',
            'IRef': 'BR-RF-DLLRF-01:I:SL:REF',
            'QRef': 'BR-RF-DLLRF-01:Q:SL:REF',
            'ARef': 'BR-RF-DLLRF-01:SL:REF:AMP',
            'PRef': 'BR-RF-DLLRF-01:SL:REF:PHS',
            'IInp': 'BR-RF-DLLRF-01:I:SL:INP',
            'QInp': 'BR-RF-DLLRF-01:Q:SL:INP',
            'AInp': 'BR-RF-DLLRF-01:SL:INP:AMP',
            'PInp': 'BR-RF-DLLRF-01:SL:INP:PHS',
            'IErr': 'BR-RF-DLLRF-01:I:SL:ERR',
            'QErr': 'BR-RF-DLLRF-01:Q:SL:ERR',
            'AErr': 'BR-RF-DLLRF-01:SL:ERR:AMP',
            'PErr': 'BR-RF-DLLRF-01:SL:ERR:PHS',
            'ASet': 'BR-RF-DLLRF-01:mV:AL:REF',
            'PSet': 'BR-RF-DLLRF-01:PL:REF',
            'AInc': 'BR-RF-DLLRF-01:AMPREF:INCRATE',
            'PInc': 'BR-RF-DLLRF-01:PHSREF:INCRATE',
        },
        'Tun': {
            'Auto': 'BR-RF-DLLRF-01:TUNE',
            'DTune': 'BR-RF-DLLRF-01:DTune-RB',
            'DPhase': 'BR-RF-DLLRF-01:TUNE:DEPHS',
            'Pl1Down': 'BR-RF-DLLRF-01:PLG1:MOVE:DN',
            'Pl1Up': 'BR-RF-DLLRF-01:PLG1:MOVE:UP',
            'Pl2Down': 'BR-RF-DLLRF-01:PLG2:MOVE:DN',
            'Pl2Up': 'BR-RF-DLLRF-01:PLG2:MOVE:UP',
            'PlM1Curr': 'RA-RaBO01:RF-CavPlDrivers:Dr1Current-Mon',
            'PlM2Curr': 'RA-RaBO01:RF-CavPlDrivers:Dr2Current-Mon',
        },
        'PwrMtr': [
            ['Cavity Power', 'BO-05D:RF-P5Cav:Cell3Pwr-Mon',
             'BO-05D:RF-P5Cav:Cell3PwrdBm-Mon', 'blue'],
            ['Power Forward', 'BO-05D:RF-P5Cav:PwrFwd-Mon',
             'BO-05D:RF-P5Cav:PwrFwddBm-Mon', 'darkGreen'],
            ['Power Reverse', 'BO-05D:RF-P5Cav:PwrRev-Mon',
             'BO-05D:RF-P5Cav:PwrRevdBm-Mon', 'red'],
        ]
    },
    'SI': {
        'Emergency': 'RA-RaSIA02:RF-IntlkCtrl:EStop-Mon',
        'Sirius Intlk': 'SI-02SB:RF-Intlk:SIA-Mon',
        'LLRF Intlk': 'SI-02SB:RF-LLRF:Intlk-Mon',
        'Intlk Details': {
            'Input': {
                'PV': 'SR-RF-DLLRF-01:Intlk-Mon',
                'Labels': (
                    'Rev Out SSA 1',
                    'Rev Out SSA 2',
                    'Not Used (RefSSA3)',
                    'Not Used (RevSSA4)',
                    'Rev Cavity',
                    'Not Used (Ext LLRF1)',
                    'Not Used (Ext LLRF2)',
                    'Not Used (Ext LLRF3)',
                    'Manual',
                    'PLC',
                    'Plunger 1 End Sw Up',
                    'Plunger 1 End Sw Down',
                    'Plunger 2 End Sw Up',
                    'Plunger 2 End Sw Down',
                ),
            },
            'Fast Input': {
                'PV': 'SR-RF-DLLRF-01:FASTINLK-MON',
                'Labels': (
                    'Cavity Voltage',
                    'Cavity Fwd',
                    'SSA 1 Out Fwd',
                    'Cell 2 Voltage (RFIN7)',
                    'Cell 6 Voltage (RFIN8)',
                    'SSA 2 Out Fwd (RFIN9)',
                    'SSA 2 Rev Fwd (RFIN10)',
                    'Pre-Drive 1 In (RFIN11)',
                    'Pre-Drive 1 Out (RFIN12)',
                    'Pre-Drive 2 In (RFIN13)',
                    'Pre-Drive 2 Out (RFIN14)',
                    'Circulator Out Fwd (RFIN15)',
                    'LLRF Beam Trip',
                ),
            }
        },
        'Reset': {
            'Global': 'SI-02SB:RF-Intlk:Reset-Sel',
            'LLRF': 'SR-RF-DLLRF-01:Reset-Cmd',
        },
        'Cav Sts': {
            'Geral': 'SI-02SB:RF-P7Cav:Sts-Mon',
            'Temp': {
                'Cells': (
                    ('SI-02SB:RF-P7Cav:Cylin1T-Mon', 'blue'),
                    ('SI-02SB:RF-P7Cav:Cylin2T-Mon', 'red'),
                    ('SI-02SB:RF-P7Cav:Cylin3T-Mon', 'yellow'),
                    ('SI-02SB:RF-P7Cav:Cylin4T-Mon', 'darkGreen'),
                    ('SI-02SB:RF-P7Cav:Cylin5T-Mon', 'magenta'),
                    ('SI-02SB:RF-P7Cav:Cylin6T-Mon', 'darkCyan'),
                    ('SI-02SB:RF-P7Cav:Cylin7T-Mon', 'darkRed'),
                ),
                'Coupler': ('SI-02SB:RF-P7Cav:CoupT-Mon', 'black'),
                'Discs': (
                    'SI-02SB:RF-P7Cav:Disc1Tms-Mon',
                    'SI-02SB:RF-P7Cav:Disc2Tms-Mon',
                    'SI-02SB:RF-P7Cav:Disc3Tms-Mon',
                    'SI-02SB:RF-P7Cav:Disc4Tms-Mon',
                    'SI-02SB:RF-P7Cav:Disc5Tms-Mon',
                    'SI-02SB:RF-P7Cav:Disc6Tms-Mon',
                    'SI-02SB:RF-P7Cav:Disc7Tms-Mon',
                    'SI-02SB:RF-P7Cav:Disc8Tms-Mon',
                ),
            },
            'FlwRt': (
                'SI-02SB:RF-P7Cav:HDFlwRt1-Mon',
                'SI-02SB:RF-P7Cav:HDFlwRt2-Mon',
                'SI-02SB:RF-P7Cav:HDFlwRt3-Mon',
            ),
            'Vac': {
                'Cells': 'SI-02SB:VA-CCG-CAV:Pressure-Mon',
                'Cond': 'SR-RF-DLLRF-01:VACUUM',
                'Cells ok': 'SI-02SB:RF-P7Cav:Pressure-Mon',
                'Coupler ok': 'SI-02SB:RF-P7Cav:CoupPressure-Mon',
            }
        },
        'TL Sts': {
            'Geral': 'RA-TL:RF-TrLine-SIA:Sts-Mon',
            'Circ TIn': 'RA-TL:RF-Circulator-SIA:Tin-Mon',
            'Circ TOut': 'RA-TL:RF-Circulator-SIA:Tout-Mon',
            'Circ Arc': 'RA-TL:RF-Circulator-SIA:Arc-Mon',
            'Load Arc': 'RA-TL:RF-Load-SIA:Arc-Mon',
            'Circ FlwRt': 'RA-TL:RF-Circulator-SIA:FlwRt-Mon',
            'Load FlwRt': 'RA-TL:RF-Load-SIA:FlwRt-Mon',
            'Circ Intlk': 'RA-TL:RF-Circulator-SIA:IntlkOp-Mon',
        },
        'SSA': {
            '1': {
                'Name': 'SSA 01',
                'Status': 'RA-ToSIA01:RF-SSAmpTower:Sts-Mon',
                'Power': 'RA-ToSIA01:RF-SSAmpTower:PwrFwdOut1-Mon',
                'SRC 1': {
                    'Label': 'AC TDK',
                    'PV': 'RA-ToSIA01:RF-ACPanel:PwrAC-Sts'
                },
                'SRC 2': {
                    'Label': 'DC TDK',
                    'PV': 'RA-ToSIA01:RF-TDKSource:PwrDC-Sts',
                },
                'PinSw': 'RA-RaSIA01:RF-LLRFPreAmp-1:PINSw1-Mon',
                'PreDrive': 'SR-RF-DLLRF-01:INPRE1:AMP',
            },
            '2': {
                'Name': 'SSA 02',
                'Status': 'RA-ToSIA02:RF-SSAmpTower:Sts-Mon',
                'Power': 'RA-ToSIA02:RF-SSAmpTower:PwrFwdOut1-Mon',
                'SRC 1': {
                    'Label': 'AC TDK',
                    'PV': 'RA-ToSIA02:RF-ACPanel:PwrAC-Sts',
                },
                'SRC 2': {
                    'Label': 'DC TDK',
                    'PV': 'RA-ToSIA02:RF-TDKSource:PwrDC-Sts',
                },
                'PinSw': 'RA-RaSIA01:RF-LLRFPreAmp-1:PINSw2-Mon',
                'PreDrive': 'SR-RF-DLLRF-01:INPRE2:AMP',
            }
        },
        'SL': {
            'Enbl': 'SR-RF-DLLRF-01:SL',
            'Mode': 'SR-RF-DLLRF-01:MODE',
            'IRef': 'SR-RF-DLLRF-01:I:SL:REF',
            'QRef': 'SR-RF-DLLRF-01:Q:SL:REF',
            'ARef': 'SR-RF-DLLRF-01:SL:REF:AMP',
            'PRef': 'SR-RF-DLLRF-01:SL:REF:PHS',
            'IInp': 'SR-RF-DLLRF-01:I:SL:INP',
            'QInp': 'SR-RF-DLLRF-01:Q:SL:INP',
            'AInp': 'SR-RF-DLLRF-01:SL:INP:AMP',
            'PInp': 'SR-RF-DLLRF-01:SL:INP:PHS',
            'IErr': 'SR-RF-DLLRF-01:I:SL:ERR',
            'QErr': 'SR-RF-DLLRF-01:Q:SL:ERR',
            'AErr': 'SR-RF-DLLRF-01:SL:ERR:AMP',
            'PErr': 'SR-RF-DLLRF-01:SL:ERR:PHS',
            'ASet': 'SR-RF-DLLRF-01:mV:AL:REF',
            'PSet': 'SR-RF-DLLRF-01:PL:REF',
            'AInc': 'SR-RF-DLLRF-01:AMPREF:INCRATE',
            'PInc': 'SR-RF-DLLRF-01:PHSREF:INCRATE',
        },
        'Tun': {
            'Auto': 'SR-RF-DLLRF-01:TUNE',
            'DTune': 'SR-RF-DLLRF-01:DTune-RB',
            'DPhase': 'SR-RF-DLLRF-01:TUNE:DEPHS',
            'Pl1Down': 'SR-RF-DLLRF-01:PLG1:MOVE:DN',
            'Pl1Up': 'SR-RF-DLLRF-01:PLG1:MOVE:UP',
            'Pl2Down': 'SR-RF-DLLRF-01:PLG2:MOVE:DN',
            'Pl2Up': 'SR-RF-DLLRF-01:PLG2:MOVE:UP',
            'PlM1Curr': 'RA-RaSIA01:RF-CavPlDrivers:Dr1Current-Mon',
            'PlM2Curr': 'RA-RaSIA01:RF-CavPlDrivers:Dr2Current-Mon',
        },
        'PwrMtr': [
            ['Cav - Cell 4', 'SI-02SB:RF-P7Cav:PwrCell4-Mon',
             'SI-02SB:RF-P7Cav:PwrCell4dBm-Mon', 'black'],
            ['Cav - Coup Fwd', 'SI-02SB:RF-P7Cav:PwrFwd-Mon',
             'SI-02SB:RF-P7Cav:PwrFwddBm-Mon', 'blue'],
            ['Cav - Coup Rev', 'SI-02SB:RF-P7Cav:PwrRev-Mon',
             'SI-02SB:RF-P7Cav:PwrRevdBm-Mon', 'red'],
            ['SSA1 - Fwd Out', 'RA-ToSIA01:RF-SSAmpTower:PwrFwdOutLLRF-Mon',
             'RA-ToSIA01:RF-SSAmpTower:PwrFwdOutdBm-Mon', 'magenta'],
            ['SSA1 - Rev Out', 'RA-ToSIA01:RF-SSAmpTower:PwrRevOutLLRF-Mon',
             'RA-ToSIA01:RF-SSAmpTower:PwrRevOutdBm-Mon', 'darkGreen'],
            ['SSA2 - Fwd Out', 'RA-ToSIA02:RF-SSAmpTower:PwrFwdOutLLRF-Mon',
             'RA-ToSIA02:RF-SSAmpTower:PwrFwdOutdBm-Mon', 'yellow'],
            ['SSA2 - Rev Out', 'RA-ToSIA02:RF-SSAmpTower:PwrRevOutLLRF-Mon',
             'RA-ToSIA02:RF-SSAmpTower:PwrRevOutdBm-Mon', 'cyan'],
            ['Circ - Fwd Out', 'RA-TL:RF-Circulator-SIA:PwrFwdOut-Mon',
             'RA-TL:RF-Circulator-SIA:PwrFwdOutdBm-Mon', 'darkCyan'],
        ]
    },
}
