# ML Detection Data Analysis

A comprehensive comparative study analyzing human versus human-in-the-loop machine learning detection systems across seven hardware object categories.

## 📋 Project Overview

This repository contains the complete data analysis for a research study examining the performance differences between pure human object detection and AI-assisted (human-in-the-loop) detection systems. The study challenges conventional assumptions about AI assistance universally improving human performance.

### Key Research Question
**Does AI assistance always improve human performance in object detection tasks?**

**Spoiler Alert**: The answer is more complex than you might think! 🤔

## 🎯 Key Findings

### 🏆 The Accuracy Paradox
- **Humans outperformed AI-assisted systems in 5 out of 7 object types**
- Accuracy improvements ranged from 3% to 17 percentage points
- Only nails showed the expected pattern where AI helped (44% → 89% accuracy)

### ⚡ Speed Trade-offs
- **AI assistance provided speed benefits in only 4 out of 7 cases**
- Best AI performance: Washers (46% faster) and Nuts (45% faster)  
- Worst AI performance: Black screws (31% slower) and Nails (51% slower)

### 🔍 Quality Control Reality Check
- **Humans consistently superior at defect detection**
- Human advantage ranges from 14% to 128% more defects detected
- AI systems missed 30-60% of actual defects in complex objects

## 📊 Dataset Overview

### Objects Tested
- **Black screws** - Complex, irregular shapes
- **Long screws** - Cylindrical, medium complexity  
- **Nails** - Linear, challenging orientations
- **Nuts** - Uniform, geometric shapes
- **Rivets** - Small, consistent form factor
- **Tek-screws** - Variable threading patterns
- **Washers** - Simple, circular objects

### Experimental Design
- **280 total observations** (20 rounds × 7 objects × 2 systems)
- **Controlled testing environment** with standardized procedures
- **Three performance metrics**: Accuracy, Efficiency (time), Defect Detection

## 📈 Visualizations

### Time Performance Analysis
![Time per Round boxplot chart showing efficiency comparison across object types](Total_Seconds_Per_Round_boxplot.png)

**Key Insights**: AI-assisted systems show more consistent timing but aren't always faster.

### Accuracy Distribution Analysis  
![Accuracy per Round boxplot chart showing detection accuracy patterns](Accuracy_per_Round_boxplot.png)

**Key Insights**: Humans demonstrate tight accuracy distributions except for nails, where AI provides crucial assistance.

### Defect Detection vs Ground Truth
![INSERT: Defect detection bar chart with ground truth comparison lines](Defects_Observed_BarPlot.png)

**Key Insights**: Humans achieve near-perfect alignment with ground truth while AI systematically under-detects defects.

## 🔬 Statistical Analysis

### Methodology
- **Independent samples t-tests** for significance testing
- **Cohen's d effect sizes** for practical significance assessment
- **Robust statistical power** with n=20 per condition

### Significance Results
- **15 out of 18 comparisons** showed statistical significance (p < 0.05)
- **Effect sizes predominantly large to huge** (Cohen's d > 0.8)
- **Strongest effects**: Rivet accuracy (d = 4.25), Tek-screw defect detection (d = 3.37)

*[INSERT: Statistical significance summary table or visualization]*

## 🏗️ Repository Structure

```
├── data/                          # Raw CSV files for each object/system combination
│   ├── nail_AI.csv
│   ├── nail_human.csv
│   ├── tek-screw_AI.csv
│   └── ...
├── data_analysis.ipynb           # Main Jupyter notebook with complete analysis
├── script.py                     # Data processing and consolidation script
├── master_data.csv              # Consolidated dataset
├── summary_statistics.csv       # Descriptive statistics by group
├── statistical_test_results.csv # T-test results and effect sizes
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy scipy matplotlib seaborn missingno
```

### Running the Analysis
1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd mldetection_data_analysis
   ```

2. **Generate master dataset**
   ```bash
   python script.py
   ```

3. **Run complete analysis**
   ```bash
   jupyter notebook data_analysis.ipynb
   ```

## 📋 Analysis Pipeline

### 1. Data Preprocessing (`script.py`)
- **Robust CSV parsing** handles varying metadata and footer notes
- **Time calculation** from Min:Sec:Centiseconds to total seconds
- **Ground truth integration** with defect counts and object totals
- **Notes extraction** capturing qualitative observations

### 2. Exploratory Data Analysis
- **Missing value analysis** and data quality assessment
- **Descriptive statistics** by item and system type
- **Distribution visualizations** for all key metrics

### 3. Statistical Testing
- **Independent samples t-tests** for group comparisons
- **Effect size calculations** using Cohen's d
- **Multiple comparison considerations** with Bonferroni adjustments

### 4. Results Interpretation
- **Performance trade-off analysis** between accuracy, speed, and quality
- **Object-specific insights** identifying optimal use cases
- **Practical recommendations** for system selection

## 🎯 Practical Implications

### ✅ Use AI Assistance For:
- **Simple, uniform objects** (washers, nuts)
- **Speed-prioritized tasks** where minor accuracy loss is acceptable
- **High-volume, repetitive operations**

### ❌ Stick with Human-Only For:
- **Complex or irregular objects** (black screws, tek-screws, rivets)
- **Quality-critical applications** requiring defect detection
- **Tasks where accuracy is non-negotiable**

### 🔄 Hybrid Approach:
- **Pre-sort objects by complexity** before system assignment
- **Use AI for initial screening, humans for quality control**
- **Leverage AI consistency for workflow planning**

## 📚 Research Context

This work contributes to the growing literature on human-AI collaboration by:

1. **Challenging the "AI always helps" assumption** with empirical evidence
2. **Identifying context-dependent factors** that determine AI assistance effectiveness  
3. **Providing practical frameworks** for optimal human-AI system selection
4. **Highlighting quality control implications** of AI-assisted detection systems

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Areas for Future Work
- **Environmental variation testing** (lighting, backgrounds, orientations)
- **Extended object complexity analysis** with additional hardware types
- **Fatigue effect studies** over longer experimental sessions
- **Hybrid workflow optimization** combining both system strengths

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions about this research or potential collaborations, please reach out:
- **Email**: [your-email]
- **LinkedIn**: [your-linkedin]
- **Research Gate**: [your-researchgate]

## 📖 Citation

If you use this work in your research, please cite:

```bibtex
@misc{mldetection2024,
  title={Human vs. Human-in-the-Loop Machine Learning Detection: A Comparative Analysis},
  author={[Your Name]},
  year={2024},
  url={[repository-url]}
}
```

---

**🧠 Remember**: The best AI system isn't always the most advanced one - it's the one that's appropriately matched to the task at hand!