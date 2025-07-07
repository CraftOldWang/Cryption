#include <iostream>

// Global curve parameters
long long A_CURVE, B_CURVE, P_MOD;

// Modular exponentiation: (base^exp) % P_MOD
long long power(long long base, long long exp) {
    long long res = 1;
    base %= P_MOD;
    if (base < 0) base += P_MOD; // Ensure base is non-negative
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % P_MOD;
        base = (base * base) % P_MOD;
        exp /= 2;
    }
    return res;
}

// Modular inverse: n^(-1) % P_MOD using Fermat's Little Theorem
long long modInverse(long long n) {
    long long norm_n = n % P_MOD;
    if (norm_n < 0) norm_n += P_MOD;
    // Inverse of 0 is undefined. Problem constraints should prevent this for valid operations.
    // E.g. 2*y cannot be 0 unless y=0 (for odd P_MOD) or P_MOD=2.
    // If y=0, point_double handles it by returning infinity.
    return power(norm_n, P_MOD - 2);
}

// Normalize value to [0, P_MOD-1]
long long normalize(long long val) {
    long long res = val % P_MOD;
    if (res < 0) res += P_MOD;
    return res;
}

struct Point {
    long long x, y;

    // Default constructor for point at infinity using problem's convention
    Point(long long _x = -1, long long _y = -1) : x(_x), y(_y) {}

    bool is_infinity() const {
        return x == -1 && y == -1;
    }

    // Equality operator
    bool operator==(const Point& other) const {
        // If both are infinity, they are equal
        if (is_infinity() && other.is_infinity()) return true;
        // If one is infinity and the other is not, they are not equal
        if (is_infinity() || other.is_infinity()) return false;
        // Otherwise, compare coordinates (assuming they are already normalized)
        return x == other.x && y == other.y;
    }
};

// Point doubling: R = 2*P
Point point_double(Point p) {
    if (p.is_infinity()) return Point(); // 2 * Infinity = Infinity
    if (normalize(p.y) == 0) return Point(); // Tangent is vertical, 2P = Infinity

    // Lambda = (3*x_P^2 + A_CURVE) / (2*y_P)
    long long term_3x2 = 3 * p.x * p.x;
    long long num_val = term_3x2 + A_CURVE;
    long long den_val = 2 * p.y;

    long long lambda = normalize(normalize(num_val) * modInverse(den_val));

    // x_R = lambda^2 - 2*x_P
    long long lambda_sq = lambda * lambda;
    long long term_2xP = 2 * p.x;
    long long xr_val = lambda_sq - term_2xP;
    long long xr = normalize(xr_val);

    // y_R = lambda*(x_P - x_R) - y_P
    // Important: (p.x - xr) must be calculated correctly with potential negatives
    // before being multiplied by lambda. All done with full integer precision then normalized.
    long long term_xP_minus_xr = p.x - xr; // xr is already normalized here
    long long yr_val = lambda * term_xP_minus_xr - p.y;
    long long yr = normalize(yr_val);
    
    return Point(xr, yr);
}

// Point addition: R = P1 + P2
Point point_add(Point p1, Point p2) {
    if (p1.is_infinity()) return p2;
    if (p2.is_infinity()) return p1;

    // If x-coordinates are different
    if (normalize(p1.x) != normalize(p2.x)) {
        // Lambda = (y_P2 - y_P1) / (x_P2 - x_P1)
        long long y_diff = p2.y - p1.y;
        long long x_diff = p2.x - p1.x;
        long long lambda = normalize(normalize(y_diff) * modInverse(x_diff));

        // x_R = lambda^2 - x_P1 - x_P2
        long long lambda_sq = lambda * lambda;
        long long xr_val = lambda_sq - p1.x - p2.x;
        long long xr = normalize(xr_val);

        // y_R = lambda*(x_P1 - x_R) - y_P1
        long long term_xP1_minus_xr = p1.x - xr; // xr is already normalized
        long long yr_val = lambda * term_xP1_minus_xr - p1.y;
        long long yr = normalize(yr_val);

        return Point(xr, yr);
    } else { // x-coordinates are the same
        if (normalize(p1.y) == normalize(p2.y)) { // Points are identical
            return point_double(p1);
        } else { // x1=x2, y1!=y2. This implies y1 = -y2 (mod P_MOD)
                 // P1 + (-P1) = Infinity
            return Point();
        }
    }
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    long long a_in, b_in, p_in;
    std::cin >> a_in >> b_in >> p_in;
    A_CURVE = a_in;
    B_CURVE = b_in; // B_CURVE is not used in addition/doubling formulas
    P_MOD = p_in;

    long long px_in, py_in, qx_in, qy_in;
    std::cin >> px_in >> py_in >> qx_in >> qy_in;

    Point P_base(px_in, py_in);
    Point Q_target(qx_in, qy_in);

    // Per problem: if Q is point at infinity (-1,-1), output 0
    if (Q_target.is_infinity()) {
        std::cout << 0 << std::endl;
        return 0;
    }

    // Problem implies P_base is not infinity ("P=(x,y)为椭圆曲线上的整点")

    Point current_multiple_P = P_base; // This is 1*P
    for (int k_val = 1; k_val < (1 << 16); ++k_val) { // k from 1 up to 2^16 - 1
        if (current_multiple_P == Q_target) {
            std::cout << k_val << std::endl;
            return 0;
        }
        // Calculate (k_val+1)*P = (k_val*P) + P
        current_multiple_P = point_add(current_multiple_P, P_base);
    }
    
    // If the loop completes, it means no k in [1, 2^16-1) was found.
    // The problem statement "0 <= k < 2^16" suggests a solution will always be found.
    // This part should ideally not be reached.

    return 0;
}

