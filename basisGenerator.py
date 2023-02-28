def basis_generator(frag, path, level, ecp_species):

    # A simple function to write the fhiaims.basis files required for a QM/MM
    # calculation with Chemshell. Eventually to be incorporated into the
    # Chemshell codebase.
    
    # fragment:
    #    Chemshell Fragment object
    # level: str
    #    Basis set level to use. 'light', 'intermediate', ...
    # ecp_species: str
    #    Species represented by pseudopotentials in the boundary region

    from os import listdir
    import re

    print(frag.names)

    # Make a list of the species in the calculation    
    symbols = list(dict.fromkeys(frag.symbols)) 
    print(symbols)
    
    # Create a list of the needed filenames for the elements contained in the fragment
    path_var = list([])
    defaults = listdir(path + '/' + level)
    for chem_symbol in symbols:
        target = chem_symbol + '_default$'
        for speciesfilename in defaults:
            test = re.search(target, speciesfilename)
            if test is None:
                continue
            if test.string == '09_F_default':
                continue
                # Removing the fluorine representing point charges
            else:
                print(test.string)
                path_var.append(test.string)

    print(path_var)

    # Open a new file, overwriting the previous one    
    fhiaims_basis = open('fhiaims.basis', 'w')

    # Write in the definition for Emptium
    print('Emptium')
    ep_path = path + '/light/00_Emptium_default'
    basis_file = open(ep_path)
    basis_set = basis_file.read()
    fhiaims_basis.write(basis_set)
    basis_file.close()
    fhiaims_basis.close()

    # Add in the basis set for any pseudopotentials
    if ecp_species is True:
        print('ECP in use')
        ecp_target = ecp_species + '_default'
        for speciesfilename in defaults:
            test = re.search(ecp_target, speciesfilename)
            if test is None:
                continue
            else:
                ecp_basis = test.string
        ecp_path = path + '/' + level + '/' + ecp_basis
        basis_file = open(ecp_path)
        basis_set = basis_file.read()
        fhiaims_basis = open('fhiaims.basis', 'a')
        fhiaims_basis.write(basis_set)
        basis_file.close()
        fhiaims_basis.close()
                   
    # Write the other basis set definitions    
    for symbol in path_var:
        sp_path = path + '/' + level + '/' + symbol + '_default'
        basis_file = open(sp_path)
        basis_set = basis_file.read()
        fhiaims_basis = open('fhiaims.basis', 'a')
        fhiaims_basis.write(basis_set)
        basis_file.close()
        fhiaims_basis.close()
        
