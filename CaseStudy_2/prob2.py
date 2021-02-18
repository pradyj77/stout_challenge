import collections

CURRENT = 2017
PREV = 2016
FIRST = 2015


def load_csv(path):
    revenue = collections.defaultdict(lambda: collections.defaultdict(float))
    with open(path, "r") as ipfile:
        for line in ipfile:
            line = line[:-1].split(",")
            revenue[int(line[-1])][line[1]] += float(line[2])
    return revenue


def all_revenues(revenue, year):
    return sum(revenue[year].values())


def new_customer_revenue_current(revenue):
    new_customers = set(revenue[CURRENT].keys()) - set(revenue[PREV].keys())
    sum_ = 0.0
    for customer in new_customers:
        sum_ += revenue[CURRENT][customer]
    return sum_


def new_customer_revenue_prev(revenue):
    new_customers = set(revenue[PREV].keys()) - set(revenue[FIRST].keys())
    sum_ = 0.0
    for customer in new_customers:
        sum_ += revenue[PREV][customer]
    return sum_


def current_existing_customers_revenue(revenue):
    existing_customers = set(revenue[CURRENT].keys()) & set(revenue[PREV].keys())
    sum_ = 0.0
    for customer in existing_customers:
        sum_ += revenue[CURRENT][customer]
    return sum_


def prev_existing_customers_revenue(revenue):
    existing_customers = set(revenue[PREV].keys()) & set(revenue[FIRST].keys())
    sum_ = 0.0
    for customer in existing_customers:
        sum_ += revenue[PREV][customer]
    return sum_


def attrition_revenue(revenue):
    sum_ = 0.0
    lost_customers_first = set(revenue[FIRST].keys()) - set(revenue[PREV].keys()) - set(revenue[CURRENT].keys())
    for customer in lost_customers_first:
        sum_ += revenue[FIRST][customer]
    lost_customers_prev = set(revenue[PREV].keys()) - set(revenue[CURRENT].keys())
    for customer in lost_customers_prev:
        sum_ += revenue[PREV][customer]
    return sum_


def total_customers(revenue, year):
    return len(revenue[year])


def get_new_customers(revenue, year):
    return sorted(set(revenue[year].keys()) - set(revenue[year - 1].keys()))


def get_lost_customers(revenue, year):
    return sorted(set(revenue[year-1].keys()) - set(revenue[year].keys()))


if __name__ == "__main__":
    revenue = load_csv("casestudy.csv")
    print("Total revenue:", all_revenues(revenue, CURRENT), all_revenues(revenue, PREV), all_revenues(revenue, FIRST)) 
    print("New customer revenue in", CURRENT, new_customer_revenue_current(revenue))
    print("New customer revenue in", PREV, new_customer_revenue_prev(revenue))
    print("Existing customer growth",
          current_existing_customers_revenue(revenue) - prev_existing_customers_revenue(revenue))
    print("Revenue lost in attrition", attrition_revenue(revenue))
    print("Existing customer revenue", CURRENT, current_existing_customers_revenue(revenue))
    print("Existing customer revenue", PREV, prev_existing_customers_revenue(revenue))
    print("Total customers", total_customers(revenue, CURRENT), total_customers(revenue, PREV), total_customers(revenue, FIRST))

    new_customers_current = get_new_customers(revenue, CURRENT)
    new_customers_prev = get_new_customers(revenue, PREV)
    print("New customers size", len(new_customers_current), len(new_customers_prev))
    op = []
    op.extend([f"{x},{CURRENT}" for x in new_customers_current])
    op.extend([f"{x},{PREV}" for x in new_customers_prev])
    with open("new_customers.csv", "w") as opfile:
        opfile.write('\n'.join(op))

    lost_customers_current = get_lost_customers(revenue, CURRENT)
    lost_customers_prev = get_lost_customers(revenue, PREV)
    print("Lost customers size", len(lost_customers_current), len(lost_customers_prev))
    op = []
    op.extend([f"{x},{CURRENT}" for x in lost_customers_current])
    op.extend([f"{x},{PREV}" for x in lost_customers_prev])
    with open("lost_customers.csv", "w") as opfile:
        opfile.write('\n'.join(op))
