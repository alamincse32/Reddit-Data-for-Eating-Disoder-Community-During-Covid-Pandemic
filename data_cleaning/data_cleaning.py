import math
import gensim
from gensim.models import ldamodel, LdaModel
import text_cleaning_utilities
from gensim.models.coherencemodel import CoherenceModel
import os
import pandas as pd


def read_post_comment(file_name):
    try:
        df = pd.read_csv(file_name)
        return df
    except Exception as err:
        print(err)


def get_post_and_comment_text(ps_comnt):
    post_and_comment_text = []
    user_ids = []
    number_of_rows = ps_comnt.shape[0]
    print(number_of_rows)
    try:
        for row in range(number_of_rows):
            local_post_and_comment_text = []
            local_user_ids = []
            row_length = len(ps_comnt.iloc[row].dropna())
            post_user_id = ps_comnt.iloc[row][1]
            if not pd.isna(post_user_id):
                local_user_ids.append(post_user_id)
            post_title_text = ps_comnt.iloc[row][2]
            post_body_text = ps_comnt.iloc[row][3]
            post_whole_text = ""
            if not pd.isna(post_title_text):
                post_whole_text = post_title_text + " "

            if not pd.isna(post_body_text):
                post_whole_text += post_body_text
            local_post_and_comment_text.append(post_whole_text)

            if row_length - 5 > 0:
                number_of_comments = math.ceil((row_length - 5) / 4)
                for i in range(1, number_of_comments + 1):
                    comment_user_id = str(ps_comnt.iloc[row][4 * i])
                    comment_data = str(ps_comnt.iloc[row][4 * i + 1])
                    if comment_user_id != 'nan':
                        local_user_ids.append(comment_user_id)
                    if comment_data != 'nan':
                        local_post_and_comment_text.append(comment_data)
            post_and_comment_text.append(local_post_and_comment_text)
            user_ids.append(local_user_ids)
    except Exception as err:
        print(err.with_traceback())
    return [post_and_comment_text, user_ids]


def remove_emojis(posts_and_comments):
    total_data_post_comment = []
    for p in posts_and_comments:
        local_data = []
        for c in p:
            text = text_cleaning_utilities.remove_emoji(c)
            local_data.append(text)
        total_data_post_comment.append(local_data)
    return total_data_post_comment


def remove_special_character(emojis_free_text):
    total_data_post_comment = []
    for p in emojis_free_text:
        local_data = []
        for c in p:
            text = text_cleaning_utilities.remove_special_characters(c)
            local_data.append(text)
        total_data_post_comment.append(local_data)
    return total_data_post_comment


def split_sentences(special_character_removed):
    return [text_cleaning_utilities.split_sentences(post_comment) for post_comment in special_character_removed]


def sentence_to_clean_lemmatization(split_sentence_to_text):
    words_token = []
    for text in split_sentence_to_text:
        lemmatized_sentence = text_cleaning_utilities.get_lemmatized_sentence(text)
        words_token.append(lemmatized_sentence)
    # return [text_cleaning_utilities.work_tokenize(text) for text in split_sentence_to_text]
    return words_token


def get_clean_tokens(texts):
    tokens = []
    for text in texts:
        clean_tokens = text_cleaning_utilities.get_clean_tokens(text)
        tokens.append(clean_tokens)

    return tokens


def make_bigram_trigram(texts):
    bigram_model = text_cleaning_utilities.build_bigram_trigram_models(texts)
    token_with_bigram = text_cleaning_utilities.get_bigram_words(texts, bigram_model[0])
    token_with_bigram_trigram = text_cleaning_utilities.get_bigram_trigram_words(token_with_bigram, bigram_model)
    return token_with_bigram_trigram


def jaccard_similarity(topic_1, topic_2):
    intersection = set(topic_1).intersection(set(topic_2))
    union = set(topic_1).union(set(topic_2))
    return float(len(intersection)) / float(len(union))

def removed_frequent_unnecery_tokens(texts):
    tokens = text_cleaning_utilities.removed_frequent_words(texts)
    return tokens


def clean_and_tokenized(post_and_comment):
    remove_emojis_from_post_comment = remove_emojis(post_and_comment)
    remove_special_characters_from_post_comment = remove_special_character(remove_emojis_from_post_comment)
    split_into_sentence = split_sentences(remove_special_characters_from_post_comment)
    clean_lemmatized_sentences = sentence_to_clean_lemmatization(split_into_sentence)
    clean_tokenized_words = get_clean_tokens(clean_lemmatized_sentences)
    # bigram_trigram_data = make_bigram_trigram(clean_tokenized_words)
    removed_frequent_words = removed_frequent_unnecery_tokens(clean_tokenized_words)

    # save the processed data

    writer = pd.ExcelWriter("post_processed_data.xlsx")

    df = pd.DataFrame(post_and_comment)
    df.to_excel(writer, sheet_name='raw_data', index=True)
    df = pd.DataFrame(remove_emojis_from_post_comment)
    df.to_excel(writer, sheet_name='emojis_removed_data', index=True)
    df = pd.DataFrame(split_into_sentence)
    df.to_excel(writer, sheet_name='split_sentence_data', index=True)
    df = pd.DataFrame(clean_lemmatized_sentences)
    df.to_excel(writer, sheet_name='lemmatized_data', index=True)
    df = pd.DataFrame(clean_tokenized_words)
    df.to_excel(writer, sheet_name='tokenized_data', index=True)
    # df = pd.DataFrame(bigram_trigram_data)
    # df.to_excel(writer, sheet_name='bi_trigram_data', index=True)
    df = pd.DataFrame(removed_frequent_words[0])
    df.to_excel(writer, sheet_name='bag_words_data', index=True)
    writer.save()
    writer.close()

    return [removed_frequent_words, clean_tokenized_words]


def process_text(posts_and_comments):
    bag_words = clean_and_tokenized(posts_and_comments)
    return bag_words


def topic_modeling(texts):
    lda_models = ldamodel.LdaModel(
        corpus=texts[0],
        id2word=texts[1],
        num_topics=58,
        random_state=100,
        update_every=1,
        chunksize=100,
        passes=10,
        alpha='auto'
    )
    return lda_models


def compute_coherence_values(mallet_path, dictionary, corpus, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


def convertldaGenToldaMallet(mallet_model):
    model_gensim = LdaModel(
        id2word=mallet_model.id2word, num_topics=mallet_model.num_topics,
        alpha=mallet_model.alpha, eta=0,
    )
    model_gensim.state.sstats[...] = mallet_model.wordtopics
    model_gensim.sync_state()
    return model_gensim


def data_cleaning_submission_comments(submission_comment_combined_df,dir_name):
    os.makedirs(dir_name, exist_ok=True)
    if submission_comment_combined_df is not None:
        post_and_comment = get_post_and_comment_text(submission_comment_combined_df.head(10))
        processed_data = process_text(post_and_comment[0])
        degree_df = pd.DataFrame([post_and_comment[1]])
        print([post_and_comment[1]])
        degree_df.to_csv(dir_name+'/graph_node.csv', encoding='utf-8-sig')


        # take different topic numbers
        num_topics = [i for i in range(6,61,2)]
        num_keywords = len(num_topics)
        LDA_models = {}
        LDA_topics = {}
        for i in num_topics:
            LDA_models[i] = LdaModel(corpus=processed_data[0][0],
                                     id2word=processed_data[0][1],
                                     num_topics=i,
                                     update_every=1,
                                     chunksize=len(processed_data[0][0]),
                                     passes=20,
                                     alpha='auto',
                                     random_state=42)

        #     shown_topics = LDA_models[i].show_topics(num_topics=i,
        #                                              num_words=num_keywords,
        #                                              formatted=False)
        #     LDA_topics[i] = [[word[0] for word in topic[1]] for topic in shown_topics]
        # LDA_stability = {}
        # for i in range(0, len(num_topics) - 1):
        #     jaccard_sims = []
        #     for t1, topic1 in enumerate(LDA_topics[num_topics[i]]):  # pylint: disable=unused-variable
        #         sims = []
        #         for t2, topic2 in enumerate(LDA_topics[num_topics[i + 1]]):  # pylint: disable=unused-variable
        #             sims.append(jaccard_similarity(topic1, topic2))
        #
        #         jaccard_sims.append(sims)
        #
        #     LDA_stability[num_topics[i]] = jaccard_sims
        #
        # mean_stabilities = [np.array(LDA_stability[i]).mean() for i in num_topics[:-1]]
        #
        # coherences = [CoherenceModel(model=LDA_models[i], texts=processed_data[1], dictionary=processed_data[0][1],
        #                              coherence='c_v').get_coherence() for i in num_topics[:-1]]
        #
        # coh_sta_diffs = [coherences[i] - mean_stabilities[i] for i in
        #                  range(num_keywords)[:-1]]  # limit topic numbers to the number of keywords
        # coh_sta_max = max(coh_sta_diffs)
        # coh_sta_max_idxs = [i for i, j in enumerate(coh_sta_diffs) if j == coh_sta_max]
        # ideal_topic_num_index = coh_sta_max_idxs[0]  # choose less topics in case there's more than one max
        # ideal_topic_num = num_topics[ideal_topic_num_index]
        # print("Topic Number:" , ideal_topic_num)
        #
        # plt.figure(figsize=(20, 10))
        # ax = sns.lineplot(x=num_topics[:-1], y=mean_stabilities, label='Average Topic Overlap')
        # ax = sns.lineplot(x=num_topics[:-1], y=coherences, label='Topic Coherence')
        #
        # ax.axvline(x=ideal_topic_num, label='Ideal Number of Topics', color='black')
        # ax.axvspan(xmin=ideal_topic_num - 1, xmax=ideal_topic_num + 1, alpha=0.5, facecolor='grey')
        #
        # y_max = max(max(mean_stabilities), max(coherences)) + (0.10 * max(max(mean_stabilities), max(coherences)))
        # ax.set_ylim([0, y_max])
        # ax.set_xlim([1, num_topics[-1] - 1])
        #
        # ax.axes.set_title('Model Metrics per Number of Topics', fontsize=25)
        # ax.set_ylabel('Metric Level', fontsize=20)
        # ax.set_xlabel('Number of Topics', fontsize=20)
        # plt.legend(fontsize=20)
        # plt.savefig("Test.png")
        # plt.show()
        #
        # topic_models = topic_modeling(processed_data[0])
        # coherence_model_lad = CoherenceModel(model=topic_models, texts=processed_data[1],
        #                                      dictionary=processed_data[0][1], coherence='c_v')
        # coherence_lda = coherence_model_lad.get_coherence()
        # print('\\n Coherence Socre: ', coherence_lda)
        # mallet_path = 'C:\\mallet-2.0.8\\bin\\mallet'
        # # mallet_path = '/mmfs1/projects/saeed.salem/mallet-2.0.8/bin/mallet'
        #
        # ldamallet = gensim.models.wrappers.ldamallet.LdaMallet(mallet_path, corpus=processed_data[0][0], num_topics=30,
        #                                                        id2word=processed_data[0][1])
        # pprint(ldamallet.show_topics(formatted=False))
        # coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=processed_data[1],
        #                                            dictionary=processed_data[0][1], coherence='c_v')
        # coherence_ldamallet = coherence_model_ldamallet.get_coherence()
        # print('\\n Coherence Socre: ', coherence_ldamallet)
        #
        # model_list, coherence_values = compute_coherence_values(mallet_path, dictionary=processed_data[0][1],
        #                                                         corpus=processed_data[0][0], texts=processed_data[1],
        #                                                         start=2, limit=100, step=5)
        #
        # # Show graph
        # limit = 100
        # start = 2
        # step = 5
        # x = range(start, limit, step)
        # plt.plot(x, coherence_values)
        # plt.xlabel("Num Topics")
        # plt.ylabel("Coherence score")
        # plt.legend(("coherence_values"), loc='best')
        # plt.savefig("graph.png")
        # plt.show()
        #
        # best_result_index = coherence_values.index(max(coherence_values))
        # optimal_model = model_list[best_result_index]
        # # Select the model and print the topics
        # model_topics = optimal_model.show_topics(formatted=False)
        # print(f'''The {x[best_result_index]} topics gives the highest coherence score \\
        # of {coherence_values[best_result_index]}''')
        # optimal_model = convertldaGenToldaMallet(optimal_model)
        #
        # pprint(topic_models.print_topics())
        # vis = pyLDAvis.gensim_models.prepare(topic_models, processed_data[0][0], processed_data[0][1])
        # pyLDAvis.save_html(vis, "post_topice_result.html")
