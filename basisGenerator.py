def basis_generator(frag, path, level, ecp_species):

    # A simple function to write the fhiaims.basis files required for a QM/MM
    # calculation with Chemshell. Eventually to be incorporated into the
    # Chemshell codebase.
    
    # fragment:
    #    Chemshell Fragment object
    # level: str
    #    Basis set level to use. 'light', 'intermediate', ...
    # point_charge_species: str
    #    Species used by Chemshell to define the location of point charges
    
    print(frag.names)

    # Make a list of the species in the calculation    
    symbols = list(dict.fromkeys(frag.symbols)) 
    print(symbols)
    
    atomic_numbers = list(dict.fromkeys(frag.znums))
    print(atomic_numbers)
    
    # Format the list so it matches the path formatting     
    path_var = list([])
    for i in range(len(symbols)):
        #print(len(str(atomic_numbers[i])))
        if len(str(atomic_numbers[i])) < 2:
            atomic_numbers[i] = '0' + str(atomic_numbers[i])
    
        #print(str(symbols[i]))
        #print(str(atomic_numbers[i]))
        prefix = str(atomic_numbers[i]) + '_' + str(symbols[i])
        print(prefix)
        path_var.append(prefix)

    print(path_var)

    # Open a new file, overwriting the previous one    
    fhiaims_basis = open('fhiaims.basis', 'w')

    # Write the definition for emptium    
    print('Emptium')
    Ep_path = path + '/light/00_Emptium_default'
    basis_file = open(Ep_path)
    basis_set = basis_file.read()
    #print(basis_set)
    fhiaims_basis.write(basis_set)
    basis_file.close()
    fhiaims_basis.close()

    if bool(ecp_species) == True:
        print('ECP in use')
        ecp_path = path + '/' + level + '/' + ecp_species + '_default'
        basis_file = open(ecp_path)
        basis_set = basis_file.read()
        #print(basis_set)
        fhiaims_basis = open('fhiaims.basis', 'a')
        fhiaims_basis.write(basis_set)
        basis_file.close()
        fhiaims_basis.close()
                   
    # Write the other basis set definitions    
    for symbol in path_var:
        #print(symbol)
        sp_path = path + '/' + level + '/' + symbol + '_default'
        basis_file = open(sp_path)
        basis_set = basis_file.read()
        #print(basis_set)
        fhiaims_basis = open('fhiaims.basis', 'a')
        fhiaims_basis.write(basis_set)
        basis_file.close()
        fhiaims_basis.close()
        
