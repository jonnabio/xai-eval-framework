# EXP4 Human Validation Study: Annotator Guide

**Thank you for participating!** This guide will help you understand what we're asking and how to complete the task.

---

## Overview

You will rate **10 AI model explanations** on how useful and clear they are. This takes about **10-15 minutes total**.

Each explanation is being evaluated to understand whether AI systems produce explanations that humans find helpful.

---

## The 5 Questions You'll Answer

For each explanation, you'll answer **5 simple questions** on a scale of 1-5:

- **1** = Strongly Disagree
- **2** = Disagree
- **3** = Neutral/Unsure
- **4** = Agree
- **5** = Strongly Agree

### Question 1: Clarity
> "This explanation is easy to understand."

**What this means**: Is the explanation written in plain language? Could a person without a technical background understand it? Does it avoid jargon or explain technical terms?

**Example - CLEAR explanation**:
"The model decided 'Yes' because: The applicant had 10+ years work experience (high value), income was $80K/year (good), and age is 45 (neutral). Together these three things indicate financial stability."

**Example - UNCLEAR explanation**:
"Feature contributions: age=0.12, income=0.67, experience=0.89. Accumulated SHAP value = 1.68 > decision boundary."

---

### Question 2: **Completeness**
> "This explanation explains WHY the model made its decision."

**What this means**: Does the explanation address the actual reasons the model predicted this outcome? Does it answer "Why did it say Yes/No?" or does it just say "it said Yes/No"?

**Example - COMPLETE explanation**:
"The model predicted 'No' because the applicant's credit score was very low (210), which heavily influenced the decision. Additionally, the applicant had no prior employment history."

**Example - INCOMPLETE explanation**:
"The model classified this as: Negative."  
*(Just states the prediction, doesn't explain why)*

---

### Question 3: **Concision**
> "This explanation is concise and not overly wordy."

**What this means**: Is the explanation reasonably brief? Or does it ramble, repeat itself, or include unnecessary details?

**Example - CONCISE explanation**:
"The model said 'Yes' because: 30+ years experience (strong), income $150K (strong), age 62 (moderate negative). Net result: strongly positive."

**Example - WORDY explanation**:
"The model, having been trained on historical data, made a prediction, and that prediction was based on several factors. The first factor was experience: the applicant had many years of experience, specifically experience in the financial sector, which contributed to the decision. Additionally, the model considered income..."

---

### Question 4: **Semantic Plausibility**
> "This explanation makes practical sense in the real world."

**What this means**: Does the explanation make logical sense in the real world? Or does it give a reason that doesn't make sense? Would a reasonable person agree with this logic?

**Example - PLAUSIBLE explanation**:
"The model predicted 'approve loan' because: high income, stable employment, low debt-to-income ratio. These are real factors that affect loan risk."

**Example - IMPLAUSIBLE explanation**:
"The model predicted 'approve loan' because: hair color is brown. Applicant name has 5 letters."  
*(These reasons don't make logical sense for a loan decision)*

---

### Question 5: **Audit Usefulness**
> "I could use this explanation to check if the model decision is fair."

**What this means**: Does this explanation give you enough information to audit the model's decision? Could you check whether the model is being fair/biased? Or is the explanation too vague?

**Example - AUDIT-USEFUL explanation**:
"The model approved the loan based on: income ($90K), years employed (8), age (35), credit score (750). You can verify these factors independently in the applicant's file and check if the model weighted them fairly."

**Example - NOT AUDIT-USEFUL explanation**:
"The model approved the loan." *(No specific reasons, can't check fairness)*

---

## How the Form Works

1. You'll see **one explanation at a time**
2. For each explanation, you'll see:
   - **What the model predicted** (e.g., "The model predicts: YES")
   - **The explanation text** (the AI-generated reason)
   - **The 5 questions** with a 1-5 slider
3. You can add **optional comments** if you want to explain your rating
4. Click **Next** to go to the next explanation

---

## Example: A Complete Walkthrough

### Scenario
**Model Prediction**: "The model predicts this person qualifies for a credit card."

**Explanation**: "Key factors: Income is $65,000 annually (positive), credit history is 8 years (positive), and current credit score is 720 (positive). These three factors together indicate good creditworthiness."

### Your Ratings

| Question | Your Rating | Why? |
|----------|-------------|------|
| **Clarity**: Is it easy to understand? | **5 - Strongly Agree** | The explanation uses plain language (income, years, credit score) and connects them clearly. |
| **Completeness**: Does it explain why? | **4 - Agree** | It gives concrete reasons, though it could mention what "good creditworthiness" means exactly. |
| **Concision**: Is it brief? | **5 - Strongly Agree** | Three bullet points, no fluff. Very concise. |
| **Plausibility**: Does it make sense? | **5 - Strongly Agree** | Of course income, credit history, and credit score matter for credit decisions. This makes sense. |
| **Audit Usefulness**: Can you check fairness? | **4 - Agree** | You could verify all three factors in the applicant's file and check if they were weighted fairly. Clear and checkable. |

---

## Tips for Success

✅ **DO**:
- Answer honestly—there are no "right" answers
- Think about what would be useful to YOU if you received this explanation
- Rate what's on the page, not what you wish it said
- Take your time (1-2 min per explanation is normal)

❌ **DON'T**:
- Overthink it—your first instinct is usually good
- Try to be consistent with previous explanations (each is separate)
- Rate based on whether you agree with the model's prediction (rate the explanation quality, not the decision)
- Leave questions blank

---

## Questions or Issues?

If you encounter any technical problems or have questions:
1. Try refreshing the page
2. Contact: [Insert contact email]
3. If the form crashes, save your case ID and report it

---

## Your Data & Privacy

- Your ratings will be stored securely
- Data will be used only for this research study
- Your responses will be anonymized (no identifying info stored)
- You can withdraw at any time without penalty

---

## Thank You!

Your feedback is essential for improving AI explainability. Thank you for taking the time to help us understand how humans interact with AI explanations.

**Expected time**: 10-15 minutes for 10 explanations  
**Compensation**: [Insert amount/acknowledgment]

---

**Ready?** [Start → or Skip this guide and go to form]
