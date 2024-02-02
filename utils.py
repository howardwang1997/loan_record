import datetime
import os
from typing import Tuple


def _initiate_file(path: str = './RECORD.txt'):
    assert not os.path.isfile(path)
    with open(path, 'w+') as f:
        f.write('')
    with open('WAIVE_INTEREST.txt'):
        f.write('')


def _format(date_string):
    assert len(date_string) == 8
    if date_string[:3] == '202':
        yyyy, mm, dd = int(date_string[:4]), int(date_string[4:6]), int(date_string[-2:])
    elif date_string[-4:-1] == '202':
        dd, mm, yyyy = int(date_string[:2]), int(date_string[2:4]), int(date_string[-4:])
        assert mm <= 12
    else:
        raise ValueError('Date type not supported')
    return datetime.date(yyyy, mm, dd)


def _calc_interest(start_date: datetime.date,
                   end_date: datetime.date,
                   amount: float,
                   rate: float,
                   compound: bool = False):
    days_overdue = (end_date - start_date).days
    if compound:
        interest = (1 + rate) ** days_overdue
    else:
        interest = 1 + rate*days_overdue
    return amount * interest


def loan(date: datetime.date,
         amount: int,
         expected_repayments: Tuple[datetime.date, int],
         daily_interest: float = 0.001,
         compound: bool = False,
         path: str = './RECORD.txt'):
    if not os.path.isfile(path):
        _initiate_file(path)
    compound_flag = 'COMPOUND' if compound else 'SIMPLE'

    with open(path, 'a+') as f:
        f.write(f'LOAN {date.isoformat()}  {amount}  EXPECTED_REPAYMENT {expected_repayments[0].isoformat()}  {expected_repayments[1]}  OVERDUE_INTEREST_RATE {daily_interest}  {compound_flag}')


def repay(date: datetime.date,
          amount: float,
          path: str = './RECORD.txt'):
    assert os.path.isfile(path)
    with open(path, 'a+') as f:
        f.write(f'REPAY {date.isoformat()}  {amount}')


def waive_interest(start_date: datetime.date,
                   end_date: datetime.date,
                   path: str = './WAIVE_INTEREST.txt'):
    with open(path, 'a+') as f:
        f.write(f'{start_date.isoformat()} to {end_date.isoformat()}')


def get_full_record(path: str = './RECORD.txt',
                    waive_interest: str = './WAIVE_INTEREST.txt'):
    assert os.path.isfile(path) and os.path.isfile(waive_interest)
    with open(path) as f:
        data = f.readlines()
    with open(waive_interest) as f:
        waiver = f.readlines()

    record = []
    for line in data:
        if line[0] == 'L':
            info = line.split()
            exp_repay_date = info[4].split('-')
            exp_repay_date = datetime.date(int(exp_repay_date[0]), int(exp_repay_date[1]), int(exp_repay_date[2]))
            exp_repay_amount = int(info[5])
            interest_rate = float(info[7])
            record.append([exp_repay_date, 'LOAN', exp_repay_amount, interest_rate])
        else:
            info = line.split()
            repay_date = info[1].split('-')
            repay_date = datetime.date(int(repay_date[0]), int(repay_date[1]), int(repay_date[2]))
            repay_amount = int(info[2])
            record.append([repay_date, 'REPAY', repay_amount])

    for line in waiver:
        info = line.split()
        start_date = info[0].split('-')
        start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date = info[1].split('-')
        end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        record.append([start_date, 'START_WAIVER'])
        record.append([end_date, 'END_WAIVER'])

    return record


def check_overdue(record, waive_interest=None):
    record.sort()
    now = datetime.date.today()
    amount = 0
    loans = []
    repays = 0
    interest_rates = []
    waiver = False

    for line in record:
        if line[0] >= now:
            continue

        loan_flag = line[1]

        if loan_flag == 'LOAN':
            amount += _calc_interest(line[0], now, line[2], line[3])
            interest_rates.append(line[3])
            loans.append((line[2]) + loans[-1])
        elif loan_flag == 'REPAY':
            order = sum([l <= repays for l in loans])
            amount -= _calc_interest(line[0], now, line[2], interest_rates[order])
        elif loan_flag == 'START_WAIVER':
            waiver = True
        else:
            waiver = False

    return amount


def check_outstanding(record, waive_interest=None):
    record.sort()
    now = datetime.date.today()
    overdue = check_overdue(record, waive_interest)
    outstanding = 0

    for line in record:
        if line[0] < now:
            continue
        assert line[1] == 'LOAN'

        outstanding += line[2]

    return outstanding + overdue
