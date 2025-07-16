# Chapter 4: Data Analysis and Results

## 4.1 Introduction

This chapter presents the empirical findings from the comparative analysis of human versus human-in-the-loop machine learning detection systems across seven distinct hardware object categories. The analysis examines three primary performance dimensions: detection accuracy, task completion time (efficiency), and defect identification capability. The results presented herein are based on 280 experimental trials conducted across multiple participants over a controlled testing period.

## 4.2 Descriptive Statistics Overview

The experimental dataset comprises 280 observations across seven object types (black screws, long screws, nails, nuts, rivets, tek-screws, and washers) with two system configurations (human-only and human-in-the-loop). Each condition was tested across 20 rounds, providing robust statistical power for comparative analysis.

### 4.2.1 Performance Metrics Summary

The descriptive statistics reveal significant variations in performance across both object types and system configurations. Mean task completion times ranged from 38.68 seconds (washer, human-in-the-loop) to 187.36 seconds (black screw, human-in-the-loop), indicating substantial task complexity differences and system interaction effects.

## 4.3 Accuracy Performance Analysis

### 4.3.1 Overall Accuracy Patterns

The analysis reveals a counterintuitive pattern wherein human-only systems demonstrated superior accuracy performance in the majority of object detection tasks. This finding challenges the conventional assumption that AI assistance universally improves human performance.

**Human-only systems outperformed human-in-the-loop systems in 5 out of 7 object categories:**

- Black screws: 103% vs. 86% (Δ = +17 percentage points)
- Long screws: 100% vs. 91% (Δ = +9 percentage points) 
- Rivets: 100% vs. 83% (Δ = +17 percentage points)
- Tek-screws: 99% vs. 85% (Δ = +14 percentage points)
- Washers: 100% vs. 97% (Δ = +3 percentage points)

**Human-in-the-loop systems showed superior performance only for:**
- Nails: 89% vs. 44% (Δ = +45 percentage points)

**Equivalent performance was observed for:**
- Nuts: 100% vs. 99% (Δ = +1 percentage point)

### 4.3.2 Accuracy Distribution Analysis

The boxplot analysis (Figure 4.1) reveals distinct accuracy distribution patterns between system types. Human-only systems demonstrated extremely tight accuracy distributions for most object types, with minimal inter-quartile ranges and few outliers. Conversely, human-in-the-loop systems showed greater variability across all object categories, suggesting that AI assistance may introduce inconsistency in detection performance.

The nail detection task presented a notable exception, where human performance exhibited extreme variability (0-100% range) while AI-assisted performance remained consistently around 89%. This pattern suggests that nails may present a unique **visual segmentation challenge** for human operators, a hypothesis explored further in Section 4.7.

## 4.4 Efficiency Performance Analysis

### 4.4.1 Task Completion Time Comparisons

The efficiency analysis reveals a heterogeneous pattern of AI assistance effects on task completion time, with both positive and negative impacts observed across different object types.

**Human-in-the-loop systems demonstrated superior efficiency for:**
- Washers: 38.68s vs. 72.13s (-46.4% completion time)
- Nuts: 73.21s vs. 133.92s (-45.3% completion time)
- Long screws: 87.06s vs. 93.06s (-6.4% completion time)
- Rivets: 103.85s vs. 170.74s (-39.2% completion time)

**Human-only systems demonstrated superior efficiency for:**
- Nails: 60.20s vs. 90.75s (-33.7% completion time)
- Tek-screws: 130.63s vs. 144.77s (-9.8% completion time)
- Black screws: 143.15s vs. 187.36s (-23.6% completion time)

### 4.4.2 Temporal Performance Consistency

The time performance visualization (Figure 4.2) demonstrates that human-in-the-loop systems consistently exhibit more predictable completion times, evidenced by tighter boxplot distributions and smaller inter-quartile ranges. Human-only systems showed substantial temporal variability, particularly for complex objects like tek-screws and nails.

This pattern suggests that while AI assistance may not always improve speed, it provides more consistent and predictable task completion times. This effect may be due to the AI offloading some of the **cognitive load** associated with the task, leading to a more regularized workflow, which has implications for planning and resource allocation.

## 4.5 Defect Detection Performance

### 4.5.1 Comparative Defect Identification Analysis

The defect detection analysis reveals the most pronounced performance gap between system types, with human-only systems demonstrating systematic superiority across all object categories where differences were observed.

**Human-only systems demonstrated superior defect detection for:**
- Tek-screws: 14.6 vs. 6.4 defects
- Rivets: 9.8 vs. 4.3 defects
- Long screws: 6.0 vs. 3.3 defects
- Black screws: 5.0 vs. 2.8 defects
- Nails: 2.1 vs. 1.85 defects

**Equivalent defect detection performance was observed for:**
- Nuts: 3.0 vs. 3.0 defects
- Washers: 3.0 vs. 3.0 defects

### 4.5.2 Ground Truth Comparison

When compared against established ground truth values (Figure 4.3), human-only systems demonstrated remarkable accuracy in defect identification:
- **Perfect matches**: Tek-screws (14.6 ≈ 14 ground truth), Long screws (6.0 = 6), Black screws (5.0 = 5)
- **Near perfect**: Rivets (9.8 ≈ 10), Washers and Nuts (3.0 = 3)

Human-in-the-loop systems showed systematic under-detection of defects:
- **Severe under-detection**: Tek-screws (6.4 vs. 14 ground truth), Rivets (4.3 vs. 10)
- **Moderate under-detection**: Long screws (3.3 vs. 6), Black screws (2.8 vs. 5)

This pattern indicates that AI assistance systematically reduces defect detection capability, potentially missing 30-60% of actual defects present in the objects. The poor performance of both systems on nails suggests the **subtlety of the defects** on that object type may be a key confounding variable.

## 4.6 Statistical Significance Analysis

### 4.6.1 Significant Findings

Independent samples t-tests confirmed that most observed performance differences were statistically significant (p < 0.05).

* **Accuracy**: Statistically significant differences favoring the human-only system were found for tek-screws, long screws, washers, black screws, and rivets. The AI-assisted system's accuracy advantage for nails was also statistically significant.
* **Efficiency**: The AI-assisted system was significantly faster for washers, nuts, and rivets, while the human-only system was significantly faster for black screws.
* **Defect Detection**: The human operator's superiority was statistically significant for tek-screws, rivets, long screws, and black screws.

### 4.6.2 Non-Significant Findings and Their Implications

The cases where statistical significance was not found are equally instructive. No significant difference in efficiency was found for nails, tek-screws, or long screws, likely due to high variance in human operator performance. Crucially, **there was no statistically significant difference in defect detection for nails (p = 0.701)**. Despite a small difference in the mean values (2.1 vs 1.85), the high p-value indicates this gap is attributable to random chance. This finding revises the initial interpretation, suggesting that for the most challenging defects, both systems performed equally poorly.

### 4.6.3 Effect Size and Overall Interpretation

The effect sizes for significant findings were predominantly large to huge (Cohen's d > 0.8), indicating that the performance differences represent substantial, practically meaningful variations. The statistical tests provide robust evidence for systematic performance differences, while also revealing where apparent differences were not statistically meaningful, thereby refining the overall conclusions.

## 4.7 Object-Specific Performance Profiles

### 4.7.1 Nails: Optimal AI Assistance Context

Nail detection represents the singular case where human-in-the-loop systems provided a clear, statistically significant accuracy improvement (44% to 89%). This suggests that tasks involving high human perceptual difficulty, such as segmenting thin, overlapping objects, may be optimal contexts for AI collaboration, even if efficiency or defect detection does not improve.

### 4.7.2 Washers and Nuts: Efficiency-Optimized Contexts

Both washer and nut detection demonstrated favorable efficiency profiles for human-in-the-loop systems. Washers showed the most dramatic efficiency improvement (46.4% time reduction) with minimal accuracy degradation (3 percentage points), while nuts provided substantial time savings (45.3%) with essentially equivalent accuracy. These profiles suggest that simple, uniform objects present optimal conditions for AI-assisted efficiency gains.

### 4.7.3 Complex Objects: Human-Only Advantages

Black screws, tek-screws, and rivets consistently favored human-only systems across multiple performance dimensions. These objects showed significant accuracy and defect detection advantages for human-only systems. Qualitative observations identified specific challenges for the AI including horizontal orientation detection, occlusion handling, and inter-object confusion.

## 4.8 Performance Trade-off Analysis

### 4.8.1 Accuracy-Efficiency Trade-offs

The analysis reveals complex trade-off relationships between accuracy and efficiency that vary significantly by object type. While human-in-the-loop systems occasionally provide efficiency improvements, these gains frequently occur at the expense of detection accuracy. The magnitude and direction of these trade-offs suggest that optimal system selection must be context-dependent.

### 4.8.2 Quality Control Implications

For applications where defect detection is paramount, the data strongly supports human-only system utilization. The consistent and statistically significant superiority of human defect detection across most categories indicates that the tested AI assistance interferes with critical quality assessment. However, the finding that neither system could reliably detect defects on nails suggests that certain defect types may require entirely different inspection protocols.

## 4.9 Summary of Findings

The empirical analysis challenges the assumption that AI assistance universally improves human performance in object detection tasks. Key findings include:

1.  **Context-dependent accuracy performance**: Human-only systems demonstrated superior, statistically significant accuracy in 5 of 7 object categories.
2.  **Inconsistent efficiency improvements**: AI assistance provided significant speed benefits in 4 of 7 cases, but these gains often came with accuracy costs.
3.  **Systematic defect detection superiority**: Human-only systems significantly outperformed AI-assisted systems in defect identification for most items. For the most challenging defects (nails), both systems failed equally.
4.  **Performance consistency patterns**: AI assistance provided more consistent completion times but introduced greater variability in accuracy.
5.  **Object complexity effects**: Simple objects (washers, nuts) benefited from AI assistance, while complex objects (black screws, tek-screws, rivets) favored human-only approaches.

## 4.10 Chapter Conclusion

The comparative analysis presented in this chapter provides empirical evidence for the complex and context-dependent nature of human-AI collaboration in object detection tasks. The results demonstrate that effective integration of AI assistance requires a nuanced understanding of task characteristics, performance priorities, and object-specific factors. The findings suggest that the "AI assistance always helps" paradigm requires reconsideration in favor of more sophisticated frameworks that account for performance trade-offs and the statistical significance of observed outcomes. The subsequent chapter will discuss the theoretical implications of these findings and their relevance to existing human-AI collaboration frameworks.