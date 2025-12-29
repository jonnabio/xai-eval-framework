
from lime.lime_tabular import LimeTabularExplainer
import inspect
import sys

print("Checking LimeTabularExplainer __init__ signature:")
sig = inspect.signature(LimeTabularExplainer.__init__)
print(sig)

if 'feature_selection' in sig.parameters:
    print("SUCCESS: feature_selection is in __init__")
else:
    print("FAILURE: feature_selection is NOT in __init__")

sys.path.append("/Users/cradmin/Documents/GitHub/xai-eval-framework/src")
from xai.lime_tabular import LIMETabularWrapper
print("\nChecking LIMETabularWrapper __init__ signature:")
sig_wrapper = inspect.signature(LIMETabularWrapper.__init__)
print(sig_wrapper)

if 'feature_selection' in sig_wrapper.parameters:
    print("SUCCESS: feature_selection is in wrapper __init__")
else:
    print("FAILURE: feature_selection is NOT in wrapper __init__")
