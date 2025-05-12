import json


def check_capacity(max_capacity: int, guests: list) -> bool:
    dates = []
    for guest in guests:
        dates.extend([(guest['check-out'], 1), (guest['check-in'], -1)])

    dates.sort(key=lambda x: (x[0], -x[1]))
    for date in dates:
        max_capacity += date[1]
        if max_capacity < 0:
            return False

    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    s = input()
    if s:
        n = int(s)
    else:
        n = int(input())

    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)

    result = check_capacity(max_capacity, guests)
    print(result)
