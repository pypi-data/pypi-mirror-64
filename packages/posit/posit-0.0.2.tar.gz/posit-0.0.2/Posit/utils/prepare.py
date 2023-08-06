import random
import os
from rdkit import Chem
from Posit.utils.RMSD import calcRMSD


def download_data(number):
    pass


def prepare_data(play_dir, pdb_dir):
    ligands = os.path.join(play_dir, pdb_dir, 'ligands.sdf')
    mols = [i for i in Chem.SDMolSupplier(ligands)]
    mols_h = [i for i in Chem.SDMolSupplier(ligands, removeHs=False)]
    ref = mols[:][0]
    atoms = [i for i in range(ref.GetNumAtoms())]
    random.shuffle(mols)

    # calc rmsd
    best_mol = None
    rmsd_value = {}
    w = Chem.SDWriter(ligands)
    for idx, mol in enumerate(mols):
        name = str(idx + 1)
        # rename mols
        mols_h[idx].SetProp('_Name', name)
        atomMaps = list(zip(atoms, atoms))
        rmsd = calcRMSD(mol, ref, atomMaps)
        rmsd_value[name] = rmsd
        # print(idx + 1, rmsd)
        if rmsd == 0:
            best_mol = name
        w.write(mols_h[idx])
    w.close()
    # rmsd_value - {"name": rmsd}
    return [rmsd_value, best_mol]