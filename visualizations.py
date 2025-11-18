"""
Enhanced Visualization Module for Quantum Search
================================================
This module provides comprehensive visualizations for the Grover search algorithm,
including detailed statistics, probability distributions, and performance metrics.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
import math
from textwrap import wrap
import re
from termcolor import colored
from qiskit.visualization import plot_histogram
import seaborn as sns

# Set style for professional plots
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except OSError:
    try:
        plt.style.use('seaborn-darkgrid')
    except OSError:
        plt.style.use('default')
sns.set_palette("husl")

def create_comprehensive_visualization(counts, positions, qc, num_repetitions, 
                                     inp_map_string, GRID_WIDTH, BYTE_SIZE,
                                     selected_row, selected_col, inp_pattern_row, 
                                     inp_pattern_col, backend_name="SIMULATE"):
    """
    Create a comprehensive multi-panel visualization optimized for 13-inch MacBook screens.
    """
    # Optimized size for 13-inch MacBook (2560x1600 or 1280x800)
    # Using 16:10 aspect ratio that fits well
    fig = plt.figure(figsize=(16, 10), facecolor='white', dpi=100)
    
    # Create a more compact grid layout with better spacing
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35, 
                  left=0.08, right=0.95, top=0.93, bottom=0.07)
    
    # Add subtle background color
    fig.patch.set_facecolor('#f8f9fa')
    
    # Calculate statistics
    total_shots = sum(counts.values())
    probabilities = {k: v/total_shots for k, v in counts.items()}
    top_5 = dict(list(sorted(counts.items(), key=lambda x: x[1], reverse=True))[:5])
    
    # Panel 1: Enhanced Histogram with Statistics
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.set_facecolor('white')
    create_enhanced_histogram(ax1, counts, positions, total_shots, top_5)
    
    # Panel 2: Probability Distribution
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.set_facecolor('white')
    create_probability_distribution(ax2, probabilities, positions)
    
    # Panel 3: Circuit Statistics
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('white')
    create_circuit_statistics(ax3, qc, num_repetitions, backend_name)
    
    # Panel 4: Search Space Analysis
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('white')
    create_search_space_analysis(ax4, positions, counts, selected_row, selected_col)
    
    # Panel 5: Performance Metrics
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.set_facecolor('white')
    create_performance_metrics(ax5, counts, positions, num_repetitions, total_shots)
    
    # Panel 6: Enhanced Map Visualization
    ax6 = fig.add_subplot(gs[2, :])
    ax6.set_facecolor('white')
    create_enhanced_map_visualization(ax6, inp_map_string, GRID_WIDTH, BYTE_SIZE,
                                     selected_row, selected_col, inp_pattern_row, 
                                     inp_pattern_col, positions, counts)
    
    # Enhanced title with better styling
    plt.suptitle('Grover Algorithm: Comprehensive Search Analysis', 
                 fontsize=18, fontweight='bold', y=0.98,
                 color='#2c3e50', family='sans-serif')
    
    # Add subtle border around the entire figure
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
        for spine in ax.spines.values():
            spine.set_edgecolor('#e0e0e0')
            spine.set_linewidth(1.5)
    
    return fig

def create_enhanced_histogram(ax, counts, positions, total_shots, top_5):
    """Create an enhanced histogram with detailed statistics - optimized for 13-inch display."""
    # Prepare data - limit to top 15 for better readability on smaller screens
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    display_limit = min(15, len(sorted_counts))
    
    position_indices = []
    position_labels = []
    count_values = []
    
    for key, value in sorted_counts[:display_limit]:
        pos_idx = int(key[::-1], 2)
        if pos_idx < len(positions):
            pos = positions[pos_idx]
            position_indices.append(pos_idx)
            position_labels.append(f"({pos['row']},{pos['col']})")
            count_values.append(value)
    
    # Create bar plot with enhanced colors
    colors = ['#27ae60' if i == 0 else '#3498db' if i < 3 else '#95a5a6' 
              for i in range(len(count_values))]
    bars = ax.bar(range(len(count_values)), count_values, color=colors, 
                  alpha=0.85, edgecolor='#34495e', linewidth=1.2, zorder=3)
    
    # Add value labels on bars (smaller font for compact display)
    for i, (bar, val) in enumerate(zip(bars, count_values)):
        height = bar.get_height()
        prob = (val / total_shots) * 100
        # Only show percentage if bar is tall enough
        if height > max(count_values) * 0.1:
            ax.text(bar.get_x() + bar.get_width()/2., height + max(count_values)*0.01,
                    f'{val}\n({prob:.1f}%)',
                    ha='center', va='bottom', fontsize=8, fontweight='bold', color='#2c3e50')
    
    # Customize axes with better styling
    ax.set_xlabel('Position Index (Row, Col)', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Measurement Count', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.set_title(f'Measurement Results Distribution\n(Total Shots: {total_shots:,})', 
                 fontsize=12, fontweight='bold', color='#2c3e50', pad=10)
    ax.set_xticks(range(len(position_labels)))
    ax.set_xticklabels(position_labels, rotation=45, ha='right', fontsize=9)
    ax.grid(True, alpha=0.25, axis='y', linestyle='--', linewidth=0.8, color='#bdc3c7')
    ax.set_axisbelow(True)
    
    # Enhanced statistics text box
    top_key = list(top_5.keys())[0]
    top_prob = (top_5[top_key] / total_shots) * 100
    stats_text = f'Top Result: {top_5[top_key]} ({top_prob:.2f}%)\n'
    stats_text += f'Top 3: {sum(list(top_5.values())[:3])} ({sum([(v/total_shots)*100 for v in list(top_5.values())[:3]]):.2f}%)\n'
    stats_text += f'Unique: {len(counts)}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='top', color='#2c3e50',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff9e6', 
                     edgecolor='#f39c12', alpha=0.9, linewidth=1.5))

def create_probability_distribution(ax, probabilities, positions):
    """Create a probability distribution pie chart - optimized for 13-inch display."""
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    top_5_probs = dict(sorted_probs[:5])
    other_prob = sum([v for k, v in sorted_probs[5:]])
    
    if other_prob > 0:
        top_5_probs['Others'] = other_prob
    
    labels = []
    for key in top_5_probs.keys():
        if key != 'Others':
            pos_idx = int(key[::-1], 2)
            if pos_idx < len(positions):
                pos = positions[pos_idx]
                labels.append(f"({pos['row']},{pos['col']})")
            else:
                labels.append(key)
        else:
            labels.append('Others')
    
    # Enhanced color scheme
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#95a5a6']
    colors = colors[:len(top_5_probs)]
    
    wedges, texts, autotexts = ax.pie(top_5_probs.values(), labels=labels, 
                                       autopct='%1.1f%%', colors=colors,
                                       startangle=90, textprops={'fontsize': 9},
                                       wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    
    for autotext in autotexts:
        autotext.set_color('#2c3e50')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    for text in texts:
        text.set_fontsize(9)
        text.set_color('#2c3e50')
        text.set_fontweight('bold')
    
    ax.set_title('Probability Distribution\n(Top 5 Results)', 
                 fontsize=12, fontweight='bold', color='#2c3e50', pad=10)

def create_circuit_statistics(ax, qc, num_repetitions, backend_name):
    """Create a visualization of circuit statistics - optimized for 13-inch display."""
    stats_data = {
        'Qubits': qc.num_qubits,
        'Depth': qc.depth(),
        'Size': qc.size(),
        'Repetitions': num_repetitions
    }
    
    categories = list(stats_data.keys())
    values = list(stats_data.values())
    colors_bar = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    bars = ax.barh(categories, values, color=colors_bar, alpha=0.85, 
                   edgecolor='#34495e', linewidth=1.2, zorder=3)
    
    # Add value labels with better formatting
    for i, (bar, val) in enumerate(zip(bars, values)):
        width = bar.get_width()
        ax.text(width + max(values)*0.02, bar.get_y() + bar.get_height()/2,
                f'{val:,}',
                ha='left', va='center', fontsize=10, fontweight='bold', color='#2c3e50')
    
    ax.set_xlabel('Value', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.set_title(f'Circuit Statistics\n(Backend: {backend_name})', 
                 fontsize=12, fontweight='bold', color='#2c3e50', pad=10)
    ax.grid(True, alpha=0.25, axis='x', linestyle='--', linewidth=0.8, color='#bdc3c7')
    ax.set_axisbelow(True)
    ax.tick_params(colors='#2c3e50', labelsize=9)

def create_search_space_analysis(ax, positions, counts, selected_row, selected_col):
    """Create a visualization of the search space - optimized for 13-inch display."""
    # Create a grid representation
    max_row = max([p['row'] for p in positions])
    max_col = max([p['col'] for p in positions])
    
    grid = np.zeros((max_row + 1, max_col + 1))
    prob_grid = np.zeros((max_row + 1, max_col + 1))
    
    total_shots = sum(counts.values())
    
    for key, value in counts.items():
        pos_idx = int(key[::-1], 2)
        if pos_idx < len(positions):
            pos = positions[pos_idx]
            grid[pos['row'], pos['col']] = value
            prob_grid[pos['row'], pos['col']] = (value / total_shots) * 100
    
    # Enhanced colormap
    im = ax.imshow(prob_grid, cmap='YlOrRd', aspect='auto', interpolation='nearest', vmin=0)
    
    # Add text annotations with better readability
    for i in range(max_row + 1):
        for j in range(max_col + 1):
            if grid[i, j] > 0:
                prob_val = prob_grid[i, j]
                # Better text color selection based on background
                text_color = 'white' if prob_val > 30 else '#2c3e50'
                # Smaller font for compact display
                ax.text(j, i, f'{int(grid[i, j])}\n({prob_val:.1f}%)',
                       ha='center', va='center', color=text_color,
                       fontsize=8, fontweight='bold')
    
    # Enhanced highlight for selected position
    if selected_row >= 0 and selected_col >= 0:
        rect = mpatches.Rectangle((selected_col - 0.5, selected_row - 0.5), 
                                 1, 1, linewidth=3, edgecolor='#00d4ff', 
                                 facecolor='none', linestyle='--', zorder=10)
        ax.add_patch(rect)
    
    ax.set_xlabel('Column', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Row', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.set_title('Search Space Heatmap\n(Probability %)', 
                 fontsize=12, fontweight='bold', color='#2c3e50', pad=10)
    ax.set_xticks(range(max_col + 1))
    ax.set_yticks(range(max_row + 1))
    ax.tick_params(colors='#2c3e50', labelsize=9)
    
    # Enhanced colorbar
    cbar = plt.colorbar(im, ax=ax, label='Probability (%)', shrink=0.8)
    cbar.set_label('Probability (%)', fontsize=9, fontweight='bold', color='#2c3e50')
    cbar.ax.tick_params(colors='#2c3e50', labelsize=8)

def create_performance_metrics(ax, counts, positions, num_repetitions, total_shots):
    """Create performance metrics visualization - optimized for 13-inch display."""
    # Calculate metrics
    top_result_count = max(counts.values())
    top_result_prob = (top_result_count / total_shots) * 100
    success_rate = top_result_prob
    confidence = (top_result_count / total_shots) * 100
    
    # Calculate entropy (measure of uncertainty)
    probabilities = [v/total_shots for v in counts.values()]
    entropy = -sum([p * math.log2(p) if p > 0 else 0 for p in probabilities])
    max_entropy = math.log2(len(counts))
    normalized_entropy = (entropy / max_entropy) * 100 if max_entropy > 0 else 0
    
    metrics = {
        'Success\nRate': success_rate,
        'Top\nResult': top_result_prob,
        'Confidence': confidence,
        'Certainty': 100 - normalized_entropy
    }
    
    categories = list(metrics.keys())
    values = list(metrics.values())
    colors_metric = ['#27ae60', '#2980b9', '#8e44ad', '#e67e22']
    
    bars = ax.bar(categories, values, color=colors_metric, alpha=0.85, 
                  edgecolor='#34495e', linewidth=1.2, zorder=3)
    
    # Add value labels
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{val:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2c3e50')
    
    ax.set_ylabel('Percentage (%)', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.set_title(f'Performance Metrics\n(Repetitions: {num_repetitions})', 
                 fontsize=12, fontweight='bold', color='#2c3e50', pad=10)
    ax.set_ylim([0, 105])
    ax.grid(True, alpha=0.25, axis='y', linestyle='--', linewidth=0.8, color='#bdc3c7')
    ax.set_axisbelow(True)
    ax.tick_params(colors='#2c3e50', labelsize=9)
    plt.xticks(rotation=0, ha='center')

def create_enhanced_map_visualization(ax, inp_map_string, GRID_WIDTH, BYTE_SIZE,
                                     selected_row, selected_col, inp_pattern_row,
                                     inp_pattern_col, positions, counts):
    """Create an enhanced map visualization with pattern highlighting."""
    # Parse map string - handle both string and list formats
    if isinstance(inp_map_string, list):
        map_clean = "".join(["".join(item) for item in inp_map_string]).replace(" ", "").replace("X", "1")
    else:
        map_clean = inp_map_string.replace(" ", "").replace("X", "1")
    
    # Calculate grid height
    if BYTE_SIZE > 0:
        GRID_HEIGHT = len(map_clean) // (GRID_WIDTH * BYTE_SIZE)
    else:
        GRID_HEIGHT = len(map_clean) // GRID_WIDTH if GRID_WIDTH > 0 else 1
    
    # Create grid
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            idx = i * GRID_WIDTH * BYTE_SIZE + j * BYTE_SIZE
            if idx < len(map_clean):
                val = map_clean[idx:idx+BYTE_SIZE]
                grid[i, j] = int(val, 2) if val else 0
    
    # Create heatmap
    cmap = plt.cm.RdYlGn
    im = ax.imshow(grid, cmap=cmap, aspect='auto', vmin=0, vmax=1, 
                   interpolation='nearest', alpha=0.7)
    
    # Add grid lines
    for i in range(GRID_HEIGHT + 1):
        ax.axhline(i - 0.5, color='black', linewidth=0.5)
    for j in range(GRID_WIDTH + 1):
        ax.axvline(j - 0.5, color='black', linewidth=0.5)
    
    # Add cell values (optimized font size for 13-inch)
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            val = int(map_clean[i * GRID_WIDTH * BYTE_SIZE + j * BYTE_SIZE:
                               i * GRID_WIDTH * BYTE_SIZE + j * BYTE_SIZE + BYTE_SIZE], 2) if BYTE_SIZE > 0 else int(map_clean[i * GRID_WIDTH + j])
            text_color = 'white' if grid[i, j] == 1 else 'black'
            ax.text(j, i, str(val), ha='center', va='center',
                   color=text_color, fontsize=11, fontweight='bold')
    
    # Highlight selected position
    if selected_row >= 0 and selected_col >= 0:
        # Highlight the pattern area
        pattern_row_len = len(inp_pattern_row)
        pattern_col_len = len(inp_pattern_col)
        
        # Draw pattern bounding box (enhanced styling)
        rect = mpatches.Rectangle((selected_col - pattern_row_len/2 - 0.5, 
                                   selected_row - pattern_col_len/2 - 0.5),
                                 pattern_row_len, pattern_col_len,
                                 linewidth=3.5, edgecolor='#00d4ff', 
                                 facecolor='none', linestyle='--', alpha=0.9, zorder=10)
        ax.add_patch(rect)
        
        # Add annotation (optimized for 13-inch)
        ax.annotate('FOUND PATTERN', 
                   xy=(selected_col, selected_row),
                   xytext=(selected_col + 2, selected_row - 2),
                   arrowprops=dict(arrowstyle='->', color='#00d4ff', lw=2.5),
                   fontsize=10, fontweight='bold', color='#00d4ff',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff9e6', 
                            edgecolor='#f39c12', alpha=0.9, linewidth=2))
    
    # Add pattern information (optimized for 13-inch)
    pattern_info = f"Row Pattern: {inp_pattern_row}\nCol Pattern: {inp_pattern_col}"
    ax.text(0.02, 0.98, pattern_info, transform=ax.transAxes,
           fontsize=9, verticalalignment='top', color='#2c3e50',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#e3f2fd', 
                    edgecolor='#2196f3', alpha=0.9, linewidth=1.5))
    
    # Add search statistics (optimized for 13-inch)
    if selected_row >= 0 and selected_col >= 0:
        # Find the count for selected position
        selected_count = 0
        for key, value in counts.items():
            pos_idx = int(key[::-1], 2)
            if pos_idx < len(positions):
                pos = positions[pos_idx]
                if pos['row'] == selected_row and pos['col'] == selected_col:
                    selected_count = value
                    break
        
        total_shots = sum(counts.values())
        prob = (selected_count / total_shots) * 100 if total_shots > 0 else 0
        stats_info = f"Selected: ({selected_row}, {selected_col})\n"
        stats_info += f"Count: {selected_count}/{total_shots}\n"
        stats_info += f"Prob: {prob:.2f}%"
        ax.text(0.98, 0.98, stats_info, transform=ax.transAxes,
               fontsize=9, verticalalignment='top', horizontalalignment='right',
               color='#2c3e50',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#e8f5e9', 
                        edgecolor='#4caf50', alpha=0.9, linewidth=1.5))
    
    ax.set_xlabel('Column Index', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Row Index', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.set_title('Search Grid with Pattern Match Highlighting', 
                 fontsize=13, fontweight='bold', color='#2c3e50', pad=10)
    ax.set_xticks(range(GRID_WIDTH))
    ax.set_yticks(range(GRID_HEIGHT))
    ax.tick_params(colors='#2c3e50', labelsize=9)
    
    # Enhanced colorbar
    cbar = plt.colorbar(im, ax=ax, ticks=[0, 1], shrink=0.6)
    cbar.set_label('Cell Value', fontsize=10, fontweight='bold', color='#2c3e50')
    cbar.set_ticklabels(['0', '1'])
    cbar.ax.tick_params(colors='#2c3e50', labelsize=9)

def show_enhanced_map(inp_map_string, GRID_WIDTH, BYTE_SIZE, selected_row=None, 
                     selected_column=None, positions=None, counts=None):
    """
    Enhanced version of show_map with more details and better formatting.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    BLANK = "".join([" " for each in range(BYTE_SIZE)])
    LINE = "═"
    
    # Parse map - handle both string and list formats
    if isinstance(inp_map_string, list):
        map_clean = "".join(["".join(item) for item in inp_map_string]).replace(" ", "").replace("X", "1")
    else:
        map_clean = inp_map_string.replace(" ", "").replace("X", "1")
    
    # Calculate grid height
    if BYTE_SIZE > 0 and GRID_WIDTH > 0:
        GRID_HEIGHT = len([c for c in map_clean if c in "01"]) // (GRID_WIDTH * BYTE_SIZE)
    elif GRID_WIDTH > 0:
        GRID_HEIGHT = len([c for c in map_clean if c in "01"]) // GRID_WIDTH
    else:
        GRID_HEIGHT = 1
    
    print("\n" + "="*80)
    print(colored(" " * 25 + "QUANTUM SEARCH GRID VISUALIZATION", "cyan", attrs=['bold']))
    print("="*80)
    
    # Upper header with column indices
    column_items = "     "
    for index in range(GRID_WIDTH):
        if index == selected_column:
            column_items = column_items + colored(f"{index:>{BYTE_SIZE+1}}", "red", attrs=['bold', 'underline'])
        else:
            column_items = column_items + f"{index:>{BYTE_SIZE+1}}"
    
    print(column_items)
    print("     " + "─" * (len(column_items) - 5))
    
    # Print rows
    row_idx = 0
    for each_map_line in wrap(map_clean, GRID_WIDTH * BYTE_SIZE):
        if row_idx >= GRID_HEIGHT:
            break
            
        line_items = wrap(each_map_line, BYTE_SIZE)
        line = ""
        
        for col_idx, item in enumerate(line_items):
            if row_idx == selected_row and col_idx == selected_column:
                line = line + colored(item, "red", attrs=['bold', 'reverse']) + " "
            elif row_idx == selected_row:
                line = line + colored(item, "yellow", attrs=['bold']) + " "
            elif col_idx == selected_column:
                line = line + colored(item, "yellow", attrs=['bold']) + " "
            else:
                line = line + item + " "
        
        row_label = colored(f"{row_idx:3d}", "cyan", attrs=['bold']) if row_idx == selected_row else f"{row_idx:3d}"
        print(f"{row_label} │ {line}│")
        row_idx += 1
    
    print("     " + "─" * (len(column_items) - 5))
    
    # Add statistics if available
    if positions and counts and selected_row is not None and selected_column is not None:
        total_shots = sum(counts.values())
        selected_count = 0
        selected_prob = 0
        
        for key, value in counts.items():
            pos_idx = int(key[::-1], 2)
            if pos_idx < len(positions):
                pos = positions[pos_idx]
                if pos['row'] == selected_row and pos['col'] == selected_column:
                    selected_count = value
                    selected_prob = (value / total_shots) * 100 if total_shots > 0 else 0
                    break
        
        print("\n" + colored("Search Statistics:", "green", attrs=['bold']))
        print(f"  • Selected Position: ({selected_row}, {selected_column})")
        print(f"  • Measurement Count: {selected_count} / {total_shots}")
        print(f"  • Probability: {selected_prob:.2f}%")
        print(f"  • Total Search Positions: {len(positions)}")
    
    print("="*80 + "\n")

def generate_summary_report(counts, positions, qc, num_repetitions, selected_row, 
                           selected_col, inp_pattern_row, inp_pattern_col, 
                           backend_name, total_shots):
    """
    Generate a comprehensive text summary report of the search results.
    """
    report = []
    report.append("="*80)
    report.append(" " * 20 + "QUANTUM SEARCH ALGORITHM - SUMMARY REPORT")
    report.append("="*80)
    report.append("")
    
    # Search Configuration
    report.append(colored("SEARCH CONFIGURATION", "cyan", attrs=['bold']))
    report.append("-" * 80)
    report.append(f"  Backend: {backend_name}")
    report.append(f"  Row Pattern: {inp_pattern_row}")
    report.append(f"  Column Pattern: {inp_pattern_col}")
    report.append(f"  Grover Iterations: {num_repetitions}")
    report.append(f"  Total Shots: {total_shots}")
    report.append("")
    
    # Circuit Information
    report.append(colored("CIRCUIT INFORMATION", "cyan", attrs=['bold']))
    report.append("-" * 80)
    report.append(f"  Total Qubits: {qc.num_qubits}")
    report.append(f"  Circuit Depth: {qc.depth()}")
    report.append(f"  Circuit Size: {qc.size()}")
    report.append("")
    
    # Search Space
    report.append(colored("SEARCH SPACE ANALYSIS", "cyan", attrs=['bold']))
    report.append("-" * 80)
    report.append(f"  Total Search Positions: {len(positions)}")
    report.append(f"  Search Space Size (N): {len(positions)}")
    report.append(f"  Expected Solutions (M): 1")
    report.append(f"  Optimal Iterations: {math.ceil((math.pi/4) * math.sqrt(len(positions)))}")
    report.append(f"  Actual Iterations: {num_repetitions}")
    report.append("")
    
    # Results Analysis
    report.append(colored("RESULTS ANALYSIS", "cyan", attrs=['bold']))
    report.append("-" * 80)
    
    sorted_results = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top_result = sorted_results[0]
    top_pos_idx = int(top_result[0][::-1], 2)
    
    if top_pos_idx < len(positions):
        top_pos = positions[top_pos_idx]
        top_prob = (top_result[1] / total_shots) * 100
        report.append(f"  Top Result: Position ({top_pos['row']}, {top_pos['col']})")
        report.append(f"    - Count: {top_result[1]} / {total_shots}")
        report.append(f"    - Probability: {top_prob:.2f}%")
        report.append(f"    - Binary Index: {top_result[0]}")
        report.append("")
    
    # Top 5 Results
    report.append("  Top 5 Results:")
    for i, (key, value) in enumerate(sorted_results[:5], 1):
        pos_idx = int(key[::-1], 2)
        if pos_idx < len(positions):
            pos = positions[pos_idx]
            prob = (value / total_shots) * 100
            report.append(f"    {i}. Position ({pos['row']}, {pos['col']}): "
                         f"{value} counts ({prob:.2f}%)")
    
    report.append("")
    
    # Success Metrics
    report.append(colored("SUCCESS METRICS", "cyan", attrs=['bold']))
    report.append("-" * 80)
    top_prob = (sorted_results[0][1] / total_shots) * 100
    top3_prob = sum([v for k, v in sorted_results[:3]]) / total_shots * 100
    
    report.append(f"  Top Result Confidence: {top_prob:.2f}%")
    report.append(f"  Top 3 Combined: {top3_prob:.2f}%")
    report.append(f"  Unique Results: {len(counts)}")
    
    # Calculate entropy
    probabilities = [v/total_shots for v in counts.values()]
    entropy = -sum([p * math.log2(p) if p > 0 else 0 for p in probabilities])
    max_entropy = math.log2(len(counts))
    normalized_entropy = (entropy / max_entropy) * 100 if max_entropy > 0 else 0
    
    report.append(f"  Result Entropy: {entropy:.3f} bits (Normalized: {normalized_entropy:.1f}%)")
    report.append("")
    
    # Selected Position (if found)
    if selected_row >= 0 and selected_col >= 0:
        report.append(colored("SELECTED POSITION", "green", attrs=['bold']))
        report.append("-" * 80)
        report.append(f"  Row: {selected_row}")
        report.append(f"  Column: {selected_col}")
        
        # Find count for selected position
        selected_count = 0
        for key, value in counts.items():
            pos_idx = int(key[::-1], 2)
            if pos_idx < len(positions):
                pos = positions[pos_idx]
                if pos['row'] == selected_row and pos['col'] == selected_col:
                    selected_count = value
                    break
        
        selected_prob = (selected_count / total_shots) * 100 if total_shots > 0 else 0
        report.append(f"  Measurement Count: {selected_count} / {total_shots}")
        report.append(f"  Probability: {selected_prob:.2f}%")
        report.append("")
    
    report.append("="*80)
    report.append("")
    
    return "\n".join(report)

