import random
import operator
import sys
import unittest
from MatrixAlgebra import MatrixAlgebra

class MatrixTest(unittest.TestCase):

    def testAdd(self):
        m1 = MatrixAlgebra.fromList([[1, 2, 3], [4, 5, 6]])
        m2 = MatrixAlgebra.fromList([[7,8,9],[10,11,12]])
        m3 = m1 + m2
        self.assertTrue(m3 == MatrixAlgebra.fromList([[8,10,12],[14,16,18]]))
    
    def testSub(self):
        m1 = MatrixAlgebra.fromList([[1,2,3],[4,5,6]])
        m2 = MatrixAlgebra.fromList([[7,8,9],[10,11,12]])
        m3 = m2 - m1
        self.assertTrue(m3 == MatrixAlgebra.fromList([[6,6,6],[6,6,6]]))

    def testMul(self):
        m1 = MatrixAlgebra.fromList([[1,2,3],[4,5,6]])
        m2 = MatrixAlgebra.fromList([[7, 8], [10, 11], [12, 13]])
        self.assertTrue(m1 * m2 == MatrixAlgebra.fromList([[63,69],[150,165]]))
        self.assertTrue(m2 * m1 == MatrixAlgebra.fromList([[39, 54, 69], [54, 75, 96], [64, 89, 114]]))

    def testTranspose(self):
        m1 = MatrixAlgebra.makeRandom(25,30)
        zerom = MatrixAlgebra.makeZero(25,30)
        m2 = m1 + zerom

        m1.transpose()
        m2.transpose()
        self.assertTrue(m2 == m1)

        # Also test getTranspose
        m2 = m1.getTranspose()
        r2 = m2.getRank()

        self.assertTrue(r2 == (25,30))
        m2.transpose()

        self.assertTrue(m2 == m1)

    def testId(self):
        
        m1 = MatrixAlgebra.makeId(10)
        m2 = MatrixAlgebra.makeRandom(4,10)
        m3 = m2 * m1
        self.assertTrue(m3 == m2)

if __name__ == "__main__":
    unittest.main()