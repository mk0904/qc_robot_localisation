"""
Research Variations Helper
===========================

This script helps you quickly switch between different research variations
for testing the Grover algorithm on different map sizes and patterns.

Usage:
    python research_variations.py <variation_name>
    
Available variations:
    - sparse_6x6: Sparse 6x6 map with pattern ["1","1","0","0"]
    - dense_6x6: Dense 6x6 map (all 1s) with pattern ["1","1","0","0"]
    - target_6x6: 6x6 map with clear target location
    - checkerboard_6x6: Checkerboard pattern 6x6 map
    - small_pattern_6x6: 6x6 map with small 2x2 pattern
    - medium_pattern_6x6: 6x6 map with medium 3x3 pattern
    - asymmetric_6x6: 6x6 map with asymmetric row/col patterns
"""

import sys

VARIATIONS = {
    "sparse_6x6": {
        "pattern_row": ["1", "1", "0", "0"],
        "pattern_col": ["1", "1", "0", "0"],
        "map": [
            ["1 1 0 0 1 0 "],
            ["0 0 1 1 0 1 "],
            ["1 1 0 0 1 1 "],
            ["0 1 1 0 0 0 "],
            ["1 0 0 1 1 0 "],
            ["0 1 0 1 0 1 "],
        ]
    },
    "dense_6x6": {
        "pattern_row": ["1", "1", "0", "0"],
        "pattern_col": ["1", "1", "0", "0"],
        "map": [
            ["1 1 1 1 1 1 "],
            ["1 1 1 1 1 1 "],
            ["1 1 1 1 1 1 "],
            ["1 1 1 1 1 1 "],
            ["1 1 1 1 1 1 "],
            ["1 1 1 1 1 1 "],
        ]
    },
    "target_6x6": {
        "pattern_row": ["1", "1", "0", "0"],
        "pattern_col": ["1", "1", "0", "0"],
        "map": [
            ["0 0 0 0 0 0 "],
            ["0 0 0 0 0 0 "],
            ["0 0 1 1 0 0 "],
            ["0 0 1 1 0 0 "],
            ["0 0 0 0 0 0 "],
            ["0 0 0 0 0 0 "],
        ]
    },
    "checkerboard_6x6": {
        "pattern_row": ["1", "0", "1"],
        "pattern_col": ["1", "0", "1"],
        "map": [
            ["1 0 1 0 1 0 "],
            ["0 1 0 1 0 1 "],
            ["1 0 1 0 1 0 "],
            ["0 1 0 1 0 1 "],
            ["1 0 1 0 1 0 "],
            ["0 1 0 1 0 1 "],
        ]
    },
    "small_pattern_6x6": {
        "pattern_row": ["1", "1"],
        "pattern_col": ["1", "1"],
        "map": [
            ["1 1 0 0 1 0 "],
            ["0 0 1 1 0 1 "],
            ["1 1 0 0 1 1 "],
            ["0 1 1 0 0 0 "],
            ["1 0 0 1 1 0 "],
            ["0 1 0 1 0 1 "],
        ]
    },
    "medium_pattern_6x6": {
        "pattern_row": ["1", "1", "0"],
        "pattern_col": ["1", "1", "0"],
        "map": [
            ["1 1 0 0 1 0 "],
            ["0 0 1 1 0 1 "],
            ["1 1 0 0 1 1 "],
            ["0 1 1 0 0 0 "],
            ["1 0 0 1 1 0 "],
            ["0 1 0 1 0 1 "],
        ]
    },
    "asymmetric_6x6": {
        "pattern_row": ["1", "0", "1"],
        "pattern_col": ["1", "1", "0"],
        "map": [
            ["1 1 0 0 1 0 "],
            ["0 0 1 1 0 1 "],
            ["1 1 0 0 1 1 "],
            ["0 1 1 0 0 0 "],
            ["1 0 0 1 1 0 "],
            ["0 1 0 1 0 1 "],
        ]
    },
}


def generate_conf_file(variation_name):
    """Generate conf.py content for a given variation."""
    if variation_name not in VARIATIONS:
        print(f"Error: Unknown variation '{variation_name}'")
        print(f"\nAvailable variations: {', '.join(VARIATIONS.keys())}")
        return None
    
    var = VARIATIONS[variation_name]
    
    # Format pattern as Python list
    pattern_row_str = str(var["pattern_row"]).replace("'", '"')
    pattern_col_str = str(var["pattern_col"]).replace("'", '"')
    
    # Format map as Python list
    map_lines = []
    for row in var["map"]:
        map_lines.append(f'    {str(row)},')
    
    map_str = "\n".join(map_lines)
    
    conf_content = f'''# ROBOT'S SENSORS (horizontal & vertical)
# Variation: {variation_name}
inp_pattern_row = {pattern_row_str}
inp_pattern_col = {pattern_col_str}

# THE MAP - 6x6 GRID
inp_map_string = [
{map_str}
]

CONFIG = {{
    "TEST_ORACLE": {{
        "enable": False, # Used to validate the Oracle
        "check_pos_row": 0, # Validate the oracle with this value (check if output=1)
        "check_pos_col": 1
    }},
    "MAKE_IT_REAL": True, # Sent it to some provider? (if False: simulate locally)
    "AVAILABLE_PROVIDERS": ["IONQ", "IBM", "FAKEIBM", "SIMULATE", "BLUEQUBIT"],
    "SELECTED_PROVIDER": "SIMULATE",
    "USE_JOB_ID": "", # Used to recall results from an external service
    "REUSE_ROW_COL_QUBITS": inp_pattern_row==inp_pattern_col, # If set to True, Row and Col patterns are the same, so Qubits are reused
}}
'''
    return conf_content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable variations:")
        for name, var in VARIATIONS.items():
            print(f"  - {name}: pattern={var['pattern_row']}, map_size=6x6")
        sys.exit(1)
    
    variation = sys.argv[1]
    conf_content = generate_conf_file(variation)
    
    if conf_content:
        # Write to conf.py
        with open("conf.py", "w") as f:
            f.write(conf_content)
        print(f"✓ Successfully updated conf.py with variation: {variation}")
        print(f"  Pattern row: {VARIATIONS[variation]['pattern_row']}")
        print(f"  Pattern col: {VARIATIONS[variation]['pattern_col']}")
        print(f"  Map size: 6x6")
        print("\nYou can now run: python main.py")

