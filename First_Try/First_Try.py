import csv
import numpy as np

#---------------------------------------------------------------------

global gift_type 
gift_type = ('ball', 'bike', 'blocks', 'book', 'coal', 'doll', 'gloves', 'horse', 'train')
global gift_quantity
gift_quantity = (1100, 500, 1000, 1200, 166, 1000, 200, 1000, 1000)

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

#---------------------------------------------------------------------

def sample_horse(size):
    return np.maximum(0, np.random.normal(5,2,size))

def sample_ball(size):
    return np.maximum(0, 1 + np.random.normal(1,0.3,size))

def sample_bike(size):
    return np.maximum(0, np.random.normal(20,10,size))

def sample_train(size):
    return np.maximum(0, np.random.normal(10,5,size))

def sample_coal(size):
    return 47 * np.random.beta(0.5,0.5,size)

def sample_book(size):
    return np.random.chisquare(2,size)

def sample_doll(size):
    return np.random.gamma(5,1,size)

def sample_blocks(size):
    return np.random.triangular(5,10,20,size)

def sample_gloves(size):
    dist1 = 3.0 + np.random.rand(size)
    dist2 = np.random.rand(size)
    toggle = np.random.rand(size) < 0.3
    dist2[toggle] = dist1[toggle]
    return dist2

def measure_weight(i, size):
    if i == 0:
        return sample_ball(size)
    elif i == 1:
        return sample_bike(size)
    elif i == 2:
        return sample_blocks(size)
    elif i == 3:
        return sample_book(size)
    elif i == 4:
        return sample_coal(size)
    elif i == 5:
        return sample_doll(size)
    elif i == 6:
        return sample_gloves(size)
    elif i == 7:
        return sample_horse(size)   
    elif i == 8:
        return sample_train(size) 
    
#---------------------------------------------------------------------
    
def generate_gift():
    all_gift = []
    for i in range(9):
        single_line = []
        for j in range(gift_quantity[i]):
            single_line.append(gift_type[i]+'_'+str(j))
        all_gift.append(single_line)
    return all_gift
    
#---------------------------------------------------------------------

def split_gift(bag):
    bag_treated = []
    bag = bag[0].split()
    for item in bag:
        bag_treated.append(item.split('_')[0])
    return bag_treated

def count_gift(bag_treated):
    count = zerolistmaker(9)
    count[0] = bag_treated.count('ball')
    count[1] = bag_treated.count('bike')
    count[2] = bag_treated.count('blocks')
    count[3] = bag_treated.count('book')
    count[4] = bag_treated.count('coal')
    count[5] = bag_treated.count('doll')
    count[6] = bag_treated.count('gloves')
    count[7] = bag_treated.count('horse')
    count[8] = bag_treated.count('train')
    return count

#---------------------------------------------------------------------

def convert_to_item(file):
    final_count = []
    with open(file) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for i in f_csv:
            i = split_gift(i)
            single_count = count_gift(i)
            final_count.append(single_count)
    return final_count
 
def convert_to_submission(number_count):
    gift_storage = generate_gift()
    order_of_distribution = zerolistmaker(9)
    submission = []
    for bag in number_count:
        sub_temp = ''
        for i in range(9):
            for j in range(bag[i]):
                if sub_temp == '':
                    sub_temp = gift_storage[i][order_of_distribution[i]]
                    order_of_distribution[i] = order_of_distribution[i] + 1
                else:
                    sub_temp = sub_temp + ' ' + gift_storage[i][order_of_distribution[i]]
                    order_of_distribution[i] = order_of_distribution[i] + 1
        submission.append(sub_temp)
    final_submission = []
    for i in submission:
        final_submission.append([i])
    return final_submission

#---------------------------------------------------------------------

def generate_submission(submission):
    csvfile = file('submission.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['Gifts'])
    for i in submission:
        writer.writerow(i)
        
#---------------------------------------------------------------------
    
def calculate_score(number_count):
    score_record = []
    for bag in number_count:
        score_temp = 0
        for i in range(9):
            if not bag[i] == 0:
                score_temp = score_temp + sum(measure_weight(i, bag[i]))
        score_record.append(score_temp)
    return score_record
             
#---------------------------------------------------------------------
         
def analysis():                   
    number_count = convert_to_item('submission_10.csv') 
    score_final = calculate_score(number_count) 
    
    print 'Number of the bags (score > 50): ' + str(len(filter(lambda x: x > 50, score_final)))
    print
    arr = np.array(score_final)
    position = np.where(arr > 50)[0]
    print 'Position of the abnormal bags:'
    for i in position:
        print i
    print
    print 'Contents of abnormal bags:'
    for i in position:
        print number_count[i]
    

analysis()



    
        
        
        
    
