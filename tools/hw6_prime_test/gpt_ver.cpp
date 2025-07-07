#include <iostream>
#include <random>
#include <cstdint>

using namespace std;

// 快速幂 (a^b mod m)
uint64_t mod_pow(uint64_t a, uint64_t b, uint64_t m) {
    uint64_t result = 1;
    a %= m;
    while (b > 0) {
        if (b & 1)
            result = (__uint128_t(result) * a) % m;
        a = (__uint128_t(a) * a) % m;
        b >>= 1;
    }
    return result;
}

bool miller_test(uint64_t d, uint64_t n, uint64_t a) {
    uint64_t x = mod_pow(a, d, n);
    if (x == 1 || x == n - 1)
        return true;

    while (d != n - 1) {
        x = (__uint128_t(x) * x) % n;
        d *= 2;

        if (x == 1) return false;
        if (x == n - 1) return true;
    }

    return false;
}

// Miller-Rabin 测试
bool is_prime(uint64_t n, int k = 5) {
    if (n < 2)
        return false;
    if (n <= 3)
        return true;
    if (n % 2 == 0)
        return false;

    // n-1 = d * 2^r
    uint64_t d = n - 1;
    while (d % 2 == 0)
        d /= 2;

    random_device rd;
    mt19937_64 gen(rd());
    uniform_int_distribution<uint64_t> dist(2, n - 2);

    for (int i = 0; i < k; ++i) {
        uint64_t a = dist(gen);
        if (!miller_test(d, n, a))
            return false;
    }

    return true;
}

int main() {
    uint64_t num;
    cin >> num;

    if (is_prime(num))
        cout <<  "Yes";
    else
        cout << "No";

    return 0;
}
