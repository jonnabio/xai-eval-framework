# Human Annotation Guidelines for XAI Evaluation

## 1. Research Goal
We are evaluating how "good" different AI explanation methods (LIME, SHAP) are. We want to know if these explanations actually help users understand the model's decisions, or if they are confusing/misleading.

Your goal is to rate the **quality of the explanation**, NOT whether the model's prediction was correct.

## 2. The Task
You will be shown 20 instances from the "Adult Income" dataset (predicting if income > $50K).
For each instance, you will see:
1.  **Prediction**: What the model predicted (e.g., ">50K").
2.  **Explanation**: A bar chart showing which features (Age, Marital Status, Capital Gain etc.) influenced that prediction.
    -   **Green bars**: Pushed the prediction towards >50K.
    -   **Red bars**: Pushed the prediction towards <=50K.

## 3. Rating Dimensions
Please rate each explanation on these 3 scales (1-5):

### A. Coherence (Is it logical?)
Does the explanation make sense to you as a human?
*   **1 (Very Poor)**: Contradictory, confusing, or highlights irrelevant features (e.g., "fnlwgt" or random noise).
*   **3 (Average)**: Mostly understandable but some features seem odd.
*   **5 (Excellent)**: Completely logical causal story (e.g., "Capital Gain" and "Education" cleanly explain high income).

### B. Faithfulness (Is it true?)
Does this explanation seem to reflect how the model *actually* reasoned?
*   *Note: This is hard to judge without seeing the model internals, so use your intuition about the feature importance.*
*   **1 (Very Poor)**: The top features seem trivial, yet the model was very confident. Something is hidden.
*   **5 (Excellent)**: The features shown clearly account for the prediction (e.g., strong Capital Loss explaining a low income classification).

### C. Usefulness (Is it helpful?)
If you were a loan officer using this AI, would this explanation help you trust/verify the decision?
*   **1 (Very Poor)**: "This tells me nothing."
*   **5 (Excellent)**: "This gives me the exact insight I need to verify the decision."

## 4. Instructions
1.  Open `tools/human_annotation_viewer.html` in Chrome/Firefox.
2.  Click **"Load Samples.json"** and select `experiments/exp1_adult/human_eval/samples.json`.
3.  Go through all 20 samples.
4.  Provide ratings for all 3 dimensions.
5.  Click **"Export Annotations"** when finished.
6.  Send the `annotations_....json` file to the research lead.

## 5. Time Estimate
It should take approximately **3-5 minutes per instance**, or ~1.5 hours total.
