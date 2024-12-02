import math
import pandas as pd

import pickle

import time    
import functools   
import random
from collections import Counter, OrderedDict

#------------------------------------------------------------------------------

def timer(func):
    """
    The `timer` function is a decorator in Python that measures and prints the runtime of the decorated
    function.
    
    :param func: The `func` parameter in the `timer` function is a function that will be timed when it
    is called. The `timer` function is a decorator that calculates and prints the runtime of the
    decorated function (`func`)
    :return: The `wrapper_timer` function is being returned from the `timer` decorator function.
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(" ====> Duration {:.2f} secs: {}".format(run_time, func.__doc__))
        return value

    return wrapper_timer #  no "()" here, we need the object to be returned.

#------------------------------------------------------------------------------
# predicates
def isElFilled(el, liste):
    """
    The function `isElFilled` checks if a specified element is present in a list and is not None, while
    the lambda function `validateIndex` checks for row duplicates in a pandas DataFrame.
    
    :param el: The `el` parameter in the `isElFilled` function represents the element that you want to
    check for in the `liste` parameter. It checks if the element is present in the list and if its value
    is not `None`
    :param liste: It seems like there is a missing value for the `liste` parameter in your code snippet.
    Could you please provide the necessary information or context for the `liste` variable so that I can
    assist you further?
    :return: The `isElFilled` function checks if a specific element `el` is present in the `liste` and
    if it is not `None`. It returns `True` if the element is present and not `None`, otherwise it
    returns `False`.
    """
    return ((el in liste) and (liste[el] is not None))

# Are there NO row duplicates?      #Types: pandas dataframe --> Boolean
validateIndex = lambda d: False if True in d.duplicated(keep="first") else False

#------------------------------------------------------------------------------
# Serialisierung    
@timer 
def pickle_out(objName, dateiName):
    """
    The function `pickle_out` serializes an object and saves it to a file using the pickle module in
    Python.
    
    :param objName: The `objName` parameter in the `pickle_out` function is the object that you want to
    serialize and save to a file using the `pickle` module in Python. This object can be any Python
    object such as a dictionary, list, class instance, etc
    :param dateiName: The `dateiName` parameter in the `pickle_out` function is the name of the file
    where the object will be serialized and saved using the `pickle` module in Python. This parameter
    specifies the file path where the serialized object will be stored
    """
    with open(dateiName, "wb") as p_out:
        pickle.dump(objName, p_out)

@timer 
def pickle_in(dateiName):
    """
    The function `pickle_in` deserializes data from a file using the `pickle` module in Python.
    
    :param dateiName: The `dateiName` parameter in the `pickle_in` function is a string that represents
    the name of the file from which you want to deserialize (load) data using the `pickle` module in
    Python
    :return: The function `pickle_in` is returning the deserialized object loaded from the file
    specified by the `dateiName` parameter using the `pickle.load` method.
    """
    with open(dateiName, "rb") as p_in:
        return pickle.load(p_in)

#------------------------------------------------------------------------------

def col_base_features(col, pattern):
    """
    The function `col_base_features` splits a column based on a specified pattern and returns the first
    element of each split.
    
    :param col: The `col` parameter is typically a pandas Series object representing a column in a
    DataFrame. It seems like the function `col_base_features` is designed to split the values in this
    column based on a specified pattern and return the first part of each split value
    :param pattern: The `pattern` parameter is a string that represents the pattern you want to split
    the values in the `col` column by. This pattern will be used to split the values in the column `col`
    into multiple parts
    :return: The function `col_base_features` takes a column `col` and a `pattern` as input, splits the
    values in the column based on the pattern, and returns a list of the first element from each split
    value.
    """
    a = list(col.str.split(pat = pattern))
    return list([x[0] for x in a])
#    c = dict(zip(effect_analysis_table["ID"], b))
    
def determine_dyn_colorder(colvals, colorder_fixedpart, pdict):
    """
    This Python function removes specific elements from a list of column values and returns a new column
    order.
    
    :param colvals: It seems like you were about to provide the `colvals` parameter for the
    `determine_dyn_colorder` function, but it is missing from your message. Could you please provide the
    `colvals` parameter so that I can assist you further with the function?
    :param colorder_fixedpart: The function `determine_dyn_colorder` takes three parameters:
    :param pdict: It seems like you were about to provide the details of the `pdict` parameter, but it
    is missing in the provided code snippet. Could you please provide the details of the `pdict`
    parameter so that I can assist you further with the `determine_dyn_colorder` function?
    :return: The function `determine_dyn_colorder` returns a list that is a combination of the
    `colorder_fixedpart` list and the `col_order` list after removing specific elements specified in the
    `remList`.
    """
    col_order = list(colvals)
    remList = ["Index", "ID", pdict["meta_typ"], pdict["meta_description"],"Wertebereich", "F_Aktiv", "F_PCA", "F_Szen"]
    for i in remList:
        try:
            col_order.remove(i)
        except:
            print(i + " nicht vorhanden")
    
    
    # col_order.remove("Index") 
    # col_order.remove("ID")     
    # col_order.remove(pdict["meta_typ"])    
    # col_order.remove(pdict["meta_description"])
    # col_order.remove("Wertebereich")
    # col_order.remove("F_Aktiv")     
    # col_order.remove("F_PCA")     
    # col_order.remove("F_Szen")  
    
    return colorder_fixedpart + col_order


lam_split = lambda x:  x.split("$")[1] 

tupToStr = lambda t: ". ".join(str(e) for e in [int(t[0]), t[1]]) 
 
# dfcn: DataFrame Col Name; zeichen: char der weg soll
#colNameRemChar = lambda x, y: x.str.replace(ch,'') for ch in list(y)

def cleanse_colnames(dfcn, zeichen):
    """
    The function `cleanse_colnames` removes specified characters from column names in a DataFrame.
    
    :param dfcn: The `dfcn` parameter in the `cleanse_colnames` function represents the column names of
    a DataFrame. It is expected to be a list of strings where each string is a column name
    :param zeichen: The parameter `zeichen` in the `cleanse_colnames` function is expected to be a
    string or a list of characters that you want to remove from the column names in a DataFrame. The
    function will iterate over each character in the `zeichen` string or list and remove it from the
    :return: The function `cleanse_colnames` returns the input `dfcn` after removing any characters
    specified in the `zeichen` parameter from each element in `dfcn`.
    """
    #dfcn ist kein Dataframe, sondern df.columns
    for v in list(zeichen):
        dfcn = dfcn.str.replace(v,'')
    return dfcn

ohlist_To_FeaturesList = lambda l: list(set([i.split("$")[0] for i in l]))
sortDictReverseOrderIntKey = \
    lambda d: sorted(list(d.items()),key=lambda x:x[0],reverse=True)

# -----------------------------------------------------------------------------
# prüfen ob "nan", "None" in liste, dictionary weg kann:
#x: list
remNanFromListFloat = lambda x: [i for i in x if str(i) != "nan"]
remNullItemsFromList = lambda x: [i for i in x if i is not None] 
#d: dictionary
remNanFromDict = lambda d: {k: v for k, v in d.items() if str(v) != "nan"}
remNullItemsFromDict = lambda d: {k: v for k, v in d.items() if v is not None}

# -----------------------------------------------------------------------------
# Math: Sets
intersect = lambda x,y: list(set(x).intersection(y)) 

#------------------------------------------------------------------------------
# Math: Combinatorics
binom = lambda n,k: math.factorial(n) // math.factorial(k) // math.factorial(n - k)

#------------------------------------------------------------------------------
# Random generator for colors
getRandomColor = lambda _: "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

#------------------------------------------------------------------------------
# FreqCounter
def countFreqs(arr):
    """
    The function `countFreqs` takes in a list of elements and returns a sorted dictionary with the
    frequency of each element in the list.
    
    :param arr: The `countFreqs` function takes a list `arr` as input and returns an ordered dictionary
    containing the frequency of each element in the input list. The function uses the `Counter` class
    from the `collections` module to count the occurrences of each element in the list and then sorts
    the dictionary
    :return: The function `countFreqs` is returning an `OrderedDict` containing the frequencies of each
    element in the input array `arr`, sorted in ascending order based on the elements.
    """
    lcounter = Counter(arr)
    return OrderedDict(sorted(lcounter.items()))



#------------------------------------------------------------------------------
#Dataframe nach Reihen sortieren, neues mit neuem Index erzeugen - BEGIN
def popRowFromDF(dframe, indexVal):    
    """
    The function `popRowFromDF` takes a DataFrame and an index value, pops the corresponding row from
    the DataFrame, and returns the popped row as a list along with the DataFrame without that row.
    
    :param dframe: The `dframe` parameter is typically a pandas DataFrame, which is a two-dimensional
    size-mutable, potentially heterogeneous tabular data structure with labeled axes (rows and columns)
    :param indexVal: The `indexVal` parameter in the `popRowFromDF` function is the index value of the
    row that you want to remove from the DataFrame (`dframe`). This function will return the row that
    was removed as a list (`poppedRow`) and the DataFrame with that row removed (`Sh
    :return: The function `popRowFromDF` returns two values: `poppedRow`, which is a list containing the
    values of the row at index `indexVal` in the DataFrame `dframe`, and `ShrinkedDF`, which is the
    DataFrame `dframe` with the row at index `indexVal` removed.
    """
    poppedRow = dframe.loc[indexVal, :].tolist()    
    ShrinkedDF = dframe.drop(indexVal)
    return poppedRow, ShrinkedDF

@timer    
def sortDF(dframe,col,asc):         #Pandas-df, String, Boolean
    """
    The `sortDF` function sorts a DataFrame based on a specified column in ascending or descending
    order.
    
    :param dframe: The `dframe` parameter is a Pandas DataFrame that you want to sort based on a
    specific column
    :param col: The `col` parameter in the `sortDF` function is a string that represents the column in
    the DataFrame by which you want to sort the data. This column will be used to determine the order in
    which the rows of the DataFrame will be sorted
    :param asc: The `asc` parameter in the `sortDF` function is a boolean value that determines whether
    the sorting should be done in ascending order (`True`) or descending order (`False`). If `asc` is
    `True`, the DataFrame will be sorted in ascending order based on the specified column. If `
    :return: The function `sortDF` returns a sorted DataFrame based on the specified column and sorting
    order (ascending or descending).
    """

    dfColList = dframe.columns.values
    retDF = pd.DataFrame(columns=dfColList)
    while not dframe.empty:
    #for i in range(4):      

        dfCol = dframe[col]     

        poppedStackdfCol = min(dfCol) if asc == True else max(dfCol)
        poppedStackIndexVal = dframe \
            .index[dframe[col] == poppedStackdfCol] \
            .tolist()

        #falls höchster/niedrigster Rang mehrfach vorliegt, wird der erste in Liste genommen 
        #if highest/lowest rank occurs multiple times, the first one is included in the list
        poppedRow, dframe = popRowFromDF(dframe, poppedStackIndexVal[0])        
        dict_row = dict(zip(dfColList, poppedRow))
#        retDF = pd.concat([retDF, dict_row], axis = 1, ignore_index = True)
        
        # retDF = retDF \
        #     .append(dict_row, ignore_index = True)
            
        retDF = pd.concat([retDF, pd.DataFrame([dict_row])], ignore_index=True)

    return retDF

# END
#------------------------------------------------------------------------------
# Dataframes: Column name aliases (compare SQL "as")

#x: dframe, y: pdict
df_cols_assign_alias = \
    lambda x,y: x.rename(columns=dict(zip(y["scenario"], y["sc_alias"]))) 




