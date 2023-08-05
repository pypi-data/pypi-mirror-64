from topoly import make_surface, lasso_type
from topoly.params import DensitySurface
import pytest

# importing the file 31.xyz. It is closed knot.
curve1 = 'data/lasso_01.xyz'
curve2 = '1 1.0 2.0 3.0\n2 2.0 2.0 5.0\n3 4.0 3. -1.\n4 -1 -1 2'
curve3 = 'data/2KUM_A.pdb'

def test_lassos():
    #S = make_surface(curve1, loop_indices=[1, 35], density=0)# =DensitySurface.LOW)
    #print("Surface,",S)
    #print(len(S),"\n",S[0])

    ot = 1
    #res = lasso_type(curve1,loop_indices=[[1, 35],[5,50]], smooth=10, output_type=ot)
    #print(res)
    #res = lasso_type(curve3,loop_indices=[[1, 35]], output_type=ot, pic_files=1011)
    #print(res)
    res = lasso_type(curve3, output_type=ot, pic_files=1011)
    print(res)


if __name__ == '__main__':
    test_lassos()


