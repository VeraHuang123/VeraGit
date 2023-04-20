def find_max_sum(num_list):
    print(num_list)
    num_max = []
    for i in range(2):
        first_max = max(num_list)
        num_list.remove(first_max)
        num_max.append(first_max)
    print(f'其中最大两数之和为：{sum(num_max)}')
#find_max_sum([11,7,1,9,10])