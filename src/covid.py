import pandas
import requests
import datetime


num_to_month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}
norway_sum_up_date = datetime.datetime(2020, 6, 28)

def inbetween_nums(pre, post):
    small = pre if pre < post else post
    big = pre if pre > post else post
    reverse = pre > post
    it = abs(big - small) // 4
    if not it:
        it = 1
    nums = list(range(small + it, big, it))
    if len(nums) == 1:
        nums = nums * 3
    if len(nums) == 2:
        nums.append(nums[1])
    if len(nums) == 4:
        nums.pop()
    if len(nums) == 5:
        nums.pop(1)
        nums.pop(3)

    return nums if not reverse else nums[::-1]


def add_row(row, data, country):
    """
        Parses the row and adds the date and value to the given data set.
    """

    row = row.split(",")
    data[0].append(f"{row[1]} {num_to_month[int(row[2])]} {row[3]}")
    data[1].append(int(row[4]))
    if country == 'norway':
        date = datetime.datetime(*[int(x) for x in row[0].split('/')][::-1])
        # Smooth out missing data from sundays, mondays and thursdays
        if date > norway_sum_up_date and date.weekday() == 2:
            post = int(row[4])
            pre = data[1][-5]
            nums = inbetween_nums(pre, post)
            data[1][-4] = nums[0]
            data[1][-3] = nums[1]
            data[1][-2] = nums[2]


def get_covid():
    """
        Returns the data on Covid cases in Norway and USA.
        The data is fetched from the European Centre for Disease Prevention and Control.
    """

    # Download the data
    res = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/data.csv")

    usa = [], []
    norway = [], []
    # Goes through the data and adds the values for Norway and USA
    for line in reversed(res.text.split("\n")):
        if "USA" in line:
            add_row(line, usa, 'usa')
        elif "Norway" in line:
            add_row(line, norway, 'norway')

    return norway, usa

