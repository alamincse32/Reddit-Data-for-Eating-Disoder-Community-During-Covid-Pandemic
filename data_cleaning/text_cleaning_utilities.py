import re
import nltk
import gensim
from gensim.utils import simple_preprocess
from nltk.tokenize import word_tokenize as wt
from nltk.corpus import stopwords
import spacy
from gensim.models import TfidfModel
from gensim import corpora

# prepare stopwords
nltk.download('stopwords')
sw = stopwords.words('english')
STOP_WORDS = sw
STOP_WORDS.extend([',', '`', "'m", "i'm", "'s", "'ve", "n't",'know','make','want','say','think','need','tell','go','thing','get','help','really','try','even','time','also','ask','find','take','talk','lot','give','way','see','sure','much','look','good','one','maybe'])


def get_lemmatized_sentence(text, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
    tokens = []
    nlp = spacy.load('en_core_web_md', disable=['parser', 'ner'])
    for sent in text:
        doc = nlp(sent)
        next_text = []
        for token in doc:
            if token.pos_ in allowed_postags:
                next_text.append(token.lemma_)
        final = " ".join(next_text)
        tokens.append(final)
    return tokens


def build_bigram_trigram_models(sentence, min_count=5, threshold=50):
    bigram = gensim.models.Phrases(sentence, min_count=min_count, threshold=threshold)
    trigram = gensim.models.Phrases(bigram[sentence], threshold=threshold)
    bigram_models = gensim.models.phrases.Phraser(bigram)
    trigram_models = gensim.models.phrases.Phraser(trigram)

    return [bigram_models, trigram_models]


def get_bigram_trigram_words(texts, models):
    bigram_trigram_tokens = []
    for text in texts:
        tokens = models[1][models[0][text]]
        bigram_trigram_tokens.append(tokens)
    return bigram_trigram_tokens


def get_bigram_words(texts, model):
    bigram_tokens = []
    for text in texts:
        tokens = model[text]
        bigram_tokens.append(tokens)
    return bigram_tokens


def get_clean_tokens(texts):
    final_token = []
    for text in texts:
        tokens = simple_preprocess(text, deacc=True)
        tokens = [token for token in tokens if token not in STOP_WORDS]
        final_token.extend(tokens)
    return final_token


def split_sentences(special_character_removed):
    nltk.download('punkt')
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_tokenize = []
    for text in special_character_removed:
        a = split_into_sentences(sent_tokenizer, text.lower())
        sentence_tokenize.extend(a)
    return sentence_tokenize


def split_into_sentences(sent_tokenizer, text):
    return sent_tokenizer.tokenize(text)


def removed_frequent_words(texts):
    id2words = corpora.Dictionary(texts)
    corpus = [id2words.doc2bow(text) for text in texts]

    # tf_idf = TfidfModel(corpus, id2word=id2words)
    # low_value = 0.03
    # words = []
    # words_missing_in_tfidf = []
    # for i in range(len(corpus)):
    #     bow = corpus[i]
    #     tfidf_ids = [id for id, value in tf_idf[bow]]
    #     bow_ids = [id for id, value in bow]
    #     low_value_words = [id for id, value in tf_idf[bow] if value < low_value]
    #     drops = low_value_words + words_missing_in_tfidf
    #     for item in drops:
    #         words.append(id2words[item])
    #     words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids]
    #
    #     new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]
    #     corpus[i] = new_bow
    return [corpus,id2words]


# Remove emojis from text data
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_special_characters(text):
    # Newlines (replaced with space to preserve cases like word1\nword2)
    text = re.sub(r'\n+', ' ', text)
    # Remove resulting ' '
    text = text.strip()
    text = re.sub(r'\s\s+', ' ', text)

    # emails
    text = re.sub('\S*@\S*\s?', '', text)

    # > Quotes
    text = re.sub(r'\"?\\?&?gt;?', '', text)

    # Bullet points/asterisk (bold/italic)
    text = re.sub(r'\*', '', text)
    text = re.sub('&amp;#x200B;', '', text)

    # remove the [removed] from text
    text = text.replace('[removed]', '')

    # remove the [deleted] from text
    text = text.replace('[deleted]', '')

    # things in parantheses or brackets
    text = re.sub(r'[\[.*?\]\(.*?\)]', '', text)

    # remove URLS
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text)

    # Strikethrough
    text = re.sub('~', '', text)

    # Exclamation mark remove
    text = re.sub('!', '', text)

    # Spoiler, which is used with < less-than (Preserves the text)
    text = re.sub('&lt;', '', text)
    text = re.sub(r'!(.*?)!', r'\1', text)

    # Code, inline and block
    text = re.sub('`', '', text)

    # Superscript (Preserves the text)
    text = re.sub(r'\^\((.*?)\)', r'\1', text)

    # Table
    text = re.sub(r'\|', ' ', text)
    text = re.sub(':-', '', text)

    # Heading
    text = re.sub('#', '', text)

    return text
