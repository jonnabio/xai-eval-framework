# Task Checklist: Phase H (Breadth Expansion)

**Objective**: Expand the framework to 4 Models x 4 XAI Methods (16+ combinations).

## Infrastructure (EXP1-56)
- [ ] **Dependencies**: Update `environment.yml`
    - [ ] Add `alibi`
    - [ ] Add `dice-ml`
    - [ ] Add `tensorflow` (CPU)
- [ ] **Architecture**: Refactor Trainers
    - [ ] Create `src/models/trainers.py`
    - [ ] Implement `BaseTrainer`
    - [ ] Implement `ModelTrainerFactory`
    - [ ] Migrate `RandomForestTrainer` and `XGBoostTrainer`

## New Models (EXP1-57)
- [ ] **SVM**: Implement `SVMTrainer` (RBF Kernel, Probability=True)
- [ ] **MLP**: Implement `MLPTrainer` (2 hidden layers default)
- [ ] **LogisticRegression**: Implement `LogisticRegressionTrainer` (Baseline)
- [ ] **Verification**: Smoke test all 3 new trainers

## New XAI Methods (EXP1-58/59)
- [ ] **Anchors**: Implement `AnchorsTabularWrapper`
- [ ] **DiCE**: Integrate `DiCETabularWrapper` with `BaseTrainer`
- [ ] **Integration**: Ensure `ExperimentRunner` can log metrics from these methods

## Execution (EXP1-60)
- [ ] **Experiment Matrix**: Generate 24 config files
- [ ] **Execution**: Run batch experiments
- [ ] **Results**: Verify `results.json` generation for all combinations
