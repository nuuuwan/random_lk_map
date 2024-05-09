from random_lk_map import RandomLKMap, ReadMe

N_GENS_PER_PIPELINE = 1


def main():
    for _ in range(N_GENS_PER_PIPELINE):
        RandomLKMap.gen()
    ReadMe().build()


if __name__ == "__main__":
    main()
