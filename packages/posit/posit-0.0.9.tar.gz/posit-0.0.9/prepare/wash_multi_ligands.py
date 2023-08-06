import os
from rdkit import Chem
import shutil


def not_ligand_chain():
    del_list = ['HOH', 'ZN', 'MN', ' MG', 'MG ', ' AL', 'AL ', 'FE ', ' FE', ' LI', 'LI ', ' NA',
                'NA ', '  K', 'K  ', ' CA', 'CA ', ' SN', 'SN ', 'SO4', 'NO3', 'PO4', ' CL', 'CL ', 'NH3', 'NAG',
                'NDG', 'Y01', 'GOL', 'EDO', 'CPS', 'CLR', 'PLP', 'HH', 'HH ', 'MAL', 'MPO', 'ADP', 'BOG', 'CAC', 'HH2',
                ' DG', 'DG ', 'HEM', 'T  ', '  T', 'G  ', '  G', 'A  ', '  A', 'U  ', '  U', 'C  ', '  C', 'ATP', 'AMP',
                'DNP', 'ANP']
    return del_list


def wash_pdb(in_dir):
    error = 0
    changed = 0
    h_error = 0
    no_ligand = 0
    for pdb in os.listdir(in_dir):
        pdb_path = os.path.join(in_dir, pdb)
        with open(pdb_path) as f:
            txt = f.readlines()

        num = [idx for idx, i in enumerate(txt) if i.startswith('HETATM')]
        if len(num) == 0:
            os.remove(pdb_path)
            error += 1
            continue
        lines = [i for idx, i in enumerate(txt) if i.startswith('HETATM')]
        atoms = []
        for i in lines:
            atoms.append(i.split()[3])
        chains = list(set(atoms))
        count_chains = [atoms.count(i) for i in chains]
        best_chain = chains[count_chains.index(max(count_chains))]
        
        # 对多个配体链进行清洗
        if len(chains) > 1:
            txt2 = []
            for i in txt:
                if i.startswith('HETATM'):
                    if i.split()[3] == best_chain:
                        txt2.append(i)
                else:
                    txt2.append(i)
            with open(pdb_path, 'w') as f:
                f.writelines(txt2)
            changed += 1

        with open('refer.pdb', 'w') as f:
            f.writelines(lines)

        # 删除读不出refer的
        mol = Chem.MolFromPDBFile('refer.pdb')
        if mol is None:
            error += 1
            os.remove(pdb_path)
            continue

        with open('refer.pdb') as f:
            lines = f.readlines()
        if lines[0].split()[3] in not_ligand_chain():
            # print('发现敌人！')
            no_ligand += 1
            os.remove(pdb_path)
            continue
        '''
        obabel_cmd = 'obabel -ipdb refer.pdb -opdb -O refer2.pdb -h'
        os.system(obabel_cmd)
        mol = Chem.MolFromPDBFile('refer2.pdb')
        if mol is None:
            h_error += 1
            os.remove(pdb_path)
            continue

        # 删除配体不连续的
        check_list = list(range(num[0], num[-1]+1))
        if num != check_list:
            os.remove(pdb_path)
            error += 1

        # 删除读不出盒子的
        os.system('./lepro_linux_x86 %s' % pdb_path)
        with open('dock.in') as f:
            txt = f.read()
        if 'xmin' in txt:
            print(pdb)
            os.remove(pdb_path)
        '''
    print(in_dir, 'removed:', error)
    print(in_dir, 'h_error', h_error)
    print(in_dir, 'changed:', changed)
    print(in_dir, 'no_ligand:', no_ligand)


def rename_pdb(in_dir):
    for pdb in os.listdir(in_dir):
        ori_name = os.path.join(in_dir, pdb)
        new_name = os.path.join(in_dir, pdb.split('.')[0] + '.pdb')
        os.rename(ori_name, new_name)


def split_dir(in_dir):
    num = 1
    for idx, pdb in enumerate(os.listdir(in_dir)):
        ori_name = os.path.join(in_dir, pdb)
        shutil.copy(ori_name, 'sc'+str(num))
        if (idx+1) % 500 == 0:
            num += 1


if __name__ == '__main__':
    '''
    for i in range(1, 7):
        in_dir = 'sc' + str(i)
        wash_pdb(in_dir)
    '''
    in_dir = 'wash_multi_ligand_2274'
    # wash_pdb(in_dir)
    split_dir(in_dir)
    # rename_pdb(in_dir)

