import gensim
import jieba
import numpy as np
from pyltp import SentenceSplitter
from config import config


class LDASummarizer():
    def __init__(self):
        # cws_model_path = os.path.join(config['development'].LTP_DATA_DIR, 'cws.model')
        # self.segmentor = Segmentor()
        # self.segmentor.load(cws_model_path)
        self.model = gensim.models.ldamodel.LdaModel.load(config['development'].LDA_PATH)
        self.stopwords = []
        with open(config['development'].STOPWORDS_PATH, 'r') as f:
            for line in f.readlines():
                word = line.split('\n')[0]
                self.stopwords.append(word)
        self.dictionary = gensim.corpora.Dictionary.load_from_text(
            config['development'].DICTIONARY_PATH)
    
    def sent_tokenizer(self, text):
        """将原始文本拆分为句子"""
        sents = SentenceSplitter.split(text)
        return [sent for sent in sents if sent]
    
    def sents2wordlist(self, sents):
        sents = [[w for w in jieba.cut(line) if
                  w not in self.stopwords and w.isprintable() and w not in "‘’“”，、；。？！《》（）//" and
                  w in self.dictionary.values()]
                 for line in sents]
        return sents
    
    def wordlist2vec(self, wordlist):
        vecs = []
        for sent in wordlist:
            bow = self.dictionary.doc2bow(sent)
            vec = self.model.inference([bow])
            vecs.append(vec[0])
        return np.concatenate(vecs)

    def doc2vec(self, wordlist):
        doc = [w for sent in wordlist for w in sent]
        bow = self.dictionary.doc2bow(doc)
        vec = self.model.inference([bow])
        return vec[0]

    
    def summarize(self, text):
        sents = self.sent_tokenizer(text)
        wordlist = self.sents2wordlist(sents)
        sents_vec = self.wordlist2vec(wordlist)
        doc_vec = self.doc2vec(wordlist)
        
        ranks = np.matmul(doc_vec, sents_vec.T)[0]
        ranked_sentences = sorted([(ranks[i], s) for i, s in enumerate(sents)],
                                  reverse=True)
        # self.segmentor.release()
        return ranked_sentences