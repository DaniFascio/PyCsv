import click
import numpy as np
import os
import pandas


@click.command()
@click.argument('file', type=str, required=True)
@click.argument('output', type=str, required=False)
@click.option('--sep', '-s', type=str, default=',', help='Separator between values in groups column')
def csv(file, sep, output):

    if not file:
        return print('File path not specified')

    if not output:
        path, name = os.path.split(file)
        name, ext = os.path.splitext(name)
        file_output = os.path.join(path, name + '_export' + ext)
    else:
        file_output = output

    print(f'{file} will be converted to another format CSV with sep="{sep}"')

    csv_file = pandas.read_csv(file, sep=';', header=0, dtype=str)
    csv_file = csv_file.replace({np.nan: None})
    print(csv_file)

    group_list = []
    curr_id = None
    prev_id = None
    new_file = pandas.DataFrame(columns=csv_file.columns)
    for _, x in csv_file.iterrows():
        id_user = x['id_user']
        if id_user and len(group_list):
            new_file.loc[len(new_file)] = [str(prev_id), ','.join(group_list)]
            group_list = []
        group_list.append(x['group_id'])
        if id_user:
            prev_id = id_user

    if len(group_list):
        new_file.loc[len(new_file)] = [str(prev_id), ','.join(group_list)]


    new_file.to_csv(file_output, index=False)



if __name__ == '__main__':
    csv()

