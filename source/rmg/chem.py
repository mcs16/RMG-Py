#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
#	RMG - Reaction Mechanism Generator
#
#	Copyright (c) 2002-2009 Prof. William H. Green (whgreen@mit.edu) and the
#	RMG Team (rmg_dev@mit.edu)
#
#	Permission is hereby granted, free of charge, to any person obtaining a
#	copy of this software and associated documentation files (the 'Software'),
#	to deal in the Software without restriction, including without limitation
#	the rights to use, copy, modify, merge, publish, distribute, sublicense,
#	and/or sell copies of the Software, and to permit persons to whom the
#	Software is furnished to do so, subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be included in
#	all copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#	DEALINGS IN THE SOFTWARE.
#
################################################################################

"""
Contains classes describing chemical entities: elements, atoms, bonds, species, etc.
"""

import quantities as pq
import pybel
import openbabel

################################################################################

class Element:
    """
	Represent a single chemical element. Each element has an atomic 
	`number`, a `name`, a `symbol`, an atomic `mass`, and a `valence`, a list 
	of the possible numbers of bonds allowed.
	
	This class is specifically for properties that all atoms of the same element
	share. Ideally there is only one instance of this class for each element. 
	"""

    def __init__(self, number, name, symbol, mass, valence):
        """Initialize a chemical element.

        Parameters:
        number -- The atomic number of the element
        name -- The name of the element
        symbol -- The symbol for the element
        mass -- The atomic mass of the element
        valence -- The valency of the element
        """
        self.number = number
        self.name = name
        self.symbol = symbol
        self.mass = mass
        self.valence = valence

################################################################################

def loadElements():
	"""
	Loads entries into a dictionary of elements. The dictionary created by
	this function is always available at :data:`rmg.chem.elements`.
	"""
	elements = {}
	elements[1] = elements['H'] = elements['hydrogen'] = Element(1, 'hydrogen', 'H', pq.Quantity(1.00794, 'g/mol'), 1)
	elements[2] = elements['He'] = elements['helium'] = Element(2, 'helium', 'He', pq.Quantity(4.002602, 'g/mol'), 0)
	elements[6] = elements['C'] = elements['carbon'] = Element(6, 'carbon', 'C', pq.Quantity(12.0107, 'g/mol'), 4)
	elements[7] = elements['N'] = elements['nitrogen'] = Element(7, 'nitrogen', 'N', pq.Quantity(14.00674, 'g/mol'), [3,5])
	elements[8] = elements['O'] = elements['oxygen'] = Element(8, 'oxygen', 'O', pq.Quantity(15.9994, 'g/mol'), 2)
	elements[9] = elements['F'] = elements['fluorine'] = Element(9, 'fluorine', 'F', pq.Quantity(18.998403, 'g/mol'), 1)
	elements[10] = elements['Ne'] = elements['neon'] = Element(10, 'neon', 'Ne', pq.Quantity(20.1797, 'g/mol'), 0)
	elements[14] = elements['Si'] = elements['silicon'] = Element(14, 'silicon', 'Si', pq.Quantity(28.0855, 'g/mol'), 4)
	elements[15] = elements['P'] = elements['phosphorus'] = Element(15, 'phosphorus', 'P', pq.Quantity(30.973761, 'g/mol'), [3,5])
	elements[16] = elements['S'] = elements['sulfur'] = Element(16, 'sulfur', 'S', pq.Quantity(32.065, 'g/mol'), [2,6])
	elements[17] = elements['Cl'] = elements['chlorine'] = Element(17, 'chlorine', 'Cl', pq.Quantity(35.453, 'g/mol'), 1)
	elements[18] = elements['Ar'] = elements['argon'] = Element(18, 'argon', 'Ar', pq.Quantity(39.348, 'g/mol'), 0)
	elements[35] = elements['Br'] = elements['bromine'] = Element(35, 'bromine', 'Br', pq.Quantity(79.904, 'g/mol'), 1)
	elements[53] = elements['I'] = elements['iodine'] = Element(53, 'iodine', 'I', pq.Quantity(126.90447, 'g/mol'), 1)
	return elements
	
# The dictionary of elements, accessible by atomic number, symbol, or name.
elements = loadElements()

################################################################################

class ElectronState:
    """
	Represent a single free electron state (none, radical, etc.) Each state is 
	defined by a unique string `label`; the `order`, or number of 
	free electrons; and a `spin` state ('' = none, 'S' = singlet, 'T' = 
	triplet).
	
	This class is specifically for properties that all free electron states 
	share. Ideally there is only one instance of this class for each free 
	electron state.
    """

    def __init__(self, label, order, spin=''):
        """
		Initialize a free electron state.

        Parameters:
        label -- A string unique to this free electron state
        order -- The number of free electrons
        spin -- The spin state for polyradicals (singlet = 'S', triplet = 'T')
        """
        self.label = label
        self.order = order
        self.spin = spin

################################################################################

def loadElectronStates():
	"""
	Loads entries into a dictionary of free electron states. The dictionary 
	created by this function is always available at 
	:data:`rmg.chem.electronStates`.
	"""
	electronStates = {}
	electronStates['0'] = ElectronState('0', 0, '')
	electronStates['1'] = ElectronState('1', 1, '')
	electronStates['2S'] = ElectronState('2S', 2, 'S')
	electronStates['2T'] = ElectronState('2T', 2, 'T')
	electronStates['3'] = ElectronState('3', 3, '')
	electronStates['4'] = ElectronState('4', 4, '')
	return electronStates

# The dictionary of electron states, accessible by label.
electronStates = loadElectronStates()

################################################################################
		
class Atom:
	"""
	Represent an atom in a chemical species. Each atom is defined by an 
	`element` (stored internally as an :class:`Element` object), a `electronState`
	(stored internally as an :class:`ElectronState` object), and a numeric `charge`.
	"""	

	def __init__(self, element=None, electronState=None, charge=0):
		"""
		Initialize an atom object.
		"""
		self.setElement(element)
		self.setElectronState(electronState)
		self.charge = charge

	def setElement(self, element):
		"""
		Set the element that this atom represents. The *element* parameter can
		be an :class:`Element` object, an integer representing the atomic 
		number, or a string containing the element symbol or name. In all 
		cases *element* will be converted to and stored as an :class:`Element` 
		object.
		"""
		if element.__class__ == str or element.__class__ == unicode:
			element = elements[element]
		if element.__class__ != Element:
			raise Exception('Invalid parameter "element".')
		self.element = element

	def setElectronState(self, electronState):
		"""
		Set the electron state that this atom represents. The *electronState* 
		parameter can be an :class:`ElectronState` object or a string 
		representing the label of the desired electron state. In all cases 
		*electronState*	will be converted to and stored as an 
		:class:`ElectronState` object.
		"""
		if electronState.__class__ == str or electronState.__class__ == unicode:
			electronState = electronStates[electronState]
		if electronState.__class__ != ElectronState:
			raise Exception('Invalid parameter "electronState".')
		self.electronState = electronState

################################################################################

class BondType:
    """
	Represent a type of chemical bond. Each bond type has a unique string 
	`label`; a unique string `name`; a numeric bond `order`; an integral 
	`piElectrons`, the number of pi electrons; and a string `location` with
	bond geometry information (i.e. 'cis' or 'trans').
	
	This class is specifically for properties that all bonds of the same type 
	share. Ideally there is only one instance of this class for each bond type.
    """

    def __init__(self, label, name, order, piElectrons, location=''):
        """Initialize a chemical bond.

        Parameters:
        label -- A short string unique to this bond type
        name -- A longer string unique to this bond type
        order -- The bond order (1 = single, 2 = double, 3 = triple, etc.)
        piElectrons -- The number of pi electrons in the bond
        location -- Bond location information ('cis' or 'trans')
        """
        self.label = label
        self.name = name
        self.order = order
        self.piElectrons = piElectrons
        self.location = location

################################################################################

def loadBondTypes():
	"""
	Loads entries into a dictionary of bond types. The dictionary created by
	this function is always available at :data:`rmg.chem.bondTypes`.
	"""
	
	bondTypes = {}
	bondTypes[1] = bondTypes['S'] = bondTypes['single'] = BondType('S', 'single', 1, 0, '')
	bondTypes[2] = bondTypes['D'] = bondTypes['double'] = BondType('D', 'double', 2, 2, '')
	bondTypes['Dcis'] = BondType('Dcis', 'double_cis', 2, 2, 'cis')
	bondTypes['Dtrans'] = BondType('Dtrans', 'double_trans', 2, 2, 'trans')
	bondTypes[3] = bondTypes['T'] = bondTypes['triple'] = BondType('T', 'triple', 3, 4, '')
	bondTypes[1.5] = bondTypes['B'] = bondTypes['benzene'] = BondType('B', 'benzene', 1.5, 1, '')
	return bondTypes
	
# The dictionary of bond types, accessible by label, order, or name.
bondTypes = loadBondTypes()

################################################################################

class Bond:
	"""
	Represent a bond in a chemical species. Each bond has a list `atoms` of 
	length two containing the two atoms in the bond and a `bondType` object,
	stored internally as a :class:`BondType` object.
	"""	

	def __init__(self, atoms, bondType=''):
		self.setBondType(bondType)
		self.atoms = atoms

	def setBondType(self, bondType):
		"""
		Set the bond type that this bond represents. The *bondType* 
		parameter can be a :class:`BondType` object, a number representing
		the bond order, or a string representing the label of the desired bond 
		type. In all cases *bondType* will be converted to and stored as a
		:class:`BondType` object.
		"""
		if bondType.__class__ == str or bondType.__class__ == unicode:
			bondType = bondTypes[bondType]
		if bondType.__class__ != BondType:
			raise Exception('Invalid parameter "bondType".')
		self.bondType = bondType

################################################################################

class Structure:
	"""
	Represent the chemical structure of a single resonance form of a chemical
	species as a graph. Atom iteration is possible via the `atoms` list,
	while bond iteration is possible via the `bonds` list. The graph is stored
	as a dictionary in the `graph` data member, where the keys are atoms and
	the values are lists of bonds.
	"""	

	def __init__(self, atoms=[], bonds=[]):
		"""
		Initialize a Structure object.
		"""
		self.atoms = atoms
		self.bonds = bonds
		self.updateGraph()
	
	def updateGraph(self):
		"""
		Rebuild the `graph` data member based on the current state of the
		`atoms` and `bonds` data members.
		"""
		self.graph = {}
		for atom in self.atoms:
			self.graph[atom] = []
		for bond in self.bonds:
			for atom in bond.atoms:
				self.graph[atom].append(bond)
	
	def fromOBMol(self, obmol):
		"""
		Convert an OpenBabel OBMol object `obmol` to a Structure object.
		"""
		
		self.atoms = []; self.bonds = []; self.graph = {}
		
		# Add hydrogen atoms to complete molecule if needed
		obmol.AddHydrogens()
		
		# Iterate through atoms in obmol
		for i in range(0, obmol.NumAtoms()):
			obatom = obmol.GetAtom(i + 1)
			
			# Use atomic number as key for element
			number = obatom.GetAtomicNum()
			
			# Process spin multiplicity
			electron = obatom.GetSpinMultiplicity()
			if electron == 0: electron = '0'
			elif electron == 1:	electron = '2S'
			elif electron == 2:	electron = '1'
			elif electron == 3:	electron = '2T'
			
			atom = Atom(elements[number], electronStates[electron])
			self.atoms.append(atom)
			
			# Add bonds by iterating again through atoms
			for j in range(0, i):
				obatom2 = obmol.GetAtom(j + 1)
				obbond = obatom.GetBond(obatom2)
				if obbond is not None:
					order = ''
					
					# Process bond type
					if obbond.IsSingle(): order = 'S'
					elif obbond.IsDouble(): order = 'D'
					elif obbond.IsTriple(): order = 'T'
					elif obbond.IsAromatic(): order = 'B'
					
					bond = Bond([self.atoms[i], self.atoms[j]], bondTypes[order])
					self.bonds.append(bond)
		
		# Create the graph from the atom and bond lists
		self.updateGraph()
		
	def toOBMol(self):
		"""
		Convert a Structure object to an OpenBabel OBMol object.
		"""
		obmol = openbabel.OBMol()
		for atom in self.atoms:
			a = obmol.NewAtom()
			a.SetAtomicNum(atom.element.number)
		for bond in self.bonds:
			index1 = self.atoms.index(bond.atoms[0])
			index2 = self.atoms.index(bond.atoms[1])
			order = bond.bondType.order
			if order == 1.5: order = 5
			obmol.AddBond(index1+1, index2+1, order)
		
		return obmol
	
	def toInChI(self):
		mol = pybel.Molecule(self.toOBMol())
		return mol.write('inchi').strip()
		
################################################################################

class Species:
	"""
	Represent a chemical species (including all of its resonance forms). Each
	species has a unique integer `id` assigned automatically by RMG and a 
	not-necessarily unique string `label`. The *structure* variable contains a 
	list of :class:`Structure` objects representing each resonance form. The 
	`reactive` flag is :data:`True` if the species can react and :data:`False` 
	if it is inert.
	"""	

	# A static counter for the number of species created since the RMG job began.
	numSpecies = 0

	def __init__(self, label='', structure=None, reactive=True):
		"""
		Initialize a Species object.
		"""
		Species.numSpecies += 1
		self.id = Species.numSpecies
		self.label = label
		if structure is None:
			self.structure = Structure()
		else:
			self.structure = structure
		self.reactive = reactive
		
	def toInChI(self):
		"""
		Return the InChI string corresponding to the current species.
		"""
		return self.structure.toInChI()
	
	def __str__(self):
		"""
		Return a string representation of the species, in the form 'id(label)'.
		"""
		return self.label + '(' + str(self.id) + ')'
		
################################################################################

if __name__ == '__main__':
	
	print ''
	
	print 'Elements available:'
	for key, element in elements.iteritems():
		print '\t' + str(key) + ' ' + element.symbol
	print ''
	
	print 'Free electron states available:'
	for key, electronState in electronStates.iteritems():
		print '\t' + electronState.label
	print ''
	
	print 'Bond types available:'
	for key, bondType in bondTypes.iteritems():
		print '\t' + str(key) + ' ' + bondType.label
	print ''
	