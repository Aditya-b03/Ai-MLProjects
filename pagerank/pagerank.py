import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    No_of_pages = len(corpus)
    prob_dict = dict()
    if len(corpus[page]) == 0:
        prob = 1/No_of_pages
        for link in corpus:
            prob_dict[link] = prob
    else:
        No_of_links = len(corpus[page])
        unlinked_prob = (1 - damping_factor)/No_of_pages
        linked_prob = unlinked_prob + (damping_factor/No_of_links)
        for link in corpus:
            if link in corpus[page]:
                prob_dict[link] = linked_prob
            else:
                prob_dict[link] = unlinked_prob
    
    return prob_dict

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    transition_matrix = dict()
    for page in corpus:
        transition_matrix[page] = transition_model(corpus , page , damping_factor)


    start_page = random.choice(list(corpus.keys()))
    count = dict()
    for page in corpus:
        count[page] = 0

    currPage = start_page
    for i in range(n):
        newPage = random.choices(list(transition_matrix[currPage].keys()),weights=transition_matrix[currPage].values() , k=1)
        count[newPage[0]] += 1
        currPage = newPage[0]

    pageRank = dict()
    for page in count:
        pageRank[page] = count[page]/n
        
    
    return pageRank
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    transition_matrix = dict()
    for page in corpus:
        transition_matrix[page] = transition_model(corpus , page , damping_factor)
    
    PrevStateProb = dict()
    CurrentStateProb = dict()

    N = len(corpus)

    for page in corpus:
        PrevStateProb[page] = 2
        CurrentStateProb[page] = 1/len(corpus)
    
    while(True):
        
        converged = True
        for page in corpus:
            if abs(CurrentStateProb[page] - PrevStateProb[page]) > 0.001:
                converged = False
        
        if(converged):
            break
        else:
            for page in corpus:
                PrevStateProb[page] = CurrentStateProb[page]

        for ToPage in corpus:
            ProbSum = 0
            for FromPage in corpus:
                ProbSum += PrevStateProb[FromPage]*transition_matrix[FromPage][ToPage]
            CurrentStateProb[ToPage] = ProbSum

    return PrevStateProb
    raise NotImplementedError


if __name__ == "__main__":
    main()
