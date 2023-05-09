import sys, os


# appends the system path to the graph files
sys.path.append(os.path.abspath('main'))
sys.path.append(os.path.abspath('test'))

from color_ref_fast import GraphFastRef
from test_utils import test


def fast_ref(graph):
    GraphFastRef([graph]).reset().refine()


if __name__ == '__main__':
    test('test/color-ref-fast/samples/', [([
        'threepaths5.gr',
        'threepaths10.gr',
        'threepaths20.gr',
        'threepaths40.gr',
        'threepaths80.gr',
        'threepaths160.gr',
        'threepaths320.gr',
        'threepaths640.gr',
        'threepaths1280.gr',
        'threepaths2560.gr',
        'threepaths5120.gr',
        'threepaths10240.gr',
    ],
        fast_ref,
        None
    )])
