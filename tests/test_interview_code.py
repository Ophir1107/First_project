import sys
import os

# # Make sure src folder is in path for terminal run
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.interview_code import tmp_try

def test_tmp_try():
    assert tmp_try() == 1