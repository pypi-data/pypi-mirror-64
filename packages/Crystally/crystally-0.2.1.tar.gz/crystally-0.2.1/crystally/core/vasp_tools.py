from crystally.core.lattice import *


def interpolate_lattices(lattice1: Lattice, lattice2: Lattice, weighting=0.5):
    """ Linearly interpolate the atom list two lattices and return new lattice. Mind that the two lattices need to be
    sorted first!

    :param lattice1: first :class:`~crystally.core.lattice.Lattice`
    :param lattice2: second :class:`~crystally.core.lattice.Lattice`
    :param weighting: weighting between the two lattices. With weighting=0 the first, with weighting=1.0 the second
    lattice is returned. With weighting=0.5 (default value) every new atom position lies exactly between the ones of
    the provided lattices.
    :return: new interpolated :class:`~crystally.core.lattice.Lattice`
    """
    if len(lattice1.atoms) != len(lattice2.atoms):
        raise ValueError("lattices must have the same number of atoms!")

    new_lattice = Lattice(vectors=lattice1.vectors, atoms=[])
    for atom1, atom2 in zip(lattice1, lattice2):
        new_position = atom1.position + atom1.position.diff(atom2.position)*weighting
        new_atom = Atom(element=atom1.element, position=new_position, sublattice=atom1.sublattice)
        new_lattice.atoms.append(new_atom)
    return new_lattice


def get_element_number_list(lattice):
    """Get a two dimensional list with the sort order of the elements within the lattice.

    The first column specifies the element name and the second column the number of adjacent atoms with this
    element. This information can be used for VASP Input files.
    For instance if the sort order of the atoms is as follows:

    X, X, Y, Y, Y, X, X

    (where X and Y are the elements of the atoms)
    the function would return the following table:

    =============  =============================
    Element Name   Number of repeating elements
    =============  =============================
    X              2
    Y              4
    X              2
    =============  =============================

    :return: two dimensional list - the first column is an int, the second a string

    Examples
    --------
    >>> #lattice = generate_from_crystal(ceria(),2,2,2).sort("position")
    >>> #print(lattice.get_element_number_list())
    [['Ce', 1], ['O', 1], ['Ce', 3], ['O', 7]]
    """
    element_number_list = []
    for atom in lattice.atoms:
        if not element_number_list:
            element_number_list.append([atom.element, 1])
        elif element_number_list[-1][0] == atom.element:
            element_number_list[-1][1] += 1
        else:
            element_number_list.append([atom.element, 1])
    return element_number_list
