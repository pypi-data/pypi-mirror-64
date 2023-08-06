import math


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
