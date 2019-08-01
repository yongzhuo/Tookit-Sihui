# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/7/31 21:21
# @author   :Mo
# @function :


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def tfidf_from_ngram(questions):
    """
        使用TfidfVectorizer计算n-gram
    :param questions:list, like ['孩子气', '大漠帝国'] 
    :return: 
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    import jieba
    def jieba_cut(x):
        x = list(jieba.cut(x))
        return ' '.join(x)
    questions = [jieba_cut(''.join(ques)) for ques in questions]
    tfidf_model = TfidfVectorizer(ngram_range=(1, 2), # n-gram特征, 默认(1,1)
                                  max_features=10000,
                                  token_pattern=r"(?u)\b\w+\b", # 过滤停用词
                                  min_df=1,
                                  max_df=0.9,
                                  use_idf=1,
                                  smooth_idf=1,
                                  sublinear_tf=1)
    tfidf_model.fit(questions)
    print(tfidf_model.transform(['紫色 ANGEL 是 虾米 回事']))
    return tfidf_model


if __name__ == "__main__":
    # test 1
    corpora_documents = [['大漠', '帝国'], ['紫色', 'Angle'], ['花落', '惊', '飞羽'],
                         ['我', 'm', 'o'], ['你', 'the', 'a', 'it', 'this'], ['大漠', '大漠']]
    corpora_documents = [''.join(ques) for ques in corpora_documents]
    # 统计词频
    vectorizer = CountVectorizer()
    # 初始化,fit和transformer   tf-idf
    transformer = TfidfTransformer()
    # 第一个fit_transform是计算tf-idf, 第二个是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpora_documents))
    print(tfidf)
    # 模型所有词语
    word = vectorizer.get_feature_names()
    print(word)
    weight = tfidf.toarray()
    print(weight)


    # test 2 from file of text
    tf_idf_model = tfidf_from_ngram(corpora_documents)
    print(tf_idf_model.transform(['你 谁 呀, 小老弟']))


    #  sklearn的tfidf模型,可以采用TfidfVectorizer,提取n-gram特征,直接用于特征计算
    #  和gensim一样, 都有TfidfVectorizer, 继承的是CountVectorizer
    #             df += int(self.smooth_idf)        # 平滑处理
    #             n_samples += int(self.smooth_idf) # 平滑处理
    #             idf = np.log(n_samples / df) + 1  # 加了个1