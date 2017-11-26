#This code reads changes_python.log and performs analytics on it
#Author: Izabela Tyrna 10358601

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

class Get_Data(object):
    
    def read_file(self,changes_file):
        # use strip to strip out spaces and trim the line.
        data = [line.strip() for line in open(changes_file, 'r')]
        return data
        
    def get_commits(self,data):
        sep = 72*'-'
        #new_sep = "Changed paths:"
        commits = []
        #current_commit = None
        index = 0
        while index < len(data):
            try:
                #get counts of add, modify, delete actions
                action_index = index + 3
                count_a = 0
                count_d = 0
                count_m = 0
                check_point = 1
                while check_point != 0:
                    value = data[action_index][0]
                    if value == "A":
                        count_a = count_a + 1
                    elif value == "D":
                        count_d = count_d + 1
                    elif value == "M":
                        count_m = count_m + 1
                    action_index = action_index + 1   
                    find_space = data[action_index]
                    check_point = len(find_space)
                    
                # parse lines that start with the folloing format: r1551925
                details = data[index + 1].split('|')
                # the author with spaces at end removed.
                commit = {'revision': details[0].strip(),
                    'author': details[1].strip(),
                    'date': details[2].strip(),
                    'number_of_lines': details[3].strip().split(' ')[0],
                    'add': count_a,
                    'modify': count_m,
                    'delete': count_d
                }
                commits.append(commit)
                index = data.index(sep, index + 1)
            except IndexError:
                break
            
        dframe = pd.DataFrame(data = commits)
        return dframe
    
    #function to extract dates from commit['date']
    def get_dates(self,dates):
        plus_index = "+"
        date_list = []
        for i in range(len(dates)):
            index = dates[i].index(plus_index)
            #print index #to see what I am getting here
            clean_date = dates[i][0:index-10] # as index is 20 extracting first 10 characters
            date_list.append(clean_date) #creating a list pf clean dates
        return date_list
    
if __name__ == '__main__':
    # open the file - and read all of the lines.
    call_object  = Get_Data()
    changes_file = 'changes_python.log'
    data = call_object .read_file(changes_file)
    commits = call_object .get_commits(data)
    
    ##DESCRIPTIVE STATISTICS
    commits['add'] = commits['add'].astype(int)
    commits['modify'] = commits['modify'].astype(int)
    commits['delete'] = commits['delete'].astype(int)
    commits['number_of_lines'] = commits['number_of_lines'].astype(int)
    descriptive = commits.describe()
    print descriptive
             
    ##GETTING MIN AND MAX DATES TO SEE WHEN THE LOGS HAPPEND
    dates_cleanup = call_object .get_dates(commits['date'])
    #print dates_cleanup #to see what I am getting here
    unique_dates = pd.unique(dates_cleanup)
    #print unique_dates #to see what I am getting here
    unique_dates.sort()
    print 'The file log was created between ' + str(unique_dates[0]) + ' and ' + unique_dates[len(unique_dates)-1]
    
    ## GETTING COUNT OF UNIQUE NAMES IN THE FILE
    unique_names = pd.unique(commits['author'])  #get unique names from commits['author']
    list_unique_names = unique_names.tolist() #converting unique_names to a list
    print 'These are the unique users in the log file: ' + str(unique_names)
    print
    list_of_authors = commits['author']
    proper_list_of_authros = list_of_authors.tolist() #converting that vairbale to a list
    print 'The below presents the list of unique names and their count in the file:'
    counts = Counter(list_of_authors) #calling counter function to to check how many times users appear in the file
    print counts
    print

    ##BAR CHART
    letter_counts = Counter(list_of_authors)
    df = pd.DataFrame.from_dict(letter_counts, orient='index')
    ax = df.plot(kind='bar', title = 'Users by amount of logs in the file', legend = False,
            figsize=(10,5))
    ax.set_xlabel('Users',fontsize=12)
    ax.set_ylabel('Frequency',fontsize=12)

      
    ##PIE CHART
    add = sum(commits['add'])
    modify = sum(commits['modify'])
    deletec = sum(commits['delete'])
    labels = ['Add','Modify','Delete']
    values = [add,modify,deletec]
    colors = ['yellowgreen', 'gold', 'lightskyblue']
    explode = (0, 0.1, 0) # explode 2nd slice
    plt.figure(figsize=(10,5))
    bx = plt.pie(values, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Frequency of Action Types')
    plt.axis('equal')
    plt.show()
    
   
    ##BAR CHART - Add Action by User
    dfchart=pd.DataFrame({'xvalues': commits["author"], 'yvalues': commits['add']})
    # plot
    plt.bar( 'xvalues', 'yvalues' , data=dfchart)
    plt.xticks(rotation='vertical')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    plt.title('Add Action by User')
    plt.show()
    
    ##BAR CHART - Modify Action by User
    dfchart=pd.DataFrame({'xvalues': commits["author"], 'yvalues': commits['modify']})
    # plot
    plt.bar( 'xvalues', 'yvalues' , data=dfchart)
    plt.xticks(rotation='vertical')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    plt.title('Modify Action by User')
    plt.show()
    
    ##BAR CHART - Delete Action by User
    dfchart=pd.DataFrame({'xvalues': commits["author"], 'yvalues': commits['delete']})
    # plot
    plt.bar( 'xvalues', 'yvalues' , data=dfchart)
    plt.xticks(rotation='vertical')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    plt.title('Delete Action by User')
    plt.show()
      
