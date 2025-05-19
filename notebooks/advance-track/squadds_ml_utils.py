import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import MultiTaskLassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import plot_tree


class DesignToHamiltonianAnalyzer:
    def __init__(self, X_design, Y_hamiltonian, design_labels, hamiltonian_labels):
        """
        Initialize the analyzer with design inputs and Hamiltonian outputs.
        """
        self.X_raw = X_design
        self.Y_raw = Y_hamiltonian
        self.design_labels = design_labels
        self.hamiltonian_labels = hamiltonian_labels

        self.scaler_X = StandardScaler()
        self.scaler_Y = StandardScaler()

        self.X = self.scaler_X.fit_transform(self.X_raw)
        self.Y = self.scaler_Y.fit_transform(self.Y_raw)

    def run_random_forest(self, n_estimators=200, random_state=42):
        """
        Trains a random forest for each Hamiltonian parameter.
        Stores and returns a feature importance DataFrame.
        """
        importance_matrix = np.zeros((self.X.shape[1], self.Y.shape[1]))

        for i, h_name in enumerate(self.hamiltonian_labels):
            rf = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
            rf.fit(self.X, self.Y[:, i])
            importance_matrix[:, i] = rf.feature_importances_

        self.rf_importance_df = pd.DataFrame(importance_matrix,
                                             index=self.design_labels,
                                             columns=self.hamiltonian_labels)
        return self.rf_importance_df

    def run_multitask_lasso(self, alpha_grid=np.logspace(-4, 1, 20)):
        """
        Trains a multi-task Lasso model.
        Stores and returns the coefficient matrix as DataFrame.
        """
        model = MultiTaskLassoCV(alphas=alpha_grid, cv=5, random_state=42)
        model.fit(self.X, self.Y)
        coef_matrix = model.coef_.T  # (n_design, n_hamiltonian)

        self.lasso_coef_df = pd.DataFrame(coef_matrix,
                                          index=self.design_labels,
                                          columns=self.hamiltonian_labels)
        return self.lasso_coef_df

    def plot_heatmaps(self):
        """
        Plots side-by-side heatmaps of RF and Lasso results.
        """
        fig, axs = plt.subplots(1, 2, figsize=(16, 6))

        sns.heatmap(self.rf_importance_df,
                    annot=True, cmap="YlOrRd", ax=axs[0], cbar_kws={'label': 'Feature Importance'})
        axs[0].set_title("Random Forest: Design Parameter Importance")
        axs[0].set_xlabel("Hamiltonian Parameter")
        axs[0].set_ylabel("Design Parameter")

        sns.heatmap(self.lasso_coef_df,
                    annot=True, center=0, cmap="coolwarm", ax=axs[1], cbar_kws={'label': 'Coefficient Value'})
        axs[1].set_title("Multi-Task Lasso: Design Influence")
        axs[1].set_xlabel("Hamiltonian Parameter")
        axs[1].set_ylabel("Design Parameter")

        plt.tight_layout()
        plt.show()

    def print_dependency_summary(self, top_k=3, threshold=1e-3):
        """
        Prints top-k most important design variables per Hamiltonian parameter
        from both Random Forest and Lasso results.
        """
        print("\n=== Top Influencers from Random Forest ===")
        for h in self.hamiltonian_labels:
            top = self.rf_importance_df[h].sort_values(ascending=False)
            print(f"\n- {h}:")
            for i in range(top_k):
                print(f"    • {top.index[i]} → importance = {top.values[i]:.4f}")

        print("\n=== Top Influencers from Lasso (with direction) ===")
        for h in self.hamiltonian_labels:
            top = self.lasso_coef_df[h].abs().sort_values(ascending=False)
            print(f"\n- {h}:")
            for i in range(top_k):
                param = top.index[i]
                coef = self.lasso_coef_df[h][param]
                print(f"    • {param} → coef = {coef:.4f} ({'↑' if coef > 0 else '↓'})")

    def plot_heatmap(self):
        """
        Plots a single heatmap depending on which model was run.
        If both are run, plots both side by side.
        If only one is run, plots only that one.
        """
        has_rf = hasattr(self, 'rf_importance_df')
        has_lasso = hasattr(self, 'lasso_coef_df')

        if has_rf and has_lasso:
            self.plot_heatmaps()
        elif has_rf:
            plt.figure(figsize=(8, 6))
            sns.heatmap(self.rf_importance_df, annot=True, cmap="YlOrRd", cbar_kws={'label': 'Feature Importance'})
            plt.title("Random Forest: Design Parameter Importance")
            plt.xlabel("Hamiltonian Parameter")
            plt.ylabel("Design Parameter")
            plt.tight_layout()
            plt.show()
        elif has_lasso:
            plt.figure(figsize=(8, 6))
            sns.heatmap(self.lasso_coef_df, annot=True, center=0, cmap="coolwarm", cbar_kws={'label': 'Coefficient Value'})
            plt.title("Multi-Task Lasso: Design Influence")
            plt.xlabel("Hamiltonian Parameter")
            plt.ylabel("Design Parameter")
            plt.tight_layout()
            plt.show()
        else:
            raise ValueError("Neither Random Forest nor Lasso results are available. Run one of the analysis methods first.")

    def get_dependency_summary_json(self, top_k=3, threshold=1e-3, pretty_print=True):
        """
        Returns a JSON-like dict of top design parameters (and their scores) for each Hamiltonian parameter.
        Only includes parameters with absolute score above the threshold.
        If both models are run, returns both. Otherwise, returns only the available one.
        If pretty_print is True, also prints the summary in a human-readable format.
        """
        summary = {}
        if hasattr(self, 'rf_importance_df'):
            rf_summary = {}
            for h in self.hamiltonian_labels:
                top = self.rf_importance_df[h].sort_values(ascending=False)
                filtered = [
                    {"parameter": top.index[i], "importance": float(top.values[i])}
                    for i in range(len(top))
                    if abs(top.values[i]) >= threshold
                ][:top_k]
                rf_summary[h] = filtered
            summary['random_forest'] = rf_summary
        if hasattr(self, 'lasso_coef_df'):
            lasso_summary = {}
            for h in self.hamiltonian_labels:
                top = self.lasso_coef_df[h].abs().sort_values(ascending=False)
                filtered = [
                    {
                        "parameter": top.index[i],
                        "coef": float(self.lasso_coef_df[h][top.index[i]])
                    }
                    for i in range(len(top))
                    if abs(top.values[i]) >= threshold
                ][:top_k]
                lasso_summary[h] = filtered
            summary['lasso'] = lasso_summary

        if pretty_print:
            print("\n=== Dependency Summary (Top {} per Hamiltonian parameter, threshold={}) ===".format(top_k, threshold))
            print(json.dumps(summary, indent=4))

        return summary
