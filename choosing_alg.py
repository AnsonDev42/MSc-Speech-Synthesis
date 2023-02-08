from scrapper import get_train_data
from queue import PriorityQueue


def build_diphone_pq():
    # build a priority queue of diphones
    # diphones are tuples of two phonemes
    # the priority is the number of times the diphone occurs in the corpus
    # the priority queue is a list of tuples (priority, diphone)
    # the priority queue is sorted by priority
    q = PriorityQueue()


def greedy_picker(sentences=[]):
    if not sentences:
        sentences = get_train_data()
    assert len(sentences) > 0
    # pick the first sentence
