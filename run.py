import argparse
from utils import check_outstanding, check_overdue, get_full_record


def main():
    parser = argparse.ArgumentParser('Check records.')
    parser.add_argument('--overdue', action='store_true')
    parser.add_argument('--outstanding', action='store_true')
    parser.add_argument('--update', action='store_true')
    args = parser.parse_args()

    record = get_full_record()
    if args.overdue:
        print(f'OVERDUE AMOUNT IS {check_overdue(record):.2f}')
    elif args.outstanding:
        print(f'OUTSTANDING AMOUNT IS {check_outstanding(record):.2f}')
    elif args.update:
        with open('README.md', 'r+') as f:
            lines = f.readlines()
            lines[-1] = ''



if __name__ == '__main__':
    main()
