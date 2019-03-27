import numpy, pdb, random, os

cont_attributes_id = ['elevation', 'aspect', 'slope', 'horizontal_distance_hydrology', 'vertical_distance_hydrology', 'horizontal_dist_roadways', 'hillshade_9am','hillshade_noon' , 'hillshade_3pm', 'horizontal_dist_f_points']
train_tuples_per_class = 66400
offset = 10


def entropy(entry_values):
    #pdb.set_trace()
    sample_size = len(entry_values)
    if sample_size == 0:
        return sample_size

    total_samples = sum(entry_values)
    pi = list(map(lambda x: x/total_samples, entry_values))
    ent = 0
    for p_i in pi:
        if p_i > 0:
            ent += (-p_i)*numpy.log2(p_i)
    if ent > 1:
        return 1
    else:
        return ent

def continue_gain(set_entropy, dic, index):
    q1_values = dic[index].get('q1')[0]
    q1_size = len(q1_values)
    q1_entropy = entropy(dic[index].get('q1')[1])

    q2_values = dic[index].get('q2')[0]
    q2_size = len(q2_values)
    q2_entropy = entropy(dic[index].get('q2')[1])

    q3_values = dic[index].get('q3')[0]
    q3_size = len(q3_values)
    q3_entropy = entropy(dic[index].get('q3')[1])

    q4_values = dic[index].get('q4')[0]
    q4_size = len(q4_values)
    q4_entropy = entropy(dic[index].get('q4')[1])

    print("q1 entropy for " + str(index) + " attribute: " + str(q1_entropy) )
    print("q2 entropy for " + str(index) + " attribute: " + str(q2_entropy) )
    print("q3 entropy for " + str(index) + " attribute: " + str(q3_entropy) )
    print("q4 entropy for " + str(index) + " attribute: " + str(q4_entropy) )

    total_gain = set_entropy - ((q1_size*q1_entropy)+(q2_size*q2_entropy)+(q3_size*q3_entropy)+(q4_size*q4_entropy))/120
    return total_gain

def divide_binary_data(sorted_attributes, file_name):
    #pdb.set_trace()

    for i in range(0, len(sorted_attributes)):
        zero_half = []
        one_half = []

        zero_soils = [0, 0, 0, 0, 0, 0, 0]
        one_soils = [0, 0, 0, 0, 0, 0, 0]

        f = open(file_name, 'r')
        for line in f:
            values = line.split(',')
            values[-1] = values[-1].replace('\n','')

            print(values[i + offset])

            if (int(values[i + offset]) == 0):
                zero_soils[int(values[-1]) -1] += 1
            else:
                one_soils[int(values[-1]) -1] += 1
        f.close()
        #pdb.set_trace()
        binary_dic = {
            '0' : zero_soils,
            '1' : one_soils
        }
        #print(zero_soils)
        #print(one_soils)


def divide_continue_data(sorted_attributes, file_name):
    main_return = []
    quantils_array = []
    #pdb.set_trace()
    for i in range(0, len(sorted_attributes)):
        q1 = numpy.quantile(sorted_attributes[i], 0.25)
        q2 = numpy.quantile(sorted_attributes[i], 0.5)
        q3 = numpy.quantile(sorted_attributes[i], 0.75)
        q4 = numpy.quantile(sorted_attributes[i], 1.0)

        quantils_array.append([cont_attributes_id[i], q1, q2, q3, q4])

        first_quarter = []
        second_quarter = []
        third_quarter = []
        fourth_quarter = []

        for j in range(0,len(sorted_attributes[i])):
            if (sorted_attributes[i][j] < q1):
                first_quarter.append(sorted_attributes[i][j])
            elif(sorted_attributes[i][j] < q2):
                second_quarter.append(sorted_attributes[i][j])
            elif(sorted_attributes[i][j] < q3):
                third_quarter.append(sorted_attributes[i][j])
            else:
                fourth_quarter.append(sorted_attributes[i][j])

        first_soils = [0, 0, 0, 0, 0, 0, 0]
        second_soils = [0, 0, 0, 0, 0, 0, 0]
        third_soils = [0, 0, 0, 0, 0, 0, 0]
        fourth_soils = [0, 0, 0, 0, 0, 0, 0]

        f = open(file_name, 'r')
        for line in f:
            values = line.split(',')
            values[len(values)-1] = values[len(values)-1].replace('\n','')

            if (float(values[i]) < q1):
                first_soils[int(values[-1])] += 1
            elif(float(values[i]) < q2):
                second_soils[int(values[-1])] += 1
            elif(float(values[i]) < q3):
               third_soils[int(values[-1])] += 1
            else:
               fourth_soils[int(values[-1])] += 1

        dic = {
            'q1' : [first_quarter, first_soils],
            'q2' : [second_quarter, second_soils],
            'q3' : [third_quarter, third_soils],
            'q4' : [fourth_quarter, fourth_soils]
        }

        main_return.append(dic)
    #pdb.set_trace()
    return main_return, quantils_array

def trainning_samples(a,b):
    samples_id = []
    global train_tuples_per_class
    while len(samples_id) < train_tuples_per_class:
        x = random.randint(a,b)
        if not x in samples_id:
                samples_id.append(x)

    return samples_id

def custom_main():

    if not (os.path.isfile('data/train_set.txt')):
        f = open('data/covtype.data', 'r')
        train_samples = trainning_samples(1, 50)
        train_samples += trainning_samples(51, 100)
        train_samples += trainning_samples(101,150)

        train_f = open('data/train_set.txt', 'a')
        test_f = open('data/test_set.txt', 'a')

        i  = 1
        for line in f:
            if i in train_samples:
                train_f.write(line)
            else:
                test_f.write(line)
            i += 1

        test_f.close()
        f.close()
        train_f.close()

    p_i = [0,0,0,0,0,0,0]
    each_column = []
    for i in range(0,55):
        each_column.append([])
    
    train_f = open('data/train_set.txt', 'r')
    
    for line in train_f:
        values = line.split(',')
        values[-1] = values[-1].replace('\n','')
        p_i[int(values[-1])-1] += 1 #forest classes

        for i in range(0, len(values)):
            each_column[i].append(int(values[i]))
    
    train_f.close()

    sorted_data = []
    for column in each_column:
        sorted_data.append(sorted(column))
    #pdb.set_trace()
    
    set_entropy = entropy(p_i)
    print(set_entropy)
    
    dic_quantiles, arr_quantiles = divide_continue_data(sorted_data[:10],'data/train_set.txt') #just quantitive attributes

    divide_binary_data(sorted_data[10:],'data/train_set.txt')  #just qualitative attributes
    


    
    
    #gains = []
    #fst_attr_gain = continue_gain(set_entropy, dic_quantiles, 0)
    #gains.append(fst_attr_gain)
    #snd_attr_gain = continue_gain(set_entropy, dic_quantiles, 1)
    #gains.append(snd_attr_gain)
    #thr_attr_gain = continue_gain(set_entropy, dic_quantiles, 2)
    #gains.append(thr_attr_gain)
    #fth_attr_gain = continue_gain(set_entropy, dic_quantiles, 3)
    #gains.append(fth_attr_gain)
    #print(gains)

    #final_attr_ordered = []
    #final_quantil_ordered = []
    #for i in gains:
    #    final_quantil_ordered.append(arr_quantiles[gains.index(max(gains))])
    #    final_attr_ordered.append(gains.index(max(gains)))
    #    gains[gains.index(max(gains))] = -1

    #return final_attr_ordered, final_quantil_ordered

def data_order(attributes_order, file_name):
    file = open(file_name, 'r')
    ordered_data = []
    for line in file:
        split_line = line.split(',')
        split_line[-1] = split_line[-1].replace('\n', '')
        ordered_line = []
        for index in attributes_order:
            ordered_line.append(float(split_line[index]))
        ordered_line.append(split_line[-1])
        ordered_data.append(ordered_line)
    file.close()
    return ordered_data