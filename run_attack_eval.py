import sys
from src.eval_safety import run

run(heldout="heldout" in sys.argv, use_ai="ai" in sys.argv)
