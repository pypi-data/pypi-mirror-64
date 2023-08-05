from topoly import gln
from topoly.params import GlnMode, PlotFormat
import pytest
import time
import os

curve1 = 'data/lassos/lasso_01.xyz'
curve2 = '1 1.0 2.0 3.0\n2 2.0 2.0 5.0\n3 4.0 3. -1.\n4 -1 -1 2'
curve3 = 'data/2KUM_A.pdb'
curve4 = 'data/2kum.pdb'
curve5 = 'chain_6T1D_A.xyz'

class TestStructure:
    def __init__(self, chain1_data, chain2_data=None, comp1_boundary=(-1,-1), comp2_boundary=(-1,-1), basic_result=None, max_result_d15=None, max_result_dm1=None, max_result_d1=None, matrix_result=None, model=None, name='', error=False):

        self.chain1_data = chain1_data
        self.chain2_data = chain2_data
        self.comp1_boundary = comp1_boundary
        self.comp2_boundary = comp2_boundary
        self.basic_result = basic_result
        self.max_result_dm1 = max_result_dm1
        self.max_result_d15 = max_result_d15
        self.max_result_d1 = max_result_d1
        self.matrix_result = matrix_result
        self.model = model
        self.name = name
        self.error = error

    def test_me(self):
        print("\n*** Test named <"+self.name+"> ***\n")
        if self.error:
            try:
                res = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=comp1_boundary, chain2_boundary=comp2_boundary)
            except:
                print("OK - Caught wrong arguments")
                return 1
            print("[ERROR] (Wrong arguments not caught)")
            return 0
        try:
            resB = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary)
            if self.basic_result:
                if resB != self.basic_result:
                    print("[WRONG RESULT] mode BASIC, result",resB,", should be",self.basic_result)
                    return 0
                print("OK - mode BASIC")
                res = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary, precision_output=1)
                if res != round(self.basic_result,1):
                    print("[WRONG RESULT] wrong precision of output")
                    return 0
                print("OK - precision of output")
            if self.max_result_dm1:
                res = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary, mode=GlnMode.MAX)
                if res != self.max_result_dm1:
                      print("[WRONG RESULT] mode MAX, no local max, result",res,", should be",self.max_result_dm1)
                      return 0
                print("OK - mode MAX, no local max")
            if self.max_result_d15:
                t1 = time.time()
                res15 = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary, mode=GlnMode.MAX, max_density=15)
                t2 = time.time()
                if res15 != self.max_result_d15:
                      print("[WRONG RESULT] mode MAX, law density (15), result",res15,", should be",self.max_result_d15)
                      return 0
                print("OK - mode MAX, law density (15)")
            if self.max_result_d1:
                t3 = time.time()
                res1 = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary, mode=GlnMode.MAX, max_density=1)
                t4 = time.time()
                if res1 != self.max_result_d1:
                      print("[WRONG RESULT] mode MAX, the highest density (1), result",res1,", should be",self.max_result_d1)
                      return 0
                print("OK - mode MAX, the highest density (1)")
            if self.max_result_d15 and self.max_result_d1:
                tfast, tslow = t2-t1, t4-t3
                if tfast>tslow: print("[WARNING] lower density slower (",round(tfast,4),"s) than higher density (",round(tslow,4),"s)")
                else: print("OK - mode MAX, lower density faster (",round(tfast,4),"s) than higher density (",round(tslow,4),"s)")
                max15, max1 = res15['local maximum'][0], res1['local maximum'][0]
                if abs(max15)>abs(max1):
                    print("[WRONG RESULT] mode MAX, the highest density gives worse result (",max1,") than lower one (",max15,")")
                    return 0
                print("OK - mode MAX, the highest density gives better result (",max1,") than lower one (",max15,")")
            t1 = time.time()
            res10 = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary, mode=GlnMode.AVE, ave_tries=10)
            t2 = time.time()
            res400 = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary, mode=GlnMode.AVE, ave_tries=400)
            t3 = time.time()
            tfast, tslow = t2-t1, t3-t2
            if tfast>tslow: print("[WARNING] mode AVE, less tries slower (",round(tfast,4),"s) than more tries (",round(tslow,4),"s)")
            else: print("OK - mode AVE, less tries faster (",round(tfast,4),"s) than more tries (",round(tslow,4),"s)")
            if abs(res400-resB)>abs(res10-resB): print("[WARNING] less tries gives result (",res10,") closer to basic (",resB,") that more tries (",res400,")")
            else: print("OK - mode AVE, less tries gives result (",res10,") further to basic (",resB,") that more tries (",res400,")")

            if self.matrix_result:
                M = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary, mode=GlnMode.MATRIX)
                if M!=self.matrix_result:
                    print("[WRONG RESULT] mode MATRIX, result",M,", should be",self.matrix_result)
                    return 0
                print("OK - mode MATRIX, good result")

                def check_created_files(files_created, files_not_created):
                    for f in files_created:
                        try:
                            open(f,"r")
                        except:
                            print("[WRONG RESULT] mode MATRIX, file <"+f+"> not created, while it should be")
                            return 0
                    for f in files_not_created:
                        try:
                            open(f,"r")
                            print("[WRONG RESULT] mode MATRIX, file <"+f+"> created, while it shouldn't be")
                            return 0
                        except:
                            continue
                    return 1

                files_not_created, files_created = ["GLN_map.png","GLN_map.svg","GLN_map.pdf"], []
                if not check_created_files(files_created, files_not_created):
                    return 0
                M = gln(self.chain1_data, chain2_data = self.chain2_data, chain1_boundary=self.comp1_boundary, chain2_boundary=self.comp2_boundary, mode=GlnMode.MATRIX, matrix_plot_format=PlotFormat.PDF)
                files_not_created, files_created = ["GLN_map.png","GLN_map.svg"], ["GLN_map.pdf"]
                if not check_created_files(files_created, files_not_created):
                    return 0

                print("OK - mode MATRIX, files created / not created")

        except:
            print("[ERROR] not served - while working with this test")
            return 0
        return 1


def clean():
    files_to_remove = ["GLN_map.png","GLN_map.svg","GLN_map.pdf"]
    for f in files_to_remove:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass


# @pytest.mark.skip
def test_gln():
    
    #M = gln(curve5, chain1_boundary=(36,86), chain2_boundary=(87,300), mode=GlnMode.MATRIX, matrix_plot_format=PlotFormat.PDF, matrix_plot_fname="macierzGLN_test_6T1D_A", matrix_output_fname='macierzGLN_test_6T1D.txt')
    #clean()

    TestStr = []
    TestStr.append(TestStructure(curve1,comp1_boundary=(1,35), comp2_boundary=(36,60), basic_result=-0.187, max_result_d1={'whole chains': [-0.187], 'subchain of chain 2': [-0.225, '36-55'], 'subchain of chain 1': [-0.205, '7-35'], 'local maximum': [-0.249, '7-35', '36-55']}, max_result_d15={'whole chains': [-0.187], 'subchain of chain 2': [-0.225, '36-55'], 'subchain of chain 1': [-0.205, '7-35'], 'local maximum': [-0.187, '1-35', '36-60']}, max_result_dm1={'whole chains': [-0.187], 'subchain of chain 2': [-0.225, '36-55'], 'subchain of chain 1': [-0.205, '7-35'], 'local maximum': []}, name="lasso_01.xyz petla i ogon"))

    TestStr.append(TestStructure(curve1,comp2_boundary=(36,60),error=True,name="ERROR nachodza na siebie loop i tail"))

    TestStr.append(TestStructure(curve1, chain2_data=curve2, basic_result=-1.058, max_result_dm1={'whole chains': [-1.058], 'subchain of chain 2': [-1.058, '1-4'], 'subchain of chain 1': [-1.621, '4-33'], 'local maximum': []}, max_result_d1={'whole chains': [-1.058], 'subchain of chain 2': [-1.058, '1-4'], 'subchain of chain 1': [-1.621, '4-33'], 'local maximum': [-1.621, '4-33', '1-4']}, max_result_d15={'whole chains': [-1.058], 'subchain of chain 2': [-1.058, '1-4'], 'subchain of chain 1': [-1.621, '4-33'], 'local maximum': [-1.114, '1-46', '1-4']}, matrix_result=[[0.0, -0.02, -0.005, -1.058], [0.0, 0.0, 0.015, -1.038], [0.0, 0.0, 0.0, -1.053], [0.0, 0.0, 0.0, 0.0]], name="Z dwoch plikow i z macierza"))

    TestStr.append( TestStructure( curve3, comp1_boundary=(9,38), comp2_boundary=(39,88), basic_result=0.107, max_result_d1={'whole chains': [0.107], 'subchain of chain 2': [0.872, '48-77'], 'subchain of chain 1': [0.325, '11-34'], 'local maximum': [0.877, '9-34', '49-78']}, max_result_d15={'whole chains': [0.107], 'subchain of chain 2': [0.872, '48-77'], 'subchain of chain 1': [0.325, '11-34'], 'local maximum': [0.312, '9-38', '54-69']}, max_result_dm1={'whole chains': [0.107], 'subchain of chain 2': [0.872, '48-77'], 'subchain of chain 1': [0.325, '11-34'], 'local maximum': []}, name="2KUM_A, model domyslny" ))

    TestStr.append( TestStructure( curve4, comp1_boundary=(9,38), comp2_boundary=(39,88), name="pdb rozne modele", model=10 ))
    
    TestStr.append( TestStructure( curve5, comp1_boundary=(36,86), comp2_boundary=(87,300), max_result_d15={'whole chains': [-0.659], 'subchain of chain 2': [-1.207, '142-286'], 'subchain of chain 1': [-0.877, '42-74'], 'local maximum': [-1.101, '36-81', '117-252']}, max_result_d1={'whole chains': [-0.659], 'subchain of chain 2': [-1.207, '142-286'], 'subchain of chain 1': [-0.877, '42-74'], 'local maximum': [-1.433, '36-74', '142-286']}, name="pdb longer tail"))

    ok = 0
    clean()
    for T in TestStr: ok += T.test_me()
    print("\nSuccessfull tests: ",ok,"/",len(TestStr))
    clean()




if __name__ == '__main__':
    test_gln()

