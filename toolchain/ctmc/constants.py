#failure_mode_mutation_probabilities = {
#    'slaves':    { 'ports' : {} },
#    'ports' :    { 'slaves': {}, 'switches' : {}, 'links': {}},
#    'links' :    { 'ports' : {}, 'guardians': {} },
#    'guardians': { 'links' : {}, 'switches' : {} },
#    'switches':  { 'ports' : {}, 'guardians': {} },
#}

failure_mode_mutation_probabilities = {
    'slaves': {
        'ports': {
            'crash': {
                # Probability of a port crashing when it cannot contain a
                # crash from an adjacent slave.
                'crash': 0.111,
                # Probability of a port becoming byzantine when it cannot
                # contain a crash from an adjacent slave.
                'byzantine': 1 - 0.111
            },
            'byzantine': {
                # Probability of a port crashing when it cannot contain a
                # byzantine from an adjacent slave.
                'crash': 0,
                # Probability of a port becoming byzantine when it cannot
                # contain a byzantine from an adjacent slave.
                'byzantine': 1
            }
        }
    },

    'ports': {
        'slaves': {
            'crash': {
                # Probability of a slave crashing when it cannot contain a
                # crash from an adjacent port.
                'crash': 0.222,
                # Probability of a slave becoming byzantine when it cannot
                # contain a crash from an adjacent port.
                'byzantine': 1 - 0.222
            },
            'byzantine': {
                # Probability of a slave crashing when it cannot contain a
                # byzantine from an adjacent port.
                'crash': 0.333,
                # Probability of a slave becoming byzantine when it cannot
                # contain a byzantine from an adjacent port.
                'byzantine': 1 - 0.333
            }
        },
        'switches': {
            'crash': {
                # Probability of a switch crashing when it cannot contain a
                # crash from an adjacent port.
                'crash': 1,
                # Probability of a switch becoming byzantine when it cannot
                # contain a crash from an adjacent port.
                'byzantine': 0
            },
            'byzantine': {
                # Probability of a switch crashing when it cannot contain a
                # byzantine from an adjacent port.
                'crash': 1,
                # Probability of a switch becoming byzantine when it cannot
                # contain a byzantine from an adjacent port.
                'byzantine': 0
            }
        },
        'links': {
            'crash': {
                # Probability of a link crashing when it cannot contain a
                # crash from an adjacent port.
                'crash': 1,
                # Probability of a link becoming byzantine when it cannot
                # contain a crash from an adjacent port.
                'byzantine': 0
            },
            'byzantine': {
                # Probability of a link crashing when it cannot contain a
                # byzantine from an adjacent port.
                'crash': 0,
                # Probability of a link becoming byzantine when it cannot
                # contain a byzantine from an adjacent port.
                'byzantine': 1
            }
        }
    },

    'links': {
        'ports': {
            'crash': {
                # Probability of a port crashing when it cannot contain a
                # crash from an adjacent link.
                'crash': 1,
                # Probability of a port becoming byzantine when it cannot
                # contain a crash from an adjacent link.
                'byzantine': 0
            },
            'byzantine': {
                # Probability of a port crashing when it cannot contain a
                # byzantine from an adjacent link.
                'crash': 0,
                # Probability of a port becoming byzantine when it cannot
                # contain a byzantine from an adjacent link.
                'byzantine': 1
            }
        },
        'guardians': {
            'crash': {
                # Probability of a guardian crashing when it cannot contain a
                # crash from an adjacent link.
                'crash': 1,
                # Probability of a guardian becoming byzantine when it cannot
                # contain a crash from an adjacent link.
                'byzantine': 0
            },
            'byzantine': {
                # Probability of a guardian crashing when it cannot contain a
                # byzantine from an adjacent link.
                'crash': 1,
                # Probability of a guardian becoming byzantine when it cannot
                # contain a byzantine from an adjacent link.
                'byzantine': 0
            }
        }
    },

    'guardians': {
        'links': {
            'crash': {
                # Probability of a link crashing when it cannot contain a
                # crash from an adjacent guardian.
                'crash': 1,
                # Probability of a link becoming byzantine when it cannot
                # contain a crash from an adjacent guardian.
                'byzantine': 0
            },
            'byzantine': {
                # Probability of a link crashing when it cannot contain a
                # byzantine from an adjacent guardian.
                'crash': 1,
                # Probability of a link becoming byzantine when it cannot
                # contain a byzantine from an adjacent guardian.
                'byzantine': 0
            }
        },
        'switches': {
            'crash': {
                # Probability of a switch crashing when it cannot contain a
                # crash from an adjacent guardian.
                'crash': 1,
                # Probability of a switch becoming byzantine when it cannot
                # contain a crash from an adjacent guardian.
                'byzantine': 0
            },
            'byzantine': {
                # Probability of a switch crashing when it cannot contain a
                # byzantine from an adjacent guardian.
                'crash': 1,
                # Probability of a switch becoming byzantine when it cannot
                # contain a byzantine from an adjacent guardian.
                'byzantine': 0
            }
        }
    },

    # Guardians have crash failure semantics
    'switches': {
        'ports': {
            'crash': {
                # Probability of a port crashing when it cannot contain a
                # crash from an adjacent switch.
                'crash': 0.111,
                # Probability of a port becoming byzantine when it cannot
                # contain a crash from an adjacent switch.
                'byzantine': 1 - 0.111
            },
            'byzantine': {
                # Probability of a port crashing when it cannot contain a
                # byzantine from an adjacent switch.
                'crash': 0,
                # Probability of a port becoming byzantine when it cannot
                # contain a byzantine from an adjacent switch.
                'byzantine': 1
            }
        },
        'guardians': {
            'crash': {
                # Probability of a guardian crashing when it cannot contain a
                # crash from an adjacent switch.
                'crash': 1,
                # Probability of a guardian becoming byzantine when it cannot
                # contain a crash from an adjacent switch.
                'byzantine': 0
            },
            'byzantine': {
                # Probability of a guardian crashing when it cannot contain a
                # byzantine from an adjacent switch.
                'crash': 1,
                # Probability of a guardian becoming byzantine when it cannot
                # contain a byzantine from an adjacent switch.
                'byzantine': 0
            }
        }
    },
}