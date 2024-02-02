import argparse
from utils import loan, repay, waive_interest, _format

def main():
    parser = argparse.ArgumentParser('Set changes for record.')
    parser.add_argument('date', type=str)
    parser.add_argument('--loan', type=int)
    parser.add_argument('--repay', type=float)
    parser.add_argument('--waive_interest', type=str, help='20231231-20240101')
    parser.add_argument('--repay_date', type=str)
    parser.add_argument('--repay_amount', type=float)
    parser.add_argument('--interest_rate', type=float)
    args = parser.parse_args()

    date = _format(args.date)
    if args.loan:
        loan(date, args.loan, (_format(args.repay_date), args.repay_amount), args.interest_rate, False)
    elif args.repay:
        repay(date, args.repay)
    else:
        dates = args.waive_interest.split('-')
        waive_interest(_format(dates[0]), _format(dates[1]))


if __name__ == '__main__':
    main()
