# Grover Search Algorithm for Quantum Robot Localization

## Student Information

**Name:** Manish Kumar  
**Enrollment Number:** 230152  
**Institution:** Newton School of Technology  
**Course:** Quantum Computing

---

## Project Overview

This project implements the Grover search algorithm for quantum robot localization. The algorithm uses quantum computing to efficiently search for a robot's position in a grid-based map by matching sensor patterns (horizontal and vertical) against the map.

### Key Features

- **Quantum Search Implementation**: Uses Grover's algorithm to find optimal positions in O(√N) time complexity
- **Multi-Provider Support**: Compatible with IBM Quantum, IonQ, BlueQubit, and local simulators
- **Comprehensive Visualizations**: Professional dashboard with multiple analysis panels
- **Research Variations**: Pre-configured test cases for different scenarios
- **Detailed Reporting**: Automatic generation of summary reports and high-resolution visualizations

---

## Enhanced Visualization Features

The project includes a comprehensive visualization system optimized for 13-inch MacBook displays:

### Visualization Dashboard

1. **Measurement Results Distribution**
   - Bar chart showing measurement counts for each position
   - Color-coded bars (green for top result, blue for top 3)
   - Statistics overlay with top results and probabilities
   - Limited to top 15 results for optimal readability

2. **Probability Distribution**
   - Pie chart displaying top 5 results
   - Percentage breakdowns with clear labels
   - Enhanced color scheme for better contrast

3. **Circuit Statistics**
   - Horizontal bar chart showing:
     - Total qubits used
     - Circuit depth
     - Circuit size (number of gates)
     - Number of Grover iterations

4. **Search Space Heatmap**
   - Grid visualization showing probability distribution
   - Color-coded cells (yellow to red gradient)
   - Highlighted selected position with cyan border
   - Count and probability annotations

5. **Performance Metrics**
   - Success rate analysis
   - Confidence levels
   - Certainty measurements
   - Entropy calculations

6. **Enhanced Map Visualization**
   - Grid representation with pattern highlighting
   - Found pattern annotation with arrow
   - Pattern information overlay
   - Search statistics display

### Output Files

- **High-Resolution PNG**: `quantum_search_results_YYYYMMDD_HHMMSS.png` (300 DPI)
- **Summary Report**: `quantum_search_report_YYYYMMDD_HHMMSS.txt`
- **Enhanced Text Map**: Color-coded terminal output with statistics

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation Steps

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source ./venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env_sample .env
   # Edit .env file with your API tokens:
   # - IBM_TOKEN (for IBM Quantum)
   # - IONQ_TOKEN (for IonQ)
   # - BLUEQUBIT_TOKEN (for BlueQubit)
   ```

4. **Run the program**
   ```bash
   python main.py
   ```

---

## Configuration

### Main Configuration (`conf.py`)

The main configuration file allows you to customize:

#### Map and Pattern Settings

- **`inp_map_string`**: A 2D grid representing the search map
  ```python
  inp_map_string = [
      ["1 1 0 0 1 0 "],
      ["0 0 1 1 0 1 "],
      ["1 1 0 0 1 1 "],
      # ... more rows
  ]
  ```

- **`inp_pattern_row`**: Horizontal sensor pattern (what robot sees left-right)
  ```python
  inp_pattern_row = ["1", "1", "0", "0"]
  ```

- **`inp_pattern_col`**: Vertical sensor pattern (what robot sees up-down)
  ```python
  inp_pattern_col = ["1", "1", "0", "0"]
  ```

#### Execution Configuration

```python
CONFIG = {
    "TEST_ORACLE": {
        "enable": False,  # Set to True to validate oracle function
        "check_pos_row": 0,  # Row position to test
        "check_pos_col": 1   # Column position to test
    },
    "MAKE_IT_REAL": True,  # Whether to use real quantum hardware
    "AVAILABLE_PROVIDERS": ["IONQ", "IBM", "FAKEIBM", "SIMULATE", "BLUEQUBIT"],
    "SELECTED_PROVIDER": "SIMULATE",  # Choose your provider
    "USE_JOB_ID": "",  # Optional: resume from previous job
    "REUSE_ROW_COL_QUBITS": True,  # Optimize if row/col patterns are identical
}
```

### Research Variations

Use `research_variations.py` to quickly switch between pre-configured test cases:

```bash
python research_variations.py <variation_name>
```

Available variations:
- `sparse_6x6`: Sparse map with few matches
- `dense_6x6`: Dense map (all 1s) with many matches
- `target_6x6`: Map with clear target location
- `checkerboard_6x6`: Checkerboard pattern
- `small_pattern_6x6`: Small 2x2 pattern
- `medium_pattern_6x6`: Medium 3x3 pattern
- `asymmetric_6x6`: Asymmetric row/col patterns

---

## Example Usage

### Basic Example

```python
# In conf.py:
inp_map_string = [
    ["1 0 1 "],
    ["0 1 0 "],
    ["0 1 1 "]
]
inp_pattern_row = ["1", "0"]
inp_pattern_col = ["1", "0"]

# Run:
python main.py
```

### Using Research Variations

```bash
# Switch to sparse map variation
python research_variations.py sparse_6x6

# Run the search
python main.py
```

---

## Project Structure

```
paper_quantum_search/
├── main.py                 # Main execution script
├── lib.py                  # Core Grover algorithm implementation
├── utils.py                # Utility functions (map display, position creation)
├── visualizations.py       # Enhanced visualization system
├── conf.py                 # Configuration file
├── research_variations.py  # Pre-configured test variations
├── logs.py                 # Logging configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## Algorithm Details

### Grover's Algorithm Implementation

- **Search Space**: All possible positions where the pattern can fit
- **Oracle Function**: Checks if a position matches both row and column patterns
- **Diffusion Operator**: Amplifies the amplitude of the correct solution
- **Iterations**: Calculated as ⌈(π/4) × √(N/M)⌉ where:
  - N = total search space size
  - M = number of solutions (typically 1)

### Quantum Circuit Components

1. **Initialization**: Superposition of all possible positions
2. **Oracle**: Marks solutions with phase flip
3. **Diffusion**: Inversion about the mean
4. **Measurement**: Collapses to most probable solution

---

## Supported Quantum Providers

1. **SIMULATE**: Local Qiskit Aer simulator (fastest, no API needed)
2. **FAKEIBM**: IBM noise model simulator (requires IBM token)
3. **IBM**: Real IBM Quantum hardware (requires IBM token)
4. **IONQ**: IonQ quantum cloud (requires IonQ token)
5. **BLUEQUBIT**: BlueQubit quantum platform (requires BlueQubit token)

---

## Output and Results

### Console Output

- Real-time search progress
- Map visualization (initial and final)
- Position analysis
- Circuit statistics
- Comprehensive summary report

### Generated Files

1. **Visualization PNG**: High-resolution dashboard (300 DPI)
   - Filename: `quantum_search_results_YYYYMMDD_HHMMSS.png`
   - Contains all 6 analysis panels

2. **Summary Report**: Text file with detailed analysis
   - Filename: `quantum_search_report_YYYYMMDD_HHMMSS.txt`
   - Includes configuration, circuit info, results, and metrics

---

## Visualization Optimization

The visualization system is specifically optimized for:
- **13-inch MacBook displays** (2560x1600 Retina or 1280x800)
- **16:10 aspect ratio** for optimal fit
- **Professional styling** with consistent color scheme
- **Readable fonts** at all zoom levels
- **Efficient space usage** with compact layouts

---

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
2. **API Token Errors**: Check your `.env` file has correct tokens
3. **Memory Issues**: Reduce grid size or use `SIMULATE` provider for large circuits
4. **Visualization Not Showing**: Ensure matplotlib backend supports GUI (try `export MPLBACKEND=TkAgg`)

### Performance Tips

- Use `SIMULATE` for development and testing
- Use `FAKEIBM` to test with noise models
- Use real hardware (`IBM`, `IONQ`) for final results
- Smaller grids (4x4, 5x5) run faster than larger ones (6x6+)

---

## References

- Grover, L. K. (1996). A fast quantum mechanical algorithm for database search. *Proceedings of the 28th Annual ACM Symposium on Theory of Computing*
- Qiskit Documentation: https://qiskit.org/documentation/
- Quantum Computing Fundamentals: Nielsen & Chuang

---

## License

This project is part of the Quantum Computing course at Newton School of Technology.

---

## Contact

For questions or issues related to this project, please contact:
- **Student**: Manish Kumar
- **Enrollment**: 230152
- **Institution**: Newton School of Technology

---

*Last Updated: November 2024*
