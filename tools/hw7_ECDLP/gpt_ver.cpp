#include <bits/stdc++.h>
using namespace std;
using ll = long long;




// 求逆元
ll mod_inv(ll a, ll p) {
    ll b = p, x = 1, y = 0;
    while (b) {
        ll q = a / b;
        tie(a, b) = make_pair(b, a - q * b);
        tie(x, y) = make_pair(y, x - q * y);
    }
    if (x < 0) x += p;
    return x;
}
ll a, b, p;

struct Point {
    ll x, y;
    bool is_inf() const { return x == -1 && y == -1; }
};

// 点加
Point add(const Point &P, const Point &Q) {
    if (P.is_inf()) return Q;
    if (Q.is_inf()) return P;
    if (P.x == Q.x) {
        // P == -Q?
        if ((P.y + Q.y) % p == 0) 
            return {-1, -1};
        // P == Q, 用切线
        ll num = (3 * (P.x * P.x % p) + a) % p;
        ll den = mod_inv((2 * P.y) % p, p);
        ll lam = num * den % p;
        ll xr = (lam * lam - P.x - Q.x) % p;
        if (xr < 0) xr += p;
        ll yr = (lam * (P.x - xr) - P.y) % p;
        if (yr < 0) yr += p;
        return {xr, yr};
    } else {
        // 一般点加
        ll num = (Q.y - P.y) % p; if (num < 0) num += p;
        ll den = (Q.x - P.x) % p; if (den < 0) den += p;
        den = mod_inv(den, p);
        ll lam = num * den % p;
        ll xr = (lam * lam - P.x - Q.x) % p;
        if (xr < 0) xr += p;
        ll yr = (lam * (P.x - xr) - P.y) % p;
        if (yr < 0) yr += p;
        return {xr, yr};
    }
}

// k*P
Point mul(Point P, ll k) {
    Point R = {-1, -1}; // 单位元
    while (k) {
        if (k & 1) R = add(R, P);
        P = add(P, P);
        k >>= 1;
    }
    return R;
}

int main(){


    ll x, y, X, Y;
    cin >> a >> b >> p;
    cin >> x >> y >> X >> Y;
    Point P = {x, y}, Q = {X, Y};

    if (Q.is_inf()) {
        cout << 0 << "\n";
        return 0;
    }
    const int N = 1 << 16;       
    int m = (int)ceil(sqrt(N));  

    // baby 步： 存 j*P → j
    unordered_map<ll,int> baby;
    baby.reserve(m+1);
    Point cur = {-1, -1};
    for (int j = 0; j < m; j++) {
        // 用 (x<<32)|y 作为 key
        ll key = (cur.x << 32) ^ cur.y;
        if (!baby.count(key)) baby[key] = j;
        cur = add(cur, P);
    }

    // giant 步： 用 Q - i*m*P 来匹配 baby
    Point mP = mul(P, m);
    Point giant = Q;
    for (int i = 0; i <= m; i++) {
        ll key = (giant.x << 32) ^ giant.y;
        if (baby.count(key)) {
            ll j = baby[key];
            ll k = (ll)i * m + j;
            if (k < N) {
                cout << k << "\n";
                return 0;
            }
        }
        // giant = giant - mP  == giant + (-mP)
        // 计算 -mP
        Point neg_mP = {mP.x, (-mP.y + p) % p};
        giant = add(giant, neg_mP);
    }

    cout << -1 << "\n";
    return 0;
}
