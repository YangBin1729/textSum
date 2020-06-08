__author__ = 'yangbin1729'

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '123@456#789$012%'


class DevelopmentConfig(Config):
    DEBUG = True
    MODEL_DIR = os.path.join(basedir, 'saved')
    Word2Vec_DIR = os.path.join(MODEL_DIR,
                                'word2vec/wiki_corpus_above200.model')
    LTP_DATA_DIR = os.path.join(MODEL_DIR, 'ltp_data_v3.4.0')
    # CLASSIFIER_DIR = os.path.join(MODEL_DIR, 'classifier')
    # TOKENIZER = os.path.join(CLASSIFIER_DIR, 'tokenizer.pickle')
    
    # DATA_DIR = os.path.join(basedir, 'datasets')
    # corpus_path = os.path.join(DATA_DIR, 'qa_corpus.csv')
    # stopwords_path = os.path.join(DATA_DIR, 'stopword.txt')
    
    LDA_PATH = os.path.join(MODEL_DIR, 'lda/lda.model')
    STOPWORDS_PATH = os.path.join(MODEL_DIR, "chinese_stopwords.txt")
    DICTIONARY_PATH = os.path.join(MODEL_DIR, 'lda/dictionary')
    
    DEFAULT_SUMMARIZED = """
    里皮已经回到了欧洲，但他仍有一肚子话想说。
    在接受天空体育采访时，里皮表示——自己选择辞去国足主帅是因为继续合作的条件没有了。
    “我在中国度过了将近8年的时间，那是一段快乐的时光。带领国家队重要的不是赢得比赛，而是发展运动，我帮助了中国足球发展。”
    “之所以选择辞职是因为继续合作的条件没有了。当我相信不再有热情、欲望和信任这些继续合作的自然条件时，我不喜欢赚太多自己不应得的钱。”
    关于未来的计划，里皮表示：“我没有重返俱乐部教练席的渴望，我认为自己永远不会再执教俱乐部了。”
    """


class ProductionConfig(Config):
    DEBUG = False
    # MODEL_DIR = r'/home/student/project/project-01/noam/project01/models'
    # Word2Vec_DIR = os.path.join(MODEL_DIR,
    #                             'word2vec/wiki_corpus_above200.model')
    # LTP_DATA_DIR = os.path.join(MODEL_DIR, 'ltp')
    # CLASSIFIER_DIR = r'/home/student/project/project-01/noam/project01' \
    #                  r'/classifiers'
    # TOKENIZER = os.path.join(MODEL_DIR, 'classifier/tokenizer.pickle')
    #
    # DATA_DIR = os.path.join(basedir, 'datasets')
    # corpus_path = os.path.join(DATA_DIR, 'qa_corpus.csv')
    # stopwords_path = os.path.join(DATA_DIR, 'stopword.txt')


config = {'development': DevelopmentConfig, 'production': ProductionConfig, }