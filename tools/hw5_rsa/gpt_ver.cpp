#include <iostream>
using namespace std;

typedef unsigned long long ull;

// 计算 (a * b) mod n，避免溢出
ull mul_mod(ull a, ull b, ull mod) {
    __int128_t temp = (__int128_t)a * b;
    __int128_t quotient = temp / mod;
    __int128_t remainder = temp - quotient * mod;
    return (ull)remainder;
}

// 计算 base^exp mod mod，使用二进制平方乘法算法
ull pow_mod(ull base, ull exp, ull mod) {
    ull result = 1;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = mul_mod(result, base, mod);
        }
        base = mul_mod(base, base, mod);
        exp /= 2;
    }
    return result;
}

// RSA解密函数：m = c^d mod n
ull decrypt(ull c, ull d, ull n) {
    return pow_mod(c, d, n);
}

int main() {
    ull c ;
    ull d; 
    ull n; 

    ull m = decrypt(c, d, n);
    cout << "Decrypted message: " << m << endl;


    long long p,q,e,c;
    cin >> p >> q >> e >> c;
    if (p * q > 0) {
      throw "too big";
    }
    const long long euler_n = (p-1)*(q-1);
    long long d = mul_inverse(e, euler_n);
    long long n = p*q;
    long long m = Square_and_mul(c, static_cast<long long>(d), n);
  
    // cout << euler_n <<endl;
    // cout << d <<endl;
    // cout << c <<endl;
    // cout << static_cast<long long>(d)<<endl;
    // cout << n << endl;
    cout << m <<endl;
    return 0;
}