__author__ = 'yangbin1729'

import os
import numpy as np
import networkx as nx
import jieba
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from pyltp import SentenceSplitter, Segmentor
from config import config


class TextRankSummarizer():
    def __init__(self):
        # cws_model_path = os.path.join(config['development'].LTP_DATA_DIR, 'cws.model')
        # self.segmentor = Segmentor()
        # self.segmentor.load(cws_model_path)
        self.model = Word2Vec.load(config['development'].Word2Vec_DIR)
    
    def sent_tokenizer(self, text):
        """将原始文本拆分为句子"""
        sents = SentenceSplitter.split(text)
        return [sent for sent in sents if sent]
    
    def sent_vectorize(self, sent):
        """词向量相加，生成句子向量"""
        
        # wordlist = segmentor.segment(sent)
        wordlist = jieba.cut(sent)
        word_vectors = [self.model.wv[w] for w in wordlist if w in self.model.wv]
        return np.mean(word_vectors, axis=0)
    
    def similarity_matrix(self, sents):
        """生成相似度矩阵"""
        
        sent_vectors = np.array(
            [self.sent_vectorize(sent) for sent in sents if sent])
        M = cosine_similarity(sent_vectors)
        return M
    
    def summarize(self, text, n=3):
        """获得 TextRank 值最大的 n 句话"""
        self.text = text
        sents = self.sent_tokenizer(self.text)
        M = self.similarity_matrix(sents)
        graph = nx.from_numpy_array(M)
        ranks = nx.pagerank(graph)
        ranked_sentences = sorted([(ranks[i], s) for i, s in enumerate(sents)],
                                  reverse=True)
        # self.segmentor.release()
        return ranked_sentences


# todo：生成式摘要

if __name__ == '__main__':
    text = """写在《孤军》之前：（这一段好像没贴过）
        这些年我一直总是在看各地民国史资料，特别钟爱的是口述，口述中尤其喜欢看平民的口述史。
        平民的口述极为真切朴实，更易感同身受。
        某一天，我看到一个女子的回忆，东北沦陷期间，还算殷实的家被折腾得家破人亡，她成了孤儿四处流浪。
        事情起因，是她哥读书留在关内，传闻当了八路，这成为宪兵队军警等等的把柄，各色人等轮番登场，监视敲诈了一轮又一轮，家产赔光之后，一个特务借口将她父亲抓了，打得奄奄一息才接出来，接出来就死了，母亲随后也死了，只剩她一人逃亡。
        她的哥哥最终有没有当八路不知道，有没有兄妹团圆也不知道，这切骨之恨，即便在老了之后仍然留在她心里。
        不仅仅是她，整个东北沦陷地区，翻看地方文史，惨案累累，罄竹难书，宪兵军警特务肆意妄为，被抓捕的无辜者比比皆是，要不就当马路大送达731，要不就送到矿山森林，要不就投入监牢……
        除了无辜者，抓捕抗日分子，包括国民党和共产党的行动也屡屡发生，各地的大抓捕之后，是无数青年的鲜血和生命，也是无数家庭的家破人亡。
        然而，时至今日，还有人借着几张漂亮的宣传照宣传伪满洲国的丰功伟绩，真是不可思议。
        愤怒和痛惜，无法全然表达我此际心情，我决心为他们做点什么，于是有了这本书，这个剧。
        我要记载这段历史，同时也用跟平民口述同样真切朴实的方式，告诉后人事实，同时警示更后来者。"""
    print(TextRankSummarizer().summarize(text, n=3))