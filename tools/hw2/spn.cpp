#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
// converted from my python ver.
using namespace std;

unordered_map<int, int> pi_s = {
    {0, 14}, {1, 4}, {2, 13}, {3, 1},
    {4, 2}, {5, 15}, {6, 11}, {7, 8},
    {8, 3}, {9, 10}, {10, 6}, {11, 12},
    {12, 5}, {13, 9}, {14, 0}, {15, 7}
};

unordered_map<int, int> pi_p = {
    {0, 1}, {1, 5}, {2, 9}, {3, 13},
    {4, 2}, {5, 6}, {6, 10}, {7, 14},
    {8, 3}, {9, 7}, {10, 11}, {11, 15},
    {12, 4}, {13, 8}, {14, 12}, {15, 16}
};

vector<int> get_Kr(int r, vector<int>& K) {
    vector<int> K_extended = K;
    K_extended.insert(K_extended.end(), K.begin(), K.end());  // 扩展K
    int index = 4 * r - 3 - 1;
    index = index % 32;
    return vector<int>(K_extended.begin() + index, K_extended.begin() + index + 16);
}

vector<int> xor_vectors(const vector<int>& a, const vector<int>& b) {
    vector<int> res(a.size());
    for (size_t i = 0; i < a.size(); i++) {
        res[i] = a[i] ^ b[i]; // 直接用异或运算
    }
    return res;
}

vector<int> do_substitute(const vector<int>& u, int l, int m) {
    vector<int> v;
    for (int i = 0; i < m; i++) {
        int before_pi_s = 0;
        for (int j = 0; j < l; j++) {
            before_pi_s = (before_pi_s << 1) | u[i * l + j];
        }
        int after_pi_s = pi_s[before_pi_s];
        
        for (int j = l - 1; j >= 0; j--) {
            v.push_back((after_pi_s >> j) & 1);
        }
    }
    return v;
}

vector<int> do_permutation(const vector<int>& v, int l, int m) {
    vector<int> res(l * m);
    for (int i = 0; i < l * m; i++) {
        res[pi_p[i] - 1] = v[i];
    }
    return res;
}

vector<int> parse_input_string(const string& input) {
    vector<int> result;
    for (char c : input) {
        if (c == '0' || c == '1') {
            result.push_back(c - '0');
        }
    }
    return result;
}

int main() {
    string x_str, K_str;
    cin >> x_str >> K_str;

    vector<int> x = parse_input_string(x_str);
    vector<int> K = parse_input_string(K_str);

    vector<int> y;
    int l = 4, m = 4, Nr = 4;
    vector<int> w = x;

    for (int r = 1; r < Nr; r++) {
        vector<int> u = xor_vectors(w, get_Kr(r, K));
        vector<int> v = do_substitute(u, l, m);
        w = do_permutation(v, l, m);
    }

    vector<int> u = xor_vectors(w, get_Kr(Nr, K));
    vector<int> v = do_substitute(u, l, m);
    y = xor_vectors(v, get_Kr(Nr + 1, K));

    for (int i = 0; i < l * m; i++) {
        cout << y[i];
    }
    // cout << endl;

    return 0;
}
