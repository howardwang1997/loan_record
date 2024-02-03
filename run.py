import argparse
import datetime
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
        with open('README.md') as f:
            lines = f.readlines()
        ovd, ots = check_overdue(record), check_outstanding(record)
        lines[-1] = f'### OVERDUE: HK$ {ovd:.2f} , OUTSTANDING: HK$ {ots: .2f} ({datetime.date.today().isoformat()})'
        with open('README.md', 'w+') as f:
            f.write(''.join(lines))


if __name__ == '__main__':
    main()
