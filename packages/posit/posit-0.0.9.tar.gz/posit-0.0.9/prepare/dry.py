import os
import shutil


def dry(datapath, tmp_dir, savedpath):
    error = 0
    for i in os.listdir(datapath):
        pdb = os.path.join(datapath, i)
        tmp_pdb = os.path.join(tmp_dir, 'dry_' + i)
        try:
            os.system(f'pdb4amber -i {pdb} -o {tmp_pdb} -d')
            shutil.copy(tmp_pdb, savedpath)
        except Exception as e:
            print(i, repr(e))
            error += 1

    print(error)


if __name__ == '__main__':
    datapath = 'kinase_pdbs'
    savedpath = 'kinase_pdbs_dry'
    tmp_dir = 'tmp'

    dry(datapath, tmp_dir, savedpath)



