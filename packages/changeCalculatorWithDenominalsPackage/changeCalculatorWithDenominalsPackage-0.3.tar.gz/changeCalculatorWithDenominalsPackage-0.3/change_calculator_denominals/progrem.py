import sys
OF_COIN = ' of coin '
INPUT_WANTEDNUM = 'enter the number you want to get from denominals \n'
INPUT_DENOMINALS = 'enter list of denominals separated by space \n'
NO_COMBINATION = 'no combination found.'
COINS_NEEDED_BASE = 'coins needed are: '

def result_to_string(amt_coins, arr_coins):
    if len(arr_coins) == 0:
        return NO_COMBINATION

    arr_coins.sort()
    current_coin_amount = 1
    result_string = COINS_NEEDED_BASE
    if amt_coins == 1:
        result_string += '1 of ' + arr_coins[0]
        return result_string
    for i in range(0, amt_coins):
        if i == 0:
            continue
        if arr_coins[i] == arr_coins[i-1]:
            current_coin_amount += 1
            if (i+1) == amt_coins:
                result_string += str(current_coin_amount) + OF_COIN + str(arr_coins[i])
                return result_string
        else:
            result_string += str(current_coin_amount) + OF_COIN + str(arr_coins[i-1]) + ' and '
            current_coin_amount = 1
            if i+1 == amt_coins:
                result_string += str(current_coin_amount) + OF_COIN + str(arr_coins[i])
                return result_string
    return result_string


def calculate_recursive(coins, len_coins, needed_amt, curr_array, result_array, min_coins):
    if (needed_amt == 0):
        return 0

    for coin in range(0, len_coins):
        curr_array.append(int(coins[coin]))
        if sum(curr_array) == needed_amt:
            if len(curr_array) < min_coins :
                min_coins = len(curr_array)
                result_array = list(curr_array)
            curr_array.pop()
            continue
        elif sum(curr_array) < needed_amt:
             result_array, min_coins = calculate_recursive(coins, len_coins, needed_amt, curr_array, result_array, min_coins)
        elif sum(curr_array) > needed_amt:
            curr_array.pop()
    if(len(curr_array) != 0):
        curr_array.pop()
    return result_array, min_coins


def main():
    wanted_number = input(INPUT_WANTEDNUM)
    coins_input = input(INPUT_DENOMINALS)
    coins = coins_input.split()
    result_array, min_coins = calculate_recursive(coins, len(coins), int(wanted_number), [], [], sys.maxsize)
    print(result_to_string(min_coins, result_array))


if __name__ == '__main__':
    main()
