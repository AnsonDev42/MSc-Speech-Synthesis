from scrapper import get_data


def load_standard_phonelist(diphone=False):
    if diphone:
        tmp_name = 'diphone_list'
    else:
        tmp_name = 'phone_list'
    with open(tmp_name, 'r') as f:
        phonelist = f.readlines()
    phonelist = [phone.strip() for phone in phonelist]
    return phonelist


pl = load_standard_phonelist(diphone=False)
print(pl)


def create_diphone_list():
    """
    create a file for storing all possible diphones ???TODO: check needed and how to get the rank?
    :return:
    """
    all_phones = load_standard_phonelist()
    with open('diphone_list', 'w') as f:
        for phone1 in pl:
            for phone2 in pl:
                if phone1 == phone2:
                    continue
                f.write(f'{phone1}-{phone2}\n')
    return


def phone_to_diphone(phone_list=[]):
    """
    convert a list of phones to a list of diphones
    :param phone_list:
    :return:
    """
    if not phone_list:
        return []
    diphone_list = []
    for i in range(len(phone_list) - 1):
        diphone_list.append(f'{phone_list[i]}-{phone_list[i + 1]}')
    return diphone_list


def load_phone_list():
    """

    TODO: for now its phone list.... FIX IT TO diphone
    :return:
    """

    import pickle
    sentence2diphones = {}
    with open('sentence2diphones.pkl', 'rb') as f:
        sentence2diphones = pickle.load(f)
        if sentence2diphones:
            return sentence2diphones

    with open('utts_train.mlf', 'r') as f:
        lines = f.readlines()
    sentence_index = -1
    tmp_diphones = []
    for line in lines:
        if line.startswith('#!MLF!#'):
            sentence2diphones[sentence_index] = tmp_diphones
            tmp_diphones = []
            continue
        if line.startswith('"*/'):
            # get the sentence index such as "*/c_books_train_0001.lab" to 1
            sentence_index = int(line.split('_')[-1].split('.')[0])
            continue
        tmp_diphones.append(line.strip())
    sentence2diphones.remove(-1)  # remove the first empty element

    # create a binary pickle file
    f = open("sentence2diphones.pkl", "wb")
    # write the python object (dict) to pickle file
    pickle.dump(sentence2diphones, f)
    f.close()
    return sentence2diphones


def greedy_picker(sentences=[]):
    """"
    this function will pick the sentences that are most valuable to the system
    in a greedy manner, only check a few sentences at a time

    """
    if not sentences:
        train_sentences = get_data('train')
    assert len(train_sentences) > 0
    # pick the first sentence

    # pretend to have a dictionrary with scores: {'aa':20, 'bb':19, 'cc':18, ...}
    scores = {}

    # another dictionary record if the sentence has been picked: {'aa':True, 'bb':False, 'cc':False, ...}
    picked = {}
    current_sentences = 0
    current_sentences_set = {}  # only store the index of the sentence in the train_sentences

    # create a priority queue to store the sentence index and its score
    import heapq
    sentence_score_queue = []
    sentence2phone = load_phone_list()

    def get_diphones(sentence_idx):
        # get the diphones of the sentence
        phones = sentence2phone[sentence_idx]
        diphones = phone_to_diphone(phones)
        return diphones

    def score_sentence(index):
        # obtain the diphones of the sentence
        diphones = get_diphones(index)
        score = 0
        max_unseen_diphone_reward = 0  # maybe remove this but giving heavy reward to unseen diphones
        for diphone in diphones:
            score += scores[diphone]
            if not picked[diphone] and scores[diphone] > max_unseen_diphone_reward:
                max_unseen_diphone_reward = scores[diphone]
        score /= len(diphones)

        return score, max_unseen_diphone_reward

    def pick1(sentences):
        # randomly pick 10 sentences, and score them with normalisation:
        # ((12+15+3 .. )+( if it hitted the first time, times 10 to the scores ) ) / len(sentence)
        # score the sentence
        picking_index = -1

        # score = score_sentence(sentence)
        # scores[sentence] = score
        # picked[sentence] = False
        # pick the sentence with the highest score
        # add the sentence to the current_sentences
        # remove the sentence from the train_sentences
        return

    aim_num = 100
    while current_sentences < aim_num:
        pick1()
        current_sentences += 1
    # repeat until the current_sentences >= aim_num

    #

    return current_sentences_set
