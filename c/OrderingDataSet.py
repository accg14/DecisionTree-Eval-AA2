
def order_data_set():
  f = open('covtype.data', 'r')
  f1 = open('soil_1.txt', 'a')
  f2 = open('soil_2.txt', 'a')
  f3 = open('soil_3.txt', 'a')
  f4 = open('soil_4.txt', 'a')
  f5 = open('soil_5.txt', 'a')
  f6 = open('soil_6.txt', 'a')
  f7 = open('soil_7.txt', 'a')

  for line in f:
    array_line = line.split(',')
    if int(array_line[-1]) == 1:
      f1.write(line)
    elif int(array_line[-1]) == 2:
      f2.write(line)
    elif int(array_line[-1]) == 3:
      f3.write(line)
    elif int(array_line[-1]) == 4:
      f4.write(line)
    elif int(array_line[-1]) == 5:
      f5.write(line)
    elif int(array_line[-1]) == 6:
      f6.write(line)
    else:
      f7.write(line)

  f.close()
  f1.close()
  f2.close()
  f3.close()
  f4.close()
  f5.close()
  f6.close()
  f7.close()

def trainning_samples(percent):
  samples_id = []
  for i in range(1,round(percent)):
    samples_id.append(i)

  return samples_id

def make_training_and_test_set(file, train_f, test_f, train_samples):
  f = open(file, 'r')
  i  = 1
  for line in f:
    if i in train_samples:
      train_f.write(line)
    else:
      test_f.write(line)
    i += 1
  f.close()


def get_training_and_test_set():
  lengths = [211840, 283301, 35754, 2747, 9493, 17367, 20510]
  train_f = open('training_set.txt','a')
  test_f = open('test_set.txt', 'a')

  train_samples = []
  train_samples = trainning_samples(lengths[0] * 0.8)
  make_training_and_test_set('soil_1.txt', train_f, test_f, train_samples)
  train_samples = trainning_samples(lengths[1] * 0.8)
  make_training_and_test_set('soil_2.txt', train_f, test_f, train_samples)
  train_samples = trainning_samples(lengths[2] * 0.8)
  make_training_and_test_set('soil_3.txt', train_f, test_f, train_samples)
  train_samples = trainning_samples(lengths[3] * 0.8)
  make_training_and_test_set('soil_4.txt', train_f, test_f, train_samples)
  train_samples = trainning_samples(lengths[4] * 0.8)
  make_training_and_test_set('soil_5.txt', train_f, test_f, train_samples)
  train_samples = trainning_samples(lengths[5] * 0.8)
  make_training_and_test_set('soil_6.txt', train_f, test_f, train_samples)
  train_samples = trainning_samples(lengths[6] * 0.8)
  make_training_and_test_set('soil_7.txt', train_f, test_f, train_samples)

  train_f.close()
  test_f.close()

if __name__== "__main__":
  #order_data_set()
  get_training_and_test_set()





