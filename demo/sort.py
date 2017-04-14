

def bubble_sort(ary):
    n = len(ary)
    for i in range(n):
        for j in range(i + 1, n):
            if ary[i] > ary[j]:
                ary[i], ary[j] = ary[j], ary[i]
    return ary


def select_sort(ary):
    n = len(ary)
    for i in range(n):
        min = i
        for j in range(i + 1, n):
            if ary[j] < ary[min]:
                min = j
        ary[min], ary[i] = ary[i], ary[min]
    return ary


def insert_sort(ary):
    n = len(ary)
    for i in range(1, n):
        if ary[i] < ary[i - 1]:
            temp = ary[i]
            index = i
            for j in range(i - 1, -1, -1):
                if ary[j] > temp:
                    ary[j + 1] = ary[j]
                    index = j
                else:
                    break
            ary[index] = temp
    return ary


def merge_sort(ary):
    if len(ary) <= 1:
        return ary

    num = int(len(ary) / 2)
    left = merge_sort(ary[:num])
    right = merge_sort(ary[num:])
    return merge(left, right)


def merge(left, right):
    l, r = 0, 0
    result = []

    while l < len(left) and r < len(right):
        if left[l] < right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1

    result += left[l:]
    result += right[r:]

    return result


def quick_sort(ary):
    return qsort(ary, 0, len(ary) - 1)


def qsort(ary, left, right):
    if left >= right:
        return ary

    key = ary[left]
    lp = left
    rp = right

    while lp < rp:
        while ary[rp] >= key and lp < rp:
            rp -= 1
        while ary[lp] <= key and lp < rp:
            lp += 1
        ary[lp], ary[rp] = ary[rp], ary[lp]

    ary[left], ary[lp] = ary[lp], ary[left]

    qsort(ary, left, lp - 1)
    qsort(ary, rp + 1, right)

    return ary

if __name__ == '__main__':
    ary = [1, 8, 3, 6, 5, 4, 7, 2, 9, 0, 241, 41, 1, 7, 3]
    # print bubble_sort(ary)
    # print select_sort(ary)
    # print insert_sort(ary)
    # print merge_sort(ary)
    print quick_sort(ary)
