# ADR-047a: Visualization Library Selection

## Status
Accepted

## Context
For **EXP1-47** (Dashboard Integration), we need to visualize complex metrics including:
- Radar charts for comparing multivariable explainability scores (Fidelity, Stability, etc.).
- Bar charts for feature importance.
- Line/Scatter plots for sensitivity analysis.

The frontend is built with Next.js and Tailwind CSS. We need a library that balances performance (bundle size), TypeScript support, accessibility, and customization.

## Options Considered

### 1. Recharts
- **Pros**:
    - Built on top of SVG elements, very flexible.
    - Excellent React integration (component-based).
    - Good TypeScript support.
    - Lightweight core.
    - Native RadarChart support.
- **Cons**:
    - Can be tricky to animate complex transitions.
    - Default aesthetics are basic (requires styling).

### 2. Nivo
- **Pros**:
    - Built on top of D3, extremely powerful.
    - Beautiful default themes.
    - strong Accessibility focus.
    - "Motion" support (animations).
- **Cons**:
    - Larger bundle size (unless tree-shaken carefully).
    - API surface is massive and sometimes complex.
    - Canvas vs SVG implementations can be confusing.

### 3. Chart.js (react-chartjs-2)
- **Pros**:
    - Canvas-based (good for rendering thousands of points).
    - Familiar API for many devs.
- **Cons**:
    - Not fully "React-native" (imperative wrapper).
    - Harder to customize individual SVG elements.
    - Radar chart exists but styling is rigid.

## Decision
We will use **Recharts**.

## Rationale
1.  **Component Composition**: Recharts uses a composable API (`<RadarChart><PolarGrid /><Radar /></RadarChart>`) that fits perfectly with our modular component strategy.
2.  **TypeScript**: First-class TS support ensures type safety for our new `MetricSet` interfaces.
3.  **Bundle Size**: Lighter than Nivo/D3 for our specific needs (we don't need complex D3 geo/network layouts).
4.  **Radar Support**: Recharts has a robust Radar implementation which is the primary visualization for the thesis comparison graphics.

## Consequences
- We will install `recharts`.
- We need to create a `ChartExporter` utility manually if we want PNG export (since Recharts is SVG, this is standard via canvas rasterization).
- We will need to implement custom tooltips to match our Tailwind design system.
