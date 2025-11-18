
# ROBOT'S SENSORS (horizontal & vertical)
# A single data is centered in the robot
# From there... if row length is 2, each data is shown with the robot in the middle-->   1 r 2

# PATTERN VARIATIONS FOR RESEARCH:
# Variation 1: Small pattern (2x2) - easier to find
# inp_pattern_row=  ["1", "1"]
# inp_pattern_col=  ["1", "1"]

# Variation 2: Medium pattern (3x3) - moderate difficulty
# inp_pattern_row=  ["1", "1", "0"]
# inp_pattern_col=  ["1", "1", "0"]

# Variation 3: Large pattern (4x4) - more challenging
# inp_pattern_row=  ["1", "1", "0", "0"]
# inp_pattern_col=  ["1", "1", "0", "0"]

# Variation 4: Asymmetric pattern - different row/col patterns
inp_pattern_row=  ["1", ]
inp_pattern_col=  ["1", ]


# THE MAP - 6x6 GRID
# Map variations for research:

# Variation 1: Sparse map with few matches
inp_map_string = [
    ["1 1 0 0 1 0 "] ,
    ["0 0 1 1 0 1 "] ,
    ["1 1 0 0 1 1 "] ,
    ["0 1 1 0 0 0 "] ,
    ["1 0 0 1 1 0 "] ,
    ["0 1 0 1 0 1 "] ,
]

# Variation 2: Dense map with many matches (commented out)
# inp_map_string = [
#     ["1 1 1 1 1 1 "] ,
#     ["1 1 1 1 1 1 "] ,
#     ["1 1 1 1 1 1 "] ,
#     ["1 1 1 1 1 1 "] ,
#     ["1 1 1 1 1 1 "] ,
#     ["1 1 1 1 1 1 "] ,
# ]

# Variation 3: Pattern with clear target location (commented out)
# inp_map_string = [
#     ["0 0 0 0 0 0 "] ,
#     ["0 0 0 0 0 0 "] ,
#     ["0 0 1 1 0 0 "] ,
#     ["0 0 1 1 0 0 "] ,
#     ["0 0 0 0 0 0 "] ,
#     ["0 0 0 0 0 0 "] ,
# ]

# Variation 4: Random-like distribution (commented out)
# inp_map_string = [
#     ["1 0 1 0 1 0 "] ,
#     ["0 1 0 1 0 1 "] ,
#     ["1 0 1 0 1 0 "] ,
#     ["0 1 0 1 0 1 "] ,
#     ["1 0 1 0 1 0 "] ,
#     ["0 1 0 1 0 1 "] ,
# ]

CONFIG = {
    "TEST_ORACLE": {
        "enable": False, # Used to validate the Oracle
        "check_pos_row": 0, # Validate the oracle with this value (check if output=1)
        "check_pos_col": 1
    },
    "MAKE_IT_REAL": True, # Sent it to some provider? (if False: simulate locally)
    "AVAILABLE_PROVIDERS": ["IONQ", "IBM", "FAKEIBM", "SIMULATE", "BLUEQUBIT"],
    "SELECTED_PROVIDER": "SIMULATE",
    "USE_JOB_ID": "", # Used to recall results from an external service
    "REUSE_ROW_COL_QUBITS": inp_pattern_row==inp_pattern_col, # If set to True, Row and Col patterns are the same, so Qubits are reused
}    
    