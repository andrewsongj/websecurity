import string, hashlib, itertools, random
from multiprocessing.pool import Pool

PER_WORKER_BEFORE_CHECK = 1_000_000
TOTAL_WORKER_RUNS = 10_000

POSSIBLE_MATCH_0 = ("'",)
POSSIBLE_MATCH_1 = ("||", "or", "oR", "Or", "OR")
POSSIBLE_MATCH_2 = ("'",)
POSSIBLE_MATCH_3 = tuple(str(d) for d in range(1, 10))

GUESS_CHAR_POOL = string.ascii_letters + string.digits
GUESS_LEN = 48

def all_matches_bytes():
    return tuple(("".join(p)).encode() for p in itertools.product(POSSIBLE_MATCH_0, POSSIBLE_MATCH_1, POSSIBLE_MATCH_2, POSSIBLE_MATCH_3))

def work(wid):
    to_match = all_matches_bytes()
    for i in range(PER_WORKER_BEFORE_CHECK):
        random_string = "".join(random.choices(GUESS_CHAR_POOL, k=GUESS_LEN))
        random_string_enc = random_string.encode()
        h = hashlib.md5()
        h.update(random_string_enc)
        hash_enc = h.digest()
        for pm in to_match:
            if hash_enc.find(pm) != -1:
                return random_string
    return None

def main():
    with Pool() as pool:
        print("Looking for solution...")
        it = pool.imap_unordered(work, range(TOTAL_WORKER_RUNS))
        for i in range(TOTAL_WORKER_RUNS):
            check = next(it)
            if check is not None:
                print("Solution found: ")
                print(check)
                exit(0)
            print("Iterations completed: {}".format((i + 1) * PER_WORKER_BEFORE_CHECK))
    print("No solution found...")
    exit(1)

if __name__ == "__main__":
    main()