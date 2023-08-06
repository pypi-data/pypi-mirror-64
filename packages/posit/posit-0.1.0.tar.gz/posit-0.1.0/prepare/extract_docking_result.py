import os
import shutil
from rdkit import Chem
from rdkit.Chem import Descriptors
from multiprocessing import Pool
import math
import numpy as np
import copy


def dis_p2p(p1, p2):
    r = math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2) + math.pow((p1[2] - p2[2]), 2)
    return r


def calcRMSD(proMol, refMol, atomMaps):
    ref_conf = refMol.GetConformer()
    mol_conf = proMol.GetConformer()
    mse = 0
    for i, j in atomMaps:
        pos1 = mol_conf.GetAtomPosition(i)
        pos2 = ref_conf.GetAtomPosition(j)
        p1 = [pos1.x, pos1.y, pos1.z]
        p2 = [pos2.x, pos2.y, pos2.z]
        r = dis_p2p(p1, p2)
        mse += r
    mse /= len(atomMaps)
    RMSD = math.sqrt(mse)
    return round(RMSD, 3)


def wash_sdf(sdf, keep=None):
    if keep is None:
        keep = []
    has_prop = set()
    keep_prop = {}
    for i in keep:
        keep_prop[i] = []
    washed_sdf = sdf.replace('.sdf', '_washed.sdf')
    w = Chem.SDWriter(washed_sdf)
    suppl = Chem.SDMolSupplier(sdf, removeHs=None)
    for mol in suppl:
        for i in keep:
            try:
                keep_prop[i] += [mol.GetProp(i)]
                has_prop.add(i)
            except Exception:
                keep_prop[i] += ['']

        for i in [str(i) for i in mol.GetPropNames()]:
            mol.SetProp(i, 'need_remove')
        w.write(mol)
    w.close()

    with open(washed_sdf) as f:
        txt = f.readlines()
    txt = [i for i in txt if not i.startswith('>') and not i.startswith('need_remove')]
    with open(washed_sdf, 'w') as f:
        f.writelines(txt)

    finnal_sdf = sdf.replace('.sdf', '_XtalPi.sdf')
    w = Chem.SDWriter(finnal_sdf)
    suppl = Chem.SDMolSupplier(washed_sdf, removeHs=None)
    for idx, mol in enumerate(suppl):
        for i in keep:
            if i in has_prop:
                mol.SetProp(i, keep_prop[i][idx])
        w.write(mol)
    w.close()

    with open(finnal_sdf) as f:
        txt = f.read()
    txt = txt.replace('RDKit', 'XtalPi')
    with open(finnal_sdf, 'w') as f:
        f.write(txt)
    suppl = None
    os.remove(washed_sdf)


def RMSD_calc(sdf):
    mols_h = [i for i in Chem.SDMolSupplier(sdf, removeHs=False)]
    mols = [i for i in Chem.SDMolSupplier(sdf)]
    ref = mols[0]
    ref_core = ref.GetSubstructMatch(ref)
    decoys = mols[1:]
    rmsd_values = []
    for mol in decoys:
        mol_core = mol.GetSubstructMatch(ref)
        atomMaps = list(zip(mol_core, ref_core))
        rmsd = calcRMSD(mol, ref, atomMaps)
        rmsd_values.append(rmsd)

    keep_rmsd_list = []
    rmsd_index = np.argsort(rmsd_values)
    w = Chem.SDWriter(sdf)
    w.write(mols_h[0])
    for i in range(1, len(rmsd_values)-1, 2):
        w.write(mols_h[rmsd_index[i]])
        keep_rmsd_list.append(rmsd_values[rmsd_index[i]])
    if np.var(keep_rmsd_list) < 0.5 and sum(keep_rmsd_list[:3]) <= 3:
        print(sdf)
        print(keep_rmsd_list, 'var:', np.var(keep_rmsd_list))
        return False
    else:
        return True


def bad_filter(input_dir, pdb_dir):
    sdf = os.path.join(input_dir, pdb_dir, 'single_rdock.sd')
    mol = next(Chem.SDMolSupplier(sdf))
    if mol is None:
        print(mol)
        shutil.rmtree(os.path.join(input_dir, pdb_dir))


def copy_mp(input_dir, output_dir, pdb_dir):
    # file in answer
    in_pdb = os.path.join(input_dir, pdb_dir, 'pro.pdb')
    in_ref = os.path.join(input_dir, pdb_dir, 'refer.sd')
    in_ligands_tmp = os.path.join(input_dir, pdb_dir, 'single_rdock.sd')
    in_ligands = os.path.join(input_dir, pdb_dir, 'ligands.sdf')

    obabel_cmd = f'obabel {in_ligands_tmp} -O {in_ligands_tmp} -h'
    os.system(obabel_cmd)
    
    # combination and wash
    with open(in_ref) as f:
        txt1 = f.read()
    with open(in_ligands_tmp) as f:
        txt2 = f.read()
    with open(in_ligands, 'w') as f:
        f.write(txt1 + txt2)
        
    wash_sdf(in_ligands)
    in_ligands = os.path.join(input_dir, pdb_dir, 'ligands_XtalPi.sdf')

    # RMSD_filter
    if not RMSD_calc(in_ligands):
        return

    # create new dir
    os.mkdir(os.path.join(output_dir, pdb_dir))

    # file to extract
    out_pdb = os.path.join(output_dir, pdb_dir, 'receptor.pdb')
    out_ligands = os.path.join(output_dir, pdb_dir, 'ligands.sdf')
    
    # copy
    shutil.copy(in_pdb, out_pdb)
    shutil.copy(in_ligands, out_ligands)

        
def extract_result(input_dir, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    for pdb_dir in os.listdir(input_dir):
        bad_filter(input_dir, pdb_dir)
        
    cpu_num = os.cpu_count()
    p = Pool(cpu_num)
    for pdb_dir in os.listdir(input_dir):
        p.apply_async(copy_mp, args=(input_dir, output_dir, pdb_dir))
    p.close()
    p.join()
    
    rbond_3 = 0
    rings_35 = 0
    # remove empty output dir
    for pdb_dir in os.listdir(output_dir):
        out_ligands = os.path.join(output_dir, pdb_dir, 'ligands.sdf')
        if not os.path.exists(out_ligands):
            shutil.rmtree(os.path.join(output_dir, pdb_dir))
            continue
        suppl = Chem.SDMolSupplier(out_ligands)
        mol = next(suppl)
        if Descriptors.NumRotatableBonds(mol) < 3:
            rbond_3 += 1
            shutil.rmtree(os.path.join(output_dir, pdb_dir))
            continue
        if not (3 <= mol.GetRingInfo().NumRings() <= 5):
            rings_35 += 1
            shutil.rmtree(os.path.join(output_dir, pdb_dir))
            continue
    print(rbond_3)
    print(rings_35)


if __name__ == '__main__':
    input_dir = 'answer'
    output_dir = 'extract'
    extract_result(input_dir, output_dir)
    
    # out_ligands = os.path.join(output_dir, '5UKF', 'ligands.sdf')
    # RMSD_calc(out_ligands)
    

