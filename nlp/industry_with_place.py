import csv
import pickle
from collections import defaultdict

# read data
FILE_NAME = '4w_trainset.csv'


def file_write(dictionary, filename, key_count, val_len_count):
    filename = '{}.txt'.format(filename)
    fileObj = open(filename, 'w')
    for key, value in dictionary.items():
        fileObj.write(key + ':' + str(list(value)))
        fileObj.write('\n')
    if key_count != 0 and val_len_count != 0:
        fileObj.write('key的总数：{}'.format(key_count))
        fileObj.write('\n')
        fileObj.write('value的长度为1的总数: {}'.format(val_len_count))
    fileObj.close()


def read_data():
    valid_data = []

    try:
        with open(FILE_NAME, 'r', encoding='GB18030') as db01:
            reader = csv.reader(db01)
            for row in reader:
                valid_data.append(row)
    except csv.Error as e:
        print(e)

    return valid_data


def save_in_four_kw(valid_data):
    dictionary1 = defaultdict(list)
    for i in valid_data[1:]:
        # value
        place = i[9]
        # key
        kw1 = i[2]
        kw2 = i[3]
        kw3 = i[4]
        kw4 = i[5]
        # kw = kw1+'-'+kw2+'-'+kw3+'-'+kw4
        # dictionary1[kw].add(place)
        dictionary1[kw1].append(place)
        dictionary1[kw2].append(place)
        dictionary1[kw3].append(place)
        dictionary1[kw4].append(place)
    key_count = 0
    val_len_count = 0
    for key, value in dictionary1.items():
        key_count += 1
        if len(value) == 1:
            val_len_count += 1

    with open('tf_idf_idf_4w_training_set.pickle', 'wb') as f:
        pickle.dump(dictionary1, f, pickle.HIGHEST_PROTOCOL)


def save_in_file(valid_data):
    # #build dict = {key(机构名): value(行业分类1，2，3，4)}
    dictionary2 = defaultdict(list)
    for i in valid_data[1:]:
        kw1 = i[2]
        kw2 = i[3]
        kw3 = i[4]
        kw4 = i[5]
        # kw = kw1+'-'+kw2+'-'+kw3+'-'+kw4
        place = i[9]
        # dictionary2[place].append(kw)
        dictionary2[place].append(kw1)
        dictionary2[place].append(kw2)
        dictionary2[place].append(kw3)
        dictionary2[place].append(kw4)
    key_count_2 = 0
    val_len_count_2 = 0
    for key, value in dictionary2.items():
        key_count_2 += 1
        if len(value) == 1:
            val_len_count_2 += 1

    file_write(dictionary2, '处置单位与行业分类关系', key_count_2, val_len_count_2)

    dict_industry_count = defaultdict(list)

    for key, value in dictionary2.items():
        dict2_industry_count = {}
        for i in value:
            list_temp = []
            list_temp.append(value.count(i))
            dict2_industry_count[i] = list_temp
        dict_industry_count[key].append(dict2_industry_count)

    file_write(dict_industry_count, '行业分类与处置单位关系testset字典版3', 0, 0)
    with open('dict_industry_count_testset1_4w_training_set.pickle', 'wb') as f:
        pickle.dump(dict_industry_count, f, pickle.HIGHEST_PROTOCOL)


def industry_class(valid_data):
    # 统计行业分类
    industry_count = []
    for i in valid_data[1:]:
        # value
        # key
        kw1, kw2, kw3, kw4 = i[2], i[3], i[4], i[5]
        # kw = kw1+'-'+kw2+'-'+kw3+'-'+kw4
        industry_count.append(kw1)
        industry_count.append(kw2)
        industry_count.append(kw3)
        industry_count.append(kw4)

    industry_count_set = set(industry_count)
    industry_count_lst = []
    dict = {}
    for i in industry_count_set:
        dict[i] = industry_count.count(i)
    industry_count_lst.append(dict)
    print(industry_count_lst)

    sorted_industry = sorted(industry_count_lst, key=lambda k: k.values())
    filename = '行业分类的统计testset_w4_v3.txt'
    fileObj = open(filename, 'w')
    for i in sorted_industry:
        for key, value in i.items():
            fileObj.write(key + ":" + str(value))
            fileObj.write('\n')
    fileObj.close()
    with open('tfidf_4w_training_set.pickle', 'wb') as f:
        pickle.dump(dict, f, pickle.HIGHEST_PROTOCOL)


def main():
    valid_data = read_data()
    save_in_file(valid_data)
    save_in_four_kw(valid_data)
    industry_class(valid_data)


if __name__ == '__main__':
    main()
