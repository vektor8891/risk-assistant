import os
import sys

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


# Simulate phishing risk
def phishing_risk():
    import src.phishing
    src.phishing.show_widgets()
