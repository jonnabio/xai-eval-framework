"""Reliability metrics for EXP4 LLM judge consistency and inter-rater agreement."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats


class ICC:
    """Intraclass Correlation Coefficient (ICC) computation."""

    @staticmethod
    def icc_2_1(
        data: pd.DataFrame,
        judge_col: str = "judge_model",
        case_col: str = "case_id",
        score_col: str,
    ) -> Dict[str, float]:
        """
        Compute ICC(2,1): two-way mixed effects, absolute agreement, single rater.
        
        Used for evaluating consistency across judges rating the same cases.
        
        ICC(2,1) interpretation:
        - > 0.75: Excellent agreement
        - 0.60-0.75: Good agreement
        - 0.40-0.59: Fair agreement
        - < 0.40: Poor agreement
        
        Args:
            data: DataFrame with judge_col, case_col, score_col
            judge_col: Column name for judge identifier
            case_col: Column name for case identifier
            score_col: Column name for score (ordinal 1-5)
        
        Returns:
            Dictionary with ICC(2,1) value and confidence intervals
        """
        # Pivot: rows=cases, columns=judges, values=scores
        pivot = data.pivot_table(index=case_col, columns=judge_col, values=score_col, aggfunc="mean")
        
        if pivot.shape[0] < 2 or pivot.shape[1] < 2:
            return {"icc_2_1": np.nan, "ci_lower": np.nan, "ci_upper": np.nan, "n_cases": pivot.shape[0]}
        
        k = pivot.shape[1]  # number of judges
        n = pivot.shape[0]  # number of cases
        
        # Grand mean
        grand_mean = pivot.values.mean()
        
        # Between-cases mean square (BMS)
        case_means = pivot.mean(axis=1)
        bms = k * np.sum((case_means - grand_mean) ** 2) / (n - 1)
        
        # Within-cases mean square (WMS)
        wms = np.sum((pivot.values - case_means.values[:, np.newaxis]) ** 2) / (n * (k - 1))
        
        # ICC(2,1)
        icc = (bms - wms) / (bms + (k - 1) * wms)
        
        # Confidence interval (95%) via Fisher Z-transformation
        r = icc
        if -1 < r < 1:
            z = 0.5 * np.log((1 + r) / (1 - r))
            se_z = 1 / np.sqrt(n - 3)
            z_crit = 1.96
            ci_z_lower = z - z_crit * se_z
            ci_z_upper = z + z_crit * se_z
            ci_lower = (np.exp(2 * ci_z_lower) - 1) / (np.exp(2 * ci_z_lower) + 1)
            ci_upper = (np.exp(2 * ci_z_upper) - 1) / (np.exp(2 * ci_z_upper) + 1)
        else:
            ci_lower = ci_upper = np.nan
        
        return {
            "icc_2_1": icc,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "n_cases": n,
            "n_judges": k,
        }

    @staticmethod
    def icc_per_dimension(
        scores_df: pd.DataFrame,
        dimensions: List[str],
        judge_col: str = "judge_model",
        case_col: str = "case_id",
    ) -> pd.DataFrame:
        """Compute ICC(2,1) for each score dimension."""
        results = []
        for dim in dimensions:
            icc_dict = ICC.icc_2_1(scores_df, judge_col=judge_col, case_col=case_col, score_col=dim)
            results.append({
                "dimension": dim,
                **icc_dict,
            })
        return pd.DataFrame(results)


class KrippendorffAlpha:
    """Krippendorff's alpha for inter-rater agreement on ordinal data."""

    @staticmethod
    def alpha_ordinal(
        data: pd.DataFrame,
        judge_col: str = "judge_model",
        case_col: str = "case_id",
        score_col: str,
        min_val: int = 1,
        max_val: int = 5,
    ) -> Dict[str, float]:
        """
        Compute Krippendorff's alpha for ordinal agreement.
        
        Alpha interpretation:
        - 0.81-1.00: Excellent agreement
        - 0.61-0.80: Good agreement
        - 0.41-0.60: Moderate agreement
        - 0.21-0.40: Fair agreement
        - 0.00-0.20: Slight agreement
        - < 0.00: Poor agreement
        
        Args:
            data: DataFrame with judge_col, case_col, score_col
            min_val, max_val: Scale boundaries (for distance metric)
        
        Returns:
            Dictionary with alpha and confidence interval
        """
        # Pivot: rows=cases, columns=judges, values=scores
        pivot = data.pivot_table(index=case_col, columns=judge_col, values=score_col, aggfunc="mean")
        
        if pivot.shape[0] < 2 or pivot.shape[1] < 2:
            return {"krippendorff_alpha": np.nan, "n_cases": pivot.shape[0]}
        
        # Ordinal distance metric (Krippendorff's delta for ordinal data)
        # delta(c, k) = ((c - k) / (max_val - min_val)) ^ 2
        
        data_matrix = pivot.values  # n_cases × n_judges
        n_cases = data_matrix.shape[0]
        n_judges = data_matrix.shape[1]
        n_total = np.sum(~np.isnan(data_matrix))
        
        # Observed disagreement
        d_o = 0
        count = 0
        for i in range(n_cases):
            row = data_matrix[i][~np.isnan(data_matrix[i])]
            for j_idx, j_val in enumerate(row):
                for k_idx in range(j_idx + 1, len(row)):
                    k_val = row[k_idx]
                    delta = ((j_val - k_val) / (max_val - min_val)) ** 2
                    d_o += delta
                    count += 1
        
        if count > 0:
            d_o = d_o / count
        
        # Expected disagreement
        # Flatten all non-NaN values and compute marginals
        flat_data = data_matrix[~np.isnan(data_matrix)]
        n = len(flat_data)
        
        d_e = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                delta = ((flat_data[i] - flat_data[j]) / (max_val - min_val)) ** 2
                d_e += delta
        
        if n > 1:
            d_e = d_e / (n * (n - 1) / 2)
        
        # Krippendorff's alpha
        if d_e == 0:
            alpha = 1.0 if d_o == 0 else 0.0
        else:
            alpha = 1 - (d_o / d_e)
        
        return {
            "krippendorff_alpha": alpha,
            "observed_disagreement": d_o,
            "expected_disagreement": d_e,
            "n_cases": n_cases,
            "n_judges": n_judges,
        }

    @staticmethod
    def alpha_per_dimension(
        scores_df: pd.DataFrame,
        dimensions: List[str],
        judge_col: str = "judge_model",
        case_col: str = "case_id",
        min_val: int = 1,
        max_val: int = 5,
    ) -> pd.DataFrame:
        """Compute Krippendorff's alpha for each score dimension."""
        results = []
        for dim in dimensions:
            alpha_dict = KrippendorffAlpha.alpha_ordinal(
                scores_df, judge_col=judge_col, case_col=case_col, score_col=dim,
                min_val=min_val, max_val=max_val
            )
            results.append({
                "dimension": dim,
                **alpha_dict,
            })
        return pd.DataFrame(results)


class MultiJudgeComparison:
    """Multi-judge comparison and disagreement analysis."""

    @staticmethod
    def judge_disagreement_matrix(
        scores_df: pd.DataFrame,
        dimensions: List[str],
        case_col: str = "case_id",
        judge_col: str = "judge_model",
    ) -> pd.DataFrame:
        """
        Compute disagreement (std dev) across judges per case and dimension.
        
        Returns ranked dataframe of high-disagreement cases for human validation.
        """
        results = []
        
        for case_id in scores_df[case_col].unique():
            case_data = scores_df[scores_df[case_col] == case_id]
            
            for dim in dimensions:
                scores_by_judge = case_data.groupby(judge_col)[dim].mean()
                
                if len(scores_by_judge) < 2:
                    continue
                
                std_dev = scores_by_judge.std()
                mean_score = scores_by_judge.mean()
                
                results.append({
                    "case_id": case_id,
                    "dimension": dim,
                    "disagreement_std": std_dev,
                    "mean_score": mean_score,
                    "n_judges": len(scores_by_judge),
                })
        
        df = pd.DataFrame(results)
        
        # Aggregate disagreement per case (mean across dimensions)
        case_disagreement = df.groupby("case_id")["disagreement_std"].mean().reset_index()
        case_disagreement.columns = ["case_id", "avg_disagreement_std"]
        case_disagreement = case_disagreement.sort_values("avg_disagreement_std", ascending=False)
        
        return case_disagreement

    @staticmethod
    def judge_comparison_summary(
        scores_df: pd.DataFrame,
        dimensions: List[str],
        judge_col: str = "judge_model",
        groupby_cols: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Generate summary table: per-judge mean/std for each dimension.
        
        Useful for identifying divergent judges or conditions.
        """
        if groupby_cols is None:
            groupby_cols = [judge_col]
        
        results = []
        
        for group_vals, group_df in scores_df.groupby(groupby_cols):
            if not isinstance(group_vals, tuple):
                group_vals = (group_vals,)
            
            group_dict = dict(zip(groupby_cols, group_vals))
            
            for dim in dimensions:
                if dim in group_df.columns:
                    mean_val = group_df[dim].mean()
                    std_val = group_df[dim].std()
                    
                    results.append({
                        **group_dict,
                        "dimension": dim,
                        "mean_score": mean_val,
                        "std_score": std_val,
                        "n_judgments": len(group_df),
                    })
        
        return pd.DataFrame(results)
