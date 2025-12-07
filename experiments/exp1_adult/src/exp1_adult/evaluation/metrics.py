def compute_fidelity(explanation, model, X_local):
    """
    Compute fidelity of the explanation.
    TODO: implement fidelity metric (R2 or MSE).
    """
    raise NotImplementedError("compute_fidelity() not implemented yet")

def compute_stability(explanation, model, X, perturbation_func):
    """
    Compute stability of the explanation.
    TODO: implement stability metric.
    """
    raise NotImplementedError("compute_stability() not implemented yet")

def compute_sparsity(explanation):
    """
    Compute sparsity of the explanation.
    TODO: implement sparsity metric.
    """
    raise NotImplementedError("compute_sparsity() not implemented yet")

def compute_cost(explanation_func):
    """
    Compute cost (time/memory) of generating explanations.
    TODO: implement cost metric.
    """
    raise NotImplementedError("compute_cost() not implemented yet")
