import random
import os
from rdkit import Chem
from Posit.utils.RMSD import calcRMSD
import zipfile
import copy


def download_data(number):
    pass


def unzip(filename, output_path='./'):
    zFile = zipfile.ZipFile(filename, 'r')
    for fileM in zFile.namelist():
        zFile.extract(fileM, output_path)
    zFile.close()


def prepare_data(play_dir, pdb_dir):
    ligands = os.path.join(play_dir, pdb_dir, 'ligands.sdf')
    mols = [i for i in Chem.SDMolSupplier(ligands)]
    mols_h = [i for i in Chem.SDMolSupplier(ligands, removeHs=False)]
    ref = copy.deepcopy(mols[0])
    ref_core = ref.GetSubstructMatch(ref)
    mols_pair = list(zip(mols, mols_h))
    random.shuffle(mols_pair)

    # calc rmsd
    best_mol = None
    rmsd_value = {}
    w = Chem.SDWriter(ligands)
    for idx, mol_pair in enumerate(mols_pair):
        mol, mol_h = mol_pair
        name = str(idx + 1)
        mol_core = mol.GetSubstructMatch(ref)
        # rename mols
        mol_h.SetProp('_Name', name)
        atomMaps = list(zip(mol_core, ref_core))
        rmsd = calcRMSD(mol, ref, atomMaps)
        rmsd_value[name] = rmsd
        # print(idx + 1, rmsd)
        if rmsd == 0:
            best_mol = name
        w.write(mol_h)
    w.close()
    # rmsd_value - {"name": rmsd}
    return [rmsd_value, best_mol]
