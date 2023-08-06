import click
import os
import datetime
from Posit.utils.prepare import unzip, prepare_data, download_data


def print_answer(user_input, best_mol, rmsd, score, pdb_id, idx):
    print_list = []
    if user_input != best_mol:
        print_list.append('\nMol %s RMSD: %s' % (user_input, rmsd[user_input]))
        print_list.append('Best Mol: %s' % best_mol)
        print_list.append('Your score of Exercise_%s: %s' % ((idx + 1), '待开发'))
    else:
        print_list.append('\nCorrect answer, Prefect!')

    print_list.append('PDB_ID: %s' % pdb_id)
    print_list.append('\nExercise_%s Answer List:' % (idx + 1))
    for i in rmsd.keys():
        print_list.append(i + ':' + str(rmsd[i]))

    for i in print_list:
        print(i)
    return print_list


@click.command()
@click.option('-n', '--number', type=int, help='Number of Exercise', default=5)
def run(number):
    # download data from CosMos
    download_data(number)

    # unzip dir
    zip_file = 'Posit.zip'
    unzip(zip_file, output_path='./')
    # os.remove(zip_file)

    answer = []
    play_dir = 'Posit'
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

    # get start time
    start = datetime.datetime.now()

    answer_area = [str(i) for i in range(1, 11)]
    for idx, ans in enumerate(answer):
        rmsd = ans[0]
        best_mol = ans[1]
        pdb_id = pdb_id_list[idx]
        while True:
            user_input = input('\nInput the mol number of Exercise_%s:' % (idx+1))
            if user_input in answer_area:
                break
            else:
                print('Input error!Please input the number!')

        # record
        txt_list.append('Exercise_%s' % (idx + 1))
        txt_list.append("User's choice: %s" % user_input)

        # calc score
        score = None

        # print_answer
        print_list = print_answer(user_input, best_mol, rmsd, score, pdb_id, idx)
        txt_list.extend(print_list)
        txt_list.append('-------------')

    print('\n\nYour total score: %s' % '待开发')
    txt_list.append('\n\nTotal score: %s\n' % '待开发')

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
