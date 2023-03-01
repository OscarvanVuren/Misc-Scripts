def basis_generator(frag, path, level, ecp_species, ecp_file):

    # A simple function to write the fhiaims.basis files required for a QM/MM
    # calculation with Chemshell. Eventually to be incorporated into the
    # Chemshell codebase.
    
    # fragment:
    #    Chemshell Fragment object
    # level: str
    #    Basis set level to use. 'light', 'intermediate', ...
    # ecp_species: str
    #    Species represented by pseudopotentials in the boundary region
    # ecp_file: str
    #    Name of the file containing pseudopotential information (.cpi)
    from os import listdir
    import re

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

    # Get and edit the default file for the species represented by pseudopotentials
    if bool(ecp_species) is True:
        print('ECPs in use')
        ecp_target = ecp_species + '_default'
        for speciesfilename in defaults:
            test = re.search(ecp_target, speciesfilename)
            if test is None:
                continue
            else:
                ecp_basis = test.string
        ecp_path = path + '/' + level + '/' + ecp_basis
        basis_file = open(ecp_path)
        basis_set_lines = basis_file.readlines()
        target_string = '  species        ' + ecp_species
        for i in range(len(basis_set_lines)):
            line_test = re.search(target_string, basis_set_lines[i])
            if line_test is None:
                continue
            else:
                basis_set_lines[i] = '  species        bq_' + ecp_species + '2_e\n'
                # Written backwards due to insert() adding before the given index
                basis_set_lines.insert(i+5, '    include_min_basis   .false.\n')
                basis_set_lines.insert(i+5, '    nonlinear_core	.false.\n')
                basis_set_lines.insert(i+5, '    pp_local_component  1\n')
                basis_set_lines.insert(i+5, '    pp_charge           2.0\n')
                basis_set_lines.insert(i+5, '    pseudo              ' + ecp_file + '\n')
                basis_set_lines.insert(i+5, '\n')
                basis_set_lines.insert(i+5, '# PSP\n')
                break
        basis_set = ''.join(basis_set_lines)
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
        
