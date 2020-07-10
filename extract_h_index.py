import numpy as np 
import pandas as pd 
import os


class HIndexCalculator(object):
    '''
        Extract all h-index-related information from raw data
    '''
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path, header=None)
        self.data = self.data.iloc[5:, :]
        self.pure_data = self.data.iloc[2:, 7:self.data.shape[1]-1]
        self.h_index = []
        self.year_list = self.data.iloc[2:, 0]
        self.year_list = pd.DataFrame(list(map(eval, list(self.year_list))))
        self.journal_list = self.data.iloc[2:, 4]
        self.cite_num = self.data.iloc[1, self.data.shape[1]-1]

    def get_h_index(self):
        self.cum_data = np.array(self.pure_data)
        self.n, self.m = self.cum_data.shape
        # string to int
        for i in range(0, self.m):
            if isinstance(self.cum_data[0,i], str):
                self.cum_data[:,i] = list(map(eval, list(self.cum_data[:,i])))
        for i in range(1, self.m):
            self.cum_data[:,i] = self.cum_data[:,i] + self.cum_data[:,i-1]

        self.h_index_list = []
        for i in range(0, self.m):
            self.h_index_list.append(self.cal_h_per_year(self.cum_data[:, i]))

        return self.h_index_list
        
    def cal_h_per_year(self, data_series):
        data_series = np.sort(data_series)
        data_series = data_series[::-1]
        h_index = 0
        for i in range(0, len(data_series)):
            if data_series[i] >= (i+1):
                h_index = i + 1
            else:
                break

        return h_index

    def get_earliest_year(self):
        self.e_year = min(self.year_list[0])
        #print(min(self.year_list[0]))
        self.academic_age = 2020 - self.e_year
        return self.e_year, self.academic_age

    def get_journal_num(self):
        self.journal_num = self.journal_list.drop_duplicates().shape[0]
        
        return self.journal_num

    def get_paper_num(self):
        self.paper_list = []
        for i in range(1969, 2021):
            temp = self.year_list[self.year_list[0]<=i]
            self.paper_list.append(len(temp))
        
        return self.paper_list



def get_all_h(file_path="./data"):
    all_h = pd.DataFrame([])
    for file_name in os.listdir(file_path):
        if file_name.endswith(".csv"):
            author = HIndexCalculator(os.path.join(file_path, file_name))
            temp = pd.DataFrame(author.get_h_index())
            temp = temp.rename({0:file_name}, axis="columns")
            all_h = pd.concat([all_h, temp], axis=1)
    
    all_h.to_csv("./results/h_index_data.csv")
    print("data saved. ")


def get_all_regressors(file_path="./data"):
    all_reg = pd.DataFrame([])
    for file_name in os.listdir(file_path):
        regressors_list = []
        if file_name.endswith(".csv"):
            author = HIndexCalculator(os.path.join(file_path, file_name))
            regressors_list.append(file_name)
            h_index_list = author.get_h_index()
            regressors_list.append(h_index_list[len(h_index_list) - 1])
            e_year, a_age = author.get_earliest_year()
            regressors_list.append(e_year)
            regressors_list.append(a_age)
            regressors_list.append(author.get_journal_num())

            temp = pd.DataFrame(regressors_list).T
            all_reg = pd.concat([all_reg, temp], axis=0)

    all_reg = all_reg.rename({0:"author_name", 1:"h-index", 2:"earliest_year", 3:"academic_age", 4:"jounal_number"}, axis="columns")
    all_reg.index = list(range(0, all_reg.shape[0]))
    all_reg.to_csv("./results/regressors_data.csv")
    print("data saved. ")


def reg_for_single_author(author, name):
    h_index_list = author.get_h_index()
    h_index_list = h_index_list[1:]
    e_year, a_age = author.get_earliest_year()
    paper_num = author.get_paper_num()
    reg_data = pd.DataFrame([])
    count = e_year if e_year>1970 else 1970
    for i in range(0, len(h_index_list)-1):
        if 1970+i >= e_year:
            curr_age = 1970 + i - e_year
            temp = [h_index_list[i+1], h_index_list[i], curr_age, paper_num[i+1]]
            temp = pd.DataFrame(temp).T
            reg_data = pd.concat([reg_data, temp], axis=0)

    reg_data.index = list(range(count, count+reg_data.shape[0]))
    reg_data = reg_data.rename({0:"h_t+1", 1:"h_t", 2:"a_age_t", 3:"paper_num_t"}, axis="columns")
    reg_data.to_csv("./results/reg_data/reg_for_%s.csv"%name)
    print("data saved. %s"%name)


def reg_for_all_author(file_path="./data"):
    for file_name in os.listdir(file_path):
        if file_name.endswith(".csv"):
            author = HIndexCalculator(os.path.join(file_path, file_name))
            reg_for_single_author(author, file_name[:-4])
            

def get_all_e_year(file_path = "./data"):
    temp_df = pd.DataFrame([])
    for file_name in os.listdir(file_path):
        if file_name.endswith(".csv"):
            author = HIndexCalculator(os.path.join(file_path, file_name))
            e_year, a_age = author.get_earliest_year()
            temp = [file_name[:-4], e_year]
            temp = pd.DataFrame(temp).T
            temp_df = pd.concat([temp_df, temp], axis=0)

    temp_df.to_csv("./results/earliest_year.csv")
    print("data saved.")


def get_paper_cite_num(file_path = "./data"):
    temp_df = pd.DataFrame([])
    for file_name in os.listdir(file_path):
        if file_name.endswith(".csv"):
            author = HIndexCalculator(os.path.join(file_path, file_name))
            paper_num = author.get_paper_num()
            paper_num = paper_num[len(paper_num)-1]
            cite_num = author.cite_num

            temp = [file_name[:-4], paper_num, cite_num]
            temp = pd.DataFrame(temp).T
            temp_df = pd.concat([temp_df, temp], axis=0)

    temp_df = temp_df.rename({0:"name", 1:"paper_num", 2:"cite_num"}, axis="columns")
    temp_df.index = range(0, temp_df.shape[0])
    temp_df.to_csv("./results/num_info.csv")
    print("data saved.")


def get_20_year(file_path = "./data"):
    temp_df = pd.DataFrame([])
    for file_name in os.listdir(file_path):
        if file_name.endswith(".csv"):
            author = HIndexCalculator(os.path.join(file_path, file_name))
            e_year, a_age = author.get_earliest_year()
            temp = author.get_h_index()
            start = e_year - 1970 + 1 if e_year >= 1970 else 0
            temp = temp[start:start+20]
            temp.insert(0, file_name)
            temp = pd.DataFrame(temp).T
            temp_df = pd.concat([temp_df, temp], axis=0)
    temp_df.index = range(0, temp_df.shape[0])
    temp_df.to_csv("./results/first_20_year.csv")
    print("data saved.")


def collect_procedure():
    get_all_h()
    get_all_regressors()
    # author = HIndexCalculator("./data/Allen, Gabrielle D..csv")
    # reg_for_single_author(author, "Yang, Lijian")
    reg_for_all_author()
    get_all_e_year()
    get_paper_cite_num()




if __name__ == "__main__":
    collect_procedure()
    # get_20_year()



