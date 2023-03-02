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


def create_diphone_list():
    """
    create a file for storing all possible diphones
    :return:
    """
    all_phones = load_standard_phonelist()
    with open('diphone_list', 'w') as f:
        for phone1 in all_phones:
            for phone2 in all_phones:
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


def load_books_phone_list(diphone=True, create=False):
    """
        create dic for each sentence to a list of phones and a dic for a list of diphones
        if exists, load from pickle file depending on param diphone

    :return: a dictionary of sentence index to a list of phones
    """

    import pickle
    sentence2diphones = {}
    sentence2phones = {}
    if not create:
        try:
            if not diphone:
                with open('sentence2phones.pkl', 'rb') as f:
                    sentence2phones = pickle.load(f)
                    if sentence2phones:
                        return sentence2phones
            else:
                with open('sentence2diphones.pkl', 'rb') as f:
                    sentence2diphones = pickle.load(f)
                    if sentence2diphones:
                        return sentence2diphones
        except:
            print('pickle file not found, creating new one')

    with open('utts_train.mlf', 'r') as f:
        lines = f.readlines()
    sentence_index = -1  # palceholder, remove later
    tmp_phone_list = []
    tmp_diphone_list = []
    for line in lines:
        if line.startswith('#!MLF!#'):
            sentence2phones[sentence_index] = tmp_phone_list
            sentence2diphones[sentence_index] = phone_to_diphone(tmp_phone_list)
            tmp_phone_list = []
            continue
        if line.startswith('"*/'):
            # get the sentence index such as "*/c_books_train_0001.lab" to 1
            sentence_index = int(line.split('_')[-1].split('.')[0])
            continue
        tmp_phone_list.append(line.strip())
    sentence2phones.pop(-1)
    sentence2diphones.pop(-1)  # remove the first empty element

    # create a binary pickle file
    f = open("sentence2diphones.pkl", "wb")
    pickle.dump(sentence2diphones, f)
    f.close()
    f = open("sentence2phones.pkl", "wb")
    pickle.dump(sentence2phones, f)
    f.close()

    if diphone:
        return sentence2diphones
    return sentence2phones


def get_distribution(diphone=False):
    standarded_phonelist = load_standard_phonelist(diphone=diphone)
    sentence2phone = load_books_phone_list(diphone=diphone)
    # now only for phones
    distribution = {}
    for sentence in sentence2phone.keys():
        for phone in sentence2phone[sentence]:
            if phone in distribution:
                distribution[phone] += 1
            else:
                distribution[phone] = 1

    # rank the distribution and print it
    # print(distribution)
    return distribution


def greedy_picker(num_sentences=100, num_candidates=10):
    """"
    this function will pick the sentences that are most valuable to the system
    in a greedy manner, only check a few sentences at a time

    """

    current_sentences_set = set()  # only store the index of the sentence in the train_sentences
    sentence2diphone = load_books_phone_list(diphone=True)
    assert len(sentence2diphone) > 0

    distribution = get_distribution(diphone=True)
    seen_diphone = set()

    def score_sentence(sentence_idx):
        # obtain the diphones of the sentence
        diphones = sentence2diphone[sentence_idx]
        local_seen_diphone = set()
        score = 0

        for diphone in diphones:
            score += (10 / distribution[diphone])
            if diphone not in local_seen_diphone and diphone not in seen_diphone:
                local_seen_diphone.add(diphone)
                score += (50 / distribution[diphone])

        # add variety diphone score
        n_kind = len(set(local_seen_diphone))
        score += 0.5 * n_kind
        score /= len(diphones)

        return score, local_seen_diphone

    def pick1(num_candidates=10):
        # randomly pick 10 sentences, and score them with normalisation:
        # ((12+15+3 .. )+( if it hitted the first time, times 10 to the scores ) ) / len(sentence)
        # score the sentence
        max_score = 0
        max_seen_diphone = set()
        # generate 10 random numbers
        import random
        random_numbers = []
        # generate 10 random numbers
        i = 0
        # set seed for reproducibility
        random.seed(42)
        while i < num_candidates:
            r = random.randint(0, len(sentence2diphone))
            if r not in random_numbers and r not in current_sentences_set:
                random_numbers.append(r)
                i += 1

        for idx in random_numbers:
            score, local_seen_diphone = score_sentence(idx)
            if score > max_score:
                max_score = score
                max_idx = idx
                max_seen_diphone = local_seen_diphone
        #  adding the max_seen_diphone into seen_diphone
        seen_diphone.update(max_seen_diphone)

        return max_idx

    while len(current_sentences_set) < num_sentences:
        current_sentences_set.add(pick1(num_candidates=num_candidates))

    return current_sentences_set


def plot_distribution():
    import matplotlib.pyplot as plt
    import numpy as np

    drawing_diphone = get_distribution(diphone=True)
    drawing_diphone = sorted(drawing_diphone.items(), key=lambda x: x[1], reverse=True)
    plt.bar(np.arange(len(drawing_diphone)), [x[1] for x in drawing_diphone])
    plt.show()

    drawing_phone = get_distribution(diphone=False)
    drawing_phone = sorted(drawing_phone.items(), key=lambda x: x[1], reverse=True)
    plt.bar(np.arange(len(drawing_phone)), [x[1] for x in drawing_phone])
    plt.show()


def check_coverage(sentence_indices=[]):
    """
    check the coverage of the sentences
    :param sentence_indices:
    :return:
    """
    sentence2diphone = load_books_phone_list(diphone=True)
    distribution = get_distribution(diphone=True)
    seen_diphone = set()
    for idx in sentence_indices:
        diphones = sentence2diphone[idx]
        for diphone in diphones:
            if diphone not in seen_diphone:
                seen_diphone.add(diphone)
    print('seen diphone: ', len(seen_diphone))
    print('total diphone in books: ', len(distribution))
    print('theoretical diphones: ', 6006)
    print(f"selected sentences' coverage in total diphone in books :{100 * len(seen_diphone) / len(distribution)}% ")
    print(f"selected sentences' coverage in theoretical diphone :{100 * len(seen_diphone) / 6006}% ")
    print(f"total books' sentences coverage in theoretical diphone  :{100 * len(distribution) / 6006}% ")


def run_baseline(aim_sentences=100):
    import random
    sentence2diphone = load_books_phone_list(diphone=True)
    # generate 150 numbers from 0 to len(sentence2diphone)
    random.seed(43)
    random_numbers = []
    i = 0
    while i < aim_sentences:
        r = random.randint(0, len(sentence2diphone))
        if r not in random_numbers:
            random_numbers.append(r)
            i += 1
    check_coverage(random_numbers)


if __name__ == '__main__':
    plot_distribution()

    aim_sentences = 100
    # run_baseline(aim_sentences=aim_sentences)
    res = greedy_picker(aim_sentences, num_candidates=50)
    check_coverage(res)
