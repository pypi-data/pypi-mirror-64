import random
import os
from rdkit import Chem
from Posit.utils.RMSD import calcRMSD
import zipfile
import copy
from boto3.session import Session


def get_s3_access():
    aws_key = 'AKIA5YRY5HWNKMYTPZYX'
    aws_secret_key = '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'
    session = Session(aws_access_key_id=aws_key,
                      aws_secret_access_key=aws_secret_key,
                      region_name='cn-northwest-1')
    s3 = session.client("s3")
    return s3


def create_playdir():
    playdir = 'Posit'
    if not os.path.exists(playdir):
        os.mkdir(playdir)
        return playdir

    num = 1
    while True:
        playdir = 'Posit' + str(num)
        if not os.path.exists(playdir):
            os.mkdir(playdir)
            break
        else:
            num += 1
    return playdir


def get_random_key(key_list, num):
    dir_names = set()
    for key in key_list:
        dir_names.add(key['Key'].split('/')[2])

    return random.sample(list(dir_names), num)


def download_data(number=5):
    # create Posit directory
    playdir = create_playdir()

    s3 = get_s3_access()
    bucket = 'posit'

    # key: Posit/PKIs/XXXX/ligands.sdf
    key_list = s3.list_objects(Bucket=bucket)['Contents']

    # get random N dir names
    random_key = get_random_key(key_list, number)

    for pdb_id in random_key:
        target_dir = os.path.join(playdir, pdb_id)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        upload_key1 = f'Posit/PKIs/{pdb_id}/ligands.sdf'
        upload_key2 = f'Posit/PKIs/{pdb_id}/receptor.pdb'
        file_name1 = upload_key1.replace('Posit/PKIs', playdir)
        file_name2 = upload_key2.replace('Posit/PKIs', playdir)
        s3.download_file(Filename=file_name1, Key=upload_key1, Bucket=bucket)
        s3.download_file(Filename=file_name2, Key=upload_key2, Bucket=bucket)

    return playdir


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


if __name__ == '__main__':
    download_data(number=5)
