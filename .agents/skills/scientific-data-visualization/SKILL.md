---
name: scientific-data-visualization
description: >-
  Expert data scientist and scientific visualization designer for academic papers, book chapters, and doctoral dissertations in AI, Machine Learning, and XAI.
  Translates complex mathematical formulations, geometric proofs, and empirical evaluation frameworks into high-impact, publication-grade pedagogical diagrams and plots.
---

# Scientific Data Visualization & Didactic Diagramming

## Overview

The `scientific-data-visualization` skill provides a comprehensive methodology for transforming abstract mathematical formulations, high-dimensional machine learning mechanics, and rigorous empirical benchmarks into clear, publication-grade scientific graphics.

It bridges the gap between formal algebra (equations, loss functions, optimization bounds) and human cognitive intuition (spatial geometry, force balances, topology, probability densities).

---

## The 4 Foundational Pillars of Scientific Visualization

### 1. Mathematical-to-Geometric Translation
Every mathematical abstraction in machine learning has a physical or geometric interpretation:
* **Kernels & Metric Weights** ($\pi_x(z) = \exp(-D^2/\sigma^2)$): Represent as radial heatmaps, intensity contours, or focal spotlights radiating from the query point $x$.
* **Optimization & Loss Landscapes** ($\arg\min \mathcal{L} + \Omega$): Represent as 2D/3D topological contour lines, gradient flow vectors, and regularized sparsity constraints (L1 diamond vs. L2 circle).
* **Game-Theoretic Coalitions** (Shapley $\phi_i$): Represent as directed sub-coalition hypercubes/lattices, permutation paths, or cumulative contribution waterfall plots.
* **Boolean Invariance & PAC Bounds** (Anchors $\text{prec}(A)$, $\text{cov}(A)$): Represent as axis-aligned hyper-rectangles (bounding boxes) enclosing homogeneous decision regions in feature space.
* **Multi-Objective Pareto Trade-offs** ($\min \mathcal{L} + \lambda_1 \text{dist} - \lambda_2 \det(\mathbf{K})$): Represent as balance-of-forces diagrams (repulsion vectors, proximity attraction springs, boundary crossing thresholds) and Pareto efficient frontiers.
* **Non-Parametric Statistical Inference** (Friedman $\chi_F^2$, Nemenyi $CD$): Represent as Demšar critical difference ranking axes with horizontal indifference bars.

### 2. Dual Coding & Cognitive Load Optimization
* **Direct Labeling vs. Legend Hunting:** Label lines, curves, and regions directly on the graphic instead of forcing the reader to scan back and forth between the plot and a remote legend.
* **Micro-Macro Design (Tufte):** Present the macroscopic pattern clearly at a glance (e.g., the global decision boundary), while encoding detailed microscopic data upon closer inspection (e.g., individual perturbed points and their local weights).
* **Step-by-Step Mechanism Decomposition:** When an algorithm executes multiple phases (e.g., Perturb $\to$ Black-Box Inference $\to$ Kernel Weighting $\to$ Lasso Fit), use a unified multi-panel storyboard showing the evolution of the feature space.

### 3. Dual-Format Delivery (Color Digital & High-Contrast Print B/W)
Scientific publications are read in PDF/tablets (color) and printed in conference/book proceedings (grayscale):
* **Color Edition:** Curated accessible palettes (e.g., Okabe-Ito, ColorBrewer, Viridis, Plasma, or deep scientific teal/indigo/coral). Avoid raw primary primaries.
* **Monochrome Edition:** Do not rely solely on grayscale lightness. Use distinct geometric markers (`o`, `s`, `^`, `D`), varied line styles (solid, dashed, dotted, dash-dot), and hatching patterns (`/`, `\\`, `x`, `+`, `o`) for area fills.

### 4. APA 7 & Publication Typography Standards
* **Callout Precedence:** Every graphic must be referenced in the text before its visual appearance.
* **Self-Contained Caption Architecture:**
  * Title/Number: `Figura X. Título descriptivo.`
  * Content explanation: Explanation of glyphs, axes, dashed lines, and markers.
  * Data/Theory Provenance: `Fuente: elaboración propia a partir de Autor (Año) / resultados del benchmark EXP...`
* **Vector Master & High-Res Export:** Generate source assets as vector graphics (`.svg`, `.pdf`) for infinite scalability, alongside 300+ DPI raster outputs (`.png`).

---

## Python Visualization Pipeline

When generating figures programmatically, adhere to:
* Consistent typographical hierarchy: Title (12-14 pt bold), Axis labels (10-11 pt), Tick labels (9-10 pt), In-chart annotations (8-9 pt).
* Clean styling: Despine top and right borders (`sns.despine()`), subtle alpha gridlines (`alpha=0.25`), and mathematical labels rendered via LaTeX math mode (`r"$f(x)$"`).
