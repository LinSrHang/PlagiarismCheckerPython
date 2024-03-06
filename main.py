from jieba import lcut
from re import match
from sys import argv
from gensim.corpora import Dictionary
from gensim.similarities import Similarity

# 通过该方法实现计算fileStr1和fileStr2的余弦相似度
def calculateSimilarity(fileStr1, fileStr2):
    texts = [fileStr1, fileStr2]
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    testCorpus = dictionary.doc2bow(fileStr1)
    cosineSimilarity = similarity[testCorpus][1]
    return cosineSimilarity

# 从filePath中读取内容
def getFileContents(filePath):
    ret = ''
    with open(filePath, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            ret += line
            line = f.readline()
    return ret

# 使用jieba库进行分词并正则
def processFile(fileStr):
    fileStr = lcut(fileStr)
    res = []
    for tags in fileStr:
        # 正则，只保留a-z，A-Z，0-9，\u4e00-\u9fa5，其中\u4e00-\u9fa5为中文utf-8编码范围
        if (match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags)):
            res.append(tags)
    return res

# 主函数入口
if __name__ == '__main__':
    # 如果命令行参数数量不为3，报错
    if len(argv) != 4:
        raise ValueError('Please provide orig.txt orig_add.txt ans.txt')
    
    orig, orig_add, ans = argv[1], argv[2], argv[3]
    print (orig, orig_add, ans)
    similarity = calculateSimilarity(processFile(getFileContents(orig)), processFile(getFileContents(orig_add)))
    print("文章相似度：%.2f"%(similarity))
    with open(ans, 'w', encoding='utf-8') as f:
        f.write("文章相似度：%.2f"%(similarity))