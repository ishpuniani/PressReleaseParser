import os
import json


def main():
    """
    Read file
    change date
    write to new file
    :return:
    """
    dir = 'releases'
    new_dir = 'releases2'
    for filename in os.listdir(dir):
        with open(dir + '/' + filename) as json_file:
            new_pr = []
            pr_arr = json.load(json_file)
            for pr in pr_arr:
                pr['date'] = ''.join(pr['date'])
                new_pr.append(pr)
            with open(new_dir + '/' + filename, 'w') as fp:
                json.dump(new_pr, fp, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
