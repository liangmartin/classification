# -*- coding:UTF-8 -*-
import csv
import re
import jieba

#0,作为四川人 来这家新开的店已经6次了...我就真搞不懂有些人是不是眼红人家店生意好 
#说人家一个肉3、4个签子？你可能还不会数数。不好意思 
#我真是使出浑身解数也没在整个店找到4个签子的 最多签子3签就两个品类 
#因为肉部分好 当然要卖贵 其余的肉都是一两个签子 大家可以看图 脆骨 郡肝 牛肉 五花肉 
#鱿鱼 牛板筋凳都是一个签子 香菜牛肉酸菜牛肉之类的两个签子。这家店为是从南方吃到北方 
#原来在芝罘区有一家 太远了 现在开了一家到大学城 终于可以好好吃了。
#下面重复我之前的做油碟方法：南方人吃火锅串串必备油碟！来说一说如何配制，非常简单！
#建议自己动手：蚝油1/5勺、蒜泥少量、小米椒少量！（小米椒一定要少量！不然巨辣！）
#香油半袋！然后可以适量加醋（个人喜酸 一般加一勺）然后放入一些芝麻、香菜适量！
#油碟制作完成！这次来还赠送了蛋炒饭 惊喜 之前刚刚开业的时候还没有 
#对于我这个吃火锅必点饭的南方人再好不过了 对于价格 全国都一样 对于学生来说确实稍贵 
#不过呢 就和吃火锅一样 偶尔吃吃还是可以 味道赞就行了～ #麻辣小郡肝# #麻辣牛肉# 
#油碟# #番茄鸳鸯锅# #麻辣脆骨# #自己盛的番茄汤#

path_meituan = './meituan_test.csv'
path_class = './class_.csv' # 类别
path_stop = './stopWords_3.txt' # 停用词


path_neg = './neg_test.txt'
path_posi = './posi_test.txt'

def get_class():
    class_ = []
    with open(path_class,'r',encoding='utf-8',errors='ignore',newline='')as f:
        reader = csv.reader(f)
        for line in reader:
            temp = line[0].replace('\n', '').strip()
            class_.append(int(temp))
    return class_


# 获取数据--文本评论
def getData(path): # 获取数据
    seg_all = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader:
            seg_all.append(line[1]) # csv第一列是index，第二列是文本评论
    return seg_all

def get_index(x): # 获得待删除的Index
    temp = [i for i,v in enumerate(x) if v=='']
    return temp

#根据index删除元素 --- 主要针对coment来讲
def delete_comments_accord_index(x, index): # 针对comments删除元素
    to_be_delete = [v for i,v in enumerate(x) if i in index]
    for i in to_be_delete:
        x.remove(i)
    return x

#根据index删除元素，对class来讲
#class中的元素只有1，-1处理方式和comment不一样
def delete_class_accord_index(class_, index): # 针对class删除元素
    temp = []
    for i,v in enumerate(class_):
        if i not in index:
            temp.append(v)
    return temp

#去除其他符号
def splitOther(data_split):
    """
    params：
    data_split:待切分的数据
    return:
    返回：是空元素的index + 待被去除index的文本---以元组的形式返回
    """
    def re_split(desstr):
        temp = ''.join(re.split(r'\W',desstr))
        return temp
    
    temp = [re_split(desstr) for desstr in data_split]
    #获取待删除的index
    index = get_index(temp)
    return (index,temp)


#由index删除列表元素
def indexProcess(func, last_comments, last_class): 
    """
    params:
    func:清洗数据的某个函数
    last_comments:待处理的文本评论列表
    last_class:待处理的文本类别
    return:
    返回已经去除了相应元素的文本列表 + 对应的class
    """

    noFunc_index = func(last_comments)[0]
    noFunc_comments = func(last_comments)[1]
    comments_noFunc = delete_comments_accord_index(noFunc_comments, noFunc_index)
    class_noFunc = delete_comments_accord_index(last_class, noFunc_index)
    return (comments_noFunc, class_noFunc)

def splitStop(data_split): #创建停用词列表
    #从txt文档中读取停用词，放进列表中
    def stopwordslist():
        #返回列表
        with open(path_stop,'r',encoding='utf-8', errors='ignore')as f:
            stopwords = [line.strip() for line in f.readlines()]
        return stopwords


    stop_words_list = stopwordslist()
    stopwords = {}.fromkeys(stop_words_list)
    # 建立一个函数去掉字符串中的停用词
    def cutStopWords(word):
        segs = jieba.cut(word, cut_all=False)
        final = ''
        for seg in segs:
            if seg not in stopwords:
                final += seg
                final += ' '
        return final
    splitStopData = [cutStopWords(v) for v in data_split]
    index = [i for i,v in enumerate(splitStopData) if v=='']
    return (index, splitStopData)

#自己检查使用，看是否将文本与标签相对应
def wirteClass(path_neg, path_posi, comments,class_): #根据类别写文档
    file_neg = open(path_neg, 'w', encoding = 'utf-8',errors='ignore')
    file_posi = open(path_posi, 'w', encoding = 'utf-8', errors = 'ignore')
    for i,v in enumerate(noStopWord_comments):
        # 使用try...except 来检测读写过程中的错误---方便之后在这里修改
        try:
            if noStopWord_class[i] == -1:
                file_neg.write(v+'\n')
            else:
                file_posi.write(v+'\n')
        except:
            # TODO: 可以再详细一些，给出提示，看是哪些具体的错误
            print('Error')
    file_neg.close()
    file_posi.close()
class_ = get_class() # 获取类别 
comments = getData(path_meituan) # 获取评论


# 充当过滤链
#-----------------------------------------------------------
noOtherWord_comments,noOtherWord_class= indexProcess(splitOther, comments,class_) # 根据index处理comments和class
noStopWord_comments,noStopWord_class=indexProcess(splitStop, noOtherWord_comments, noOtherWord_class)
#-----------------------------------------------------------
wirteClass(path_neg, path_posi, noStopWord_comments, noStopWord_class)