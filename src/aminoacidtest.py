#!/usr/bin/env python

"""Unit test for aminoacid.py"""

import aminoacid
import unittest
import itertools

aminoacids = {
    'cut': 's', 'dlt': 's', 'swi': 'r', 'mvr': 's',
    'mvl': 's', 'cop': 'r', 'off': 'l',
    'ina': 's', 'inc': 'r', 'ing': 'r', 'itt': 'l',
    'rpy': 'r', 'rpu': 'l', 'lpy': 'l', 'lpu': 'l',
}


class AminoAcidsCheck(unittest.TestCase):
    def testAminoAcidsDict(self):
        """Aminoacids is dictionary of commands mapped onto directions
        for tertiary enzyme structure"""
        self.assertEquals(aminoacid.aminoacids, aminoacids)

    def testAminoAcidCorrectCreation(self):
        """Aminoacid is successfully created from a duplet of units"""
        a = aminoacid.Aminoacid('TC')
        self.assertEquals(a.name, 'rpu')

    def testAminoAcidCorrectCreationByName(self):
        """Aminoacid is successfully created by name"""
        a = aminoacid.Aminoacid('rpu')
        self.assertEquals(a.name, 'rpu')
        self.assertIs(a.method, aminoacid.rpu)

    def testAminoAcidSaneCreation(self):
        """Aminoacid is created from any correct duplet"""
        for tup in itertools.product('ACGT', repeat=2):
            string = ''.join(tup)
            a = aminoacid.Aminoacid(string)
            self.assertEquals(a.name, aminoacid.names[string])

    def testAminoAcidSaneCreationByName(self):
        """Aminoacid is created by any correct name"""
        for name in aminoacids.keys():
            a = aminoacid.Aminoacid(name)
            self.assertEquals(a.name, name)

    def testAminoAcidIncorrectCreationNotInSet(self):
        """Exception is raised when incorrect string is supplied"""
        self.assertRaises(aminoacid.NotInSet, aminoacid.Aminoacid, 'AB')
        self.assertRaises(aminoacid.NotInSet, aminoacid.Aminoacid, 'A')
        self.assertRaises(aminoacid.NotInSet, aminoacid.Aminoacid, 'A ')
        self.assertRaises(aminoacid.NotInSet, aminoacid.Aminoacid, 'aaa')
        self.assertRaises(aminoacid.NotInSet, aminoacid.Aminoacid, 'cat')

    def testAminoAcidIncorrectCreationNotAString(self):
        """Exception is raised when not a string is supplied"""
        self.assertRaises(aminoacid.NotAString, aminoacid.Aminoacid, 42)


class AminoAcidsRunCheck(unittest.TestCase):
    def testMvrNoCopy(self):
        strands = [list('ACGT')]
        self.assertEquals(aminoacid.mvr(strands, 1, False, 0), 2)

    def testMvrCopy(self):
        strands = [list('ACGTAC')]
        self.assertEquals(aminoacid.mvr(strands, 0, True, 0), 1)
        self.assertEquals(strands, [list('ACGTAC'), list('TG    ')])
        strands = [list('ACGTAC')]
        self.assertEquals(aminoacid.mvr(strands, 1, True, 0), 2)
        self.assertEquals(strands, [list('ACGTAC'), list(' GC   ')])
        strands = [list('ACGTAC')]
        self.assertEquals(aminoacid.mvr(strands, 2, True, 0), 3)
        self.assertEquals(strands, [list('ACGTAC'), list('  CA  ')])

    def testMvlNoCopy(self):
        strands = [list('ACGT')]
        self.assertEquals(aminoacid.mvl(strands, 1, False, 0), 0)

    def testMvlCopy(self):
        strands = [list('ACGTAC')]
        self.assertEquals(aminoacid.mvl(strands, 1, True, 0), 0)
        self.assertEquals(strands, [list('ACGTAC'), list('TG    ')])
        strands = [list('ACGTAC')]
        self.assertEquals(aminoacid.mvl(strands, 2, True, 0), 1)
        self.assertEquals(strands, [list('ACGTAC'), list(' GC   ')])
        strands = [list('ACGTAC')]
        self.assertEquals(aminoacid.mvl(strands, 3, True, 0), 2)
        self.assertEquals(strands, [list('ACGTAC'), list('  CA  ')])

    def testRpyNoCopy(self):
        self.assertEquals(aminoacid.rpy([list('ACGTAGTC')], 2, False, 0), 3)

    def testRpyCopy(self):
        strands = [list('ACGT')]
        self.assertEquals(aminoacid.rpy(strands, 0, True, 0), 1)
        self.assertEquals(strands, [list('ACGT'), list('TG  ')])
        strands = [list('ACGT'), list('T')]
        self.assertEquals(aminoacid.rpy(strands, 0, True, 0), 1)
        self.assertEquals(strands, [list('ACGT'), list('TG  ')])

    def testASimpleCopyingTranslationByStage(self):
        strands = [list('ACGT')]
        self.assertEquals(aminoacid.cop(False), True)

        self.assertEquals(aminoacid.rpy(strands, 0, True, 0), 1)
        self.assertEquals(strands, [list('ACGT'), list('TG  ')])

        self.assertEquals(aminoacid.rpy(strands, 1, True, 0), 3)
        self.assertEquals(strands, [list('ACGT'), list('TGCA')])

        self.assertEquals(aminoacid.mvl(strands, 3, True, 0), 2)
        self.assertEquals(strands, [list('ACGT'), list('TGCA')])

        self.assertEquals(aminoacid.mvl(strands, 2, True, 0), 1)
        self.assertEquals(strands, [list('ACGT'), list('TGCA')])

        self.assertEquals(aminoacid.mvl(strands, 1, True, 0), 0)
        self.assertEquals(strands, [list('ACGT'), list('TGCA')])

        self.assertEquals(aminoacid.off(True), False)

        self.assertEquals(aminoacid.ina(strands, 0, False, 0),
                          ([list('AACGT'), list('T GCA')], 1))
        self.assertEquals(strands, [list('AACGT'), list('T GCA')])

    def testACopyingTranslationByStage(self):
        strands = [list('TAGATCCAGTCCATCGA')]
        copy = False
        locus = 8  # Position of second 'G'
        active_strand = 0

        locus = aminoacid.rpu(strands, locus, copy, active_strand)
        self.assertEquals(locus, 12)
        self.assertEquals(strands, [list('TAGATCCAGTCCATCGA')])

        strands, locus = aminoacid.inc(strands, locus, copy,
                                       active_strand)
        self.assertEquals(locus, 13)
        self.assertEquals(strands, [list('TAGATCCAGTCCACTCGA')])

        copy = aminoacid.cop(copy)
        strands.append(aminoacid.complement(strands[active_strand],
                                            locus, locus + 1))
        self.assertEquals(locus, 13)
        self.assertEquals(strands, [list('TAGATCCAGTCCACTCGA'),
                                    list('             G    ')])

        locus = aminoacid.mvr(strands, locus, copy, active_strand)
        self.assertEquals(locus, 14)
        self.assertEquals(strands, [list('TAGATCCAGTCCACTCGA'),
                                    list('             GA   ')])

        locus = aminoacid.mvl(strands, locus, copy, active_strand)
        self.assertEquals(locus, 13)
        self.assertEquals(strands, [list('TAGATCCAGTCCACTCGA'),
                                    list('             GA   ')])

        active_strand = aminoacid.swi(active_strand)
        strands[0] = strands[0][::-1]
        strands[1] = strands[1][::-1]
        locus = len(strands[active_strand]) - locus - 1
        self.assertEquals(active_strand, 1)
        self.assertEquals(strands, [list('AGCTCACCTGACCTAGAT'),
                                    list('   AG             ')])

        locus = aminoacid.lpu(strands, locus, copy, active_strand)
        self.assertEquals(locus, 3)
        self.assertEquals(strands, [list('AGCTCACCTGACCTAGAT'),
                                    list('   AG             ')])

        strands, locus = aminoacid.itt(strands, locus, copy, active_strand)
        self.assertEquals(locus, 4)
        self.assertEquals(strands, [list('AGCTACACCTGACCTAGAT'),
                                    list('   ATG             ')])
    
    def testInsertionAfterCopy(self):
        strands = [list('ACGTTGCA')]
        locus = 0
        active_strand = 0
        copy = False
        strands.append(aminoacid.complement(strands[active_strand],
                                            locus, locus + 1))
        strands, locus = aminoacid.ina(strands, locus, copy, active_strand)
        self.assertEquals(locus, 1)
        self.assertEquals(strands, [list('AACGTTGCA'), list('T        ')])


if __name__ == "__main__":
    unittest.main()
