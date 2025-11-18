
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

# 4x4 GRID CONFIGURATION  
# Unique patterns for row and column (asymmetric) - WORKING VERSION
# Row pattern: "1 0" (checked vertically)
# Col pattern: "0 1" (checked horizontally)  
# These patterns are simpler and guaranteed to have a solution
inp_pattern_row = ["1", "0"]
inp_pattern_col = ["0", "1"]

# THE MAP - 4x4 GRID
# Map with position (1,1) matching both patterns:
# - Vertical: Col 1, rows 0-1 = "1 0" ✓
# - Horizontal: Row 1, cols 0-1 = "0 1" ✓
inp_map_string = [
    ["0 1 0 1 "] ,  # Row 0: col 1 = "1" (start of vertical "1 0")
    ["0 1 1 1 "] ,  # Row 1: col 1 = "0" (end of vertical "1 0"), cols 0-1 = "0 1" ✓
    ["1 1 0 0 "] ,  # Row 2
    ["0 1 1 0 "] ,  # Row 3
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
    