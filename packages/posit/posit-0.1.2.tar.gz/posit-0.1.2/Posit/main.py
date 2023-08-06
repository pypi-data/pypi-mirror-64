import click
import os
import datetime
from Posit.utils.prepare import prepare_data, download_data


def print_answer(user_input, best_mol, rmsd, score, pdb_id, idx):
    print_list = ['Your score of Exercise %s : %s/10' % ((idx + 1), score)]
    if user_input != best_mol:
        print_list.append('\nMol %s RMSD: %s' % (user_input, rmsd[user_input]))
        print_list.append('Best Mol: %s' % best_mol)
    else:
        print_list.append('\nCorrect answer, Prefect!')

    print_list.append('\nPDB_ID: %s' % pdb_id)
    print_list.append('\nExercise_%s Answer List:' % (idx + 1))
    for i in rmsd.keys():
        print_list.append(i + ':' + str(rmsd[i]))

    for i in print_list:
        print(i)
    return print_list


def calc_score(rmsd):
    rmsd = float(rmsd)
    if rmsd >= 5:
        score = 0
    else:
        score = -2 * rmsd + 10

    score = int((score - int(score)) * 10)/10 + int(score)
    return score


@click.command()
@click.option('-n', '--number', type=int, help='Number of Exercise', default=5)
def run(number):
    # download data from CosMos
    play_dir = download_data(number)

    answer = []
    pdb_dir_list = [i for i in os.listdir(play_dir) if os.path.isdir(os.path.join(play_dir, i))]

    pdb_id_list = []
    for idx, pdb_dir in enumerate(pdb_dir_list):
        old_dir_name = os.path.join(play_dir, pdb_dir)
        new_dir_name = os.path.join(play_dir, 'Exercise_'+str(idx+1))
        answer.append(prepare_data(play_dir, pdb_dir))
        os.rename(old_dir_name, new_dir_name)
        # record PDB_ID
        pdb_id_list.append(pdb_dir)

    txt_list = []
    print(f'\nReady, please switch to the "{play_dir}" directory')

    # get start time
    start = datetime.datetime.now()

    total_score = []
    answer_area = [str(i) for i in range(1, 11)]
    for idx, ans in enumerate(answer):
        rmsd = ans[0]
        best_mol = ans[1]
        pdb_id = pdb_id_list[idx]
        while True:
            user_input = input('\nInput the mol number of Exercise %s :' % (idx+1))
            if user_input in answer_area:
                break
            else:
                print('Input error!Please input the number!')

        # record
        txt_list.append('Exercise %s ' % (idx + 1))
        txt_list.append("User's choice: %s" % user_input)

        # calc score
        score = calc_score(rmsd[user_input])
        total_score.append(score)

        # print_answer
        print_list = print_answer(user_input, best_mol, rmsd, score, pdb_id, idx)
        txt_list.extend(print_list)
        txt_list.append('-------------')

    average_score_txt = '\n\nYour average score of %s exercises: %s' % (number, sum(total_score)/number)
    print(average_score_txt)
    txt_list.append(average_score_txt)

    # get end time and time cost
    end = datetime.datetime.now()
    txt_list.append('start time:' + start.strftime('%Y.%m.%d-%H:%M:%S'))
    txt_list.append('end time:' + end.strftime('%Y.%m.%d-%H:%M:%S'))
    time_cost = 'time cost: ' + str(end - start)
    txt_list.append(time_cost)
    print(time_cost)

    # save to a txt file
    txt_list = [i+'\n' for i in txt_list]
    with open(os.path.join(play_dir, 'Posit_record.txt'), 'w') as f:
        f.writelines(txt_list)


if __name__ == '__main__':
    run()
