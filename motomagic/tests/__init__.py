# -*- coding: utf-8 -*-

import os

base_dir = os.path.dirname(__file__)

def run(coverage=False):
    import pytest
    argv = ['-x', base_dir, '-v', '-s']  #, "
    #if coverage:
    #    argv += ["--cov=freediscovery"]
    result = pytest.main(argv)
    status = int(result)
    return status
