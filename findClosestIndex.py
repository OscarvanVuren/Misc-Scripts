def find_closest_index(coeff,atoms,symbol):
    closest = list([])
    for n in [atom.index for atom in atoms if atom.symbol == symbol]:
        if np.allclose(atoms.positions[n],mid,atol=(lat*coeff)) == True:
            closest.append(n)
            
        else:
            continue
    
    return closest
