from Differential_analysis import solution
import random


def check_solution(test_times, effective_pair_per_run):
    random_list = [f"{random.getrandbits(32):032b}" for _ in range(test_times)]
    for index, random_key in enumerate(random_list):
        failed = False
        ans_K = solution(random_key, effective_pair_per_run)
        for i in range(4, 8):
            if not ans_K[i] == random_key[4 * i : 4 * i + 4]:
                print(f"FAILED  {index}th test")
                print(f"Random_key :\n{random_key}")
                print(f"ans_K :\n{ans_K[4:8]}")
                print(
                    f"对应的random_key 后16位: \n{[random_key[4*i:4*i+4] for i in range(4,8)]}"
                )
                print("以上，用来检查哪个出错了")
                failed = True
        if not failed:
            print(f"PASSED  {index}th test")
