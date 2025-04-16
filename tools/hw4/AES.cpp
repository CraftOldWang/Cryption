// 写了python 的版本， 使用gpt 转换成C++的
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>
#include <cstdio>
#include <iomanip>

// S-box
const unsigned char sbox[256] = {
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
};

// Rcon (only the high byte is used in AES)
const unsigned char rcon[11] = {
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
};

// Helper function to convert hex string to bytes
std::vector<unsigned char> hex_to_bytes(const std::string& hex) {
    std::vector<unsigned char> bytes;
    for (size_t i = 0; i < hex.length(); i += 2) {
        std::string byteString = hex.substr(i, 2);
        unsigned char byte = static_cast<unsigned char>(std::stoi(byteString, nullptr, 16));
        bytes.push_back(byte);
    }
    return bytes;
}

// Helper function to convert bytes to hex string
std::string bytes_to_hex(const std::vector<unsigned char>& bytes) {
    std::string hex;
    for (unsigned char byte : bytes) {
        char buf[3];
        std::sprintf(buf, "%02X", byte);
        hex += buf;
    }
    return hex;
}

// Key Expansion
std::vector<unsigned char> KeyExpansion(const std::string& Orig_Key) {
    std::vector<unsigned char> key = hex_to_bytes(Orig_Key);
    std::vector<unsigned char> w(44 * 4); // 44 words, each 4 bytes
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            w[i * 4 + j] = key[i * 4 + j];
        }
    }
    for (int i = 4; i < 44; ++i) {
        std::vector<unsigned char> temp(4);
        for (int j = 0; j < 4; ++j) {
            temp[j] = w[(i - 1) * 4 + j];
        }
        if (i % 4 == 0) {
            // RotWord
            unsigned char t = temp[0];
            temp[0] = temp[1];
            temp[1] = temp[2];
            temp[2] = temp[3];
            temp[3] = t;
            // SubWord
            for (int j = 0; j < 4; ++j) {
                temp[j] = sbox[temp[j]];
            }
            // XOR with Rcon
            temp[0] ^= rcon[i / 4];
        }
        for (int j = 0; j < 4; ++j) {
            w[i * 4 + j] = w[(i - 4) * 4 + j] ^ temp[j];
        }
    }
    return w;
}

// Add Round Key
std::vector<unsigned char> AddRoundKey(const std::vector<unsigned char>& State, const std::vector<unsigned char>& RoundKey) {
    std::vector<unsigned char> result(16);
    for (int i = 0; i < 16; ++i) {
        result[i] = State[i] ^ RoundKey[i];
    }
    return result;
}

// SubBytes
std::vector<unsigned char> SubBytes(const std::vector<unsigned char>& State) {
    std::vector<unsigned char> result(16);
    for (int i = 0; i < 16; ++i) {
        result[i] = sbox[State[i]];
    }
    return result;
}

// ShiftRows
std::vector<unsigned char> ShiftRows(const std::vector<unsigned char>& State) {
    std::vector<unsigned char> result(16);
    // Row 0: no shift
    result[0] = State[0];
    result[4] = State[4];
    result[8] = State[8];
    result[12] = State[12];
    // Row 1: left shift by 1
    result[1] = State[5];
    result[5] = State[9];
    result[9] = State[13];
    result[13] = State[1];
    // Row 2: left shift by 2
    result[2] = State[10];
    result[6] = State[14];
    result[10] = State[2];
    result[14] = State[6];
    // Row 3: left shift by 3
    result[3] = State[15];
    result[7] = State[3];
    result[11] = State[7];
    result[15] = State[11];
    return result;
}

// Galois Field multiplication
unsigned char gf_mul(unsigned char a, unsigned char b) {
    unsigned char p = 0;
    for (int i = 0; i < 8; ++i) {
        if (b & 1) {
            p ^= a;
        }
        bool hi_bit_set = a & 0x80;
        a = (a << 1) & 0xFF;
        if (hi_bit_set) {
            a ^= 0x1B; // Reduction modulo polynomial
        }
        b >>= 1;
    }
    return p;
}

// MixColumns
std::vector<unsigned char> MixColumns(const std::vector<unsigned char>& State) {
    std::vector<unsigned char> result(16);
    for (int c = 0; c < 4; ++c) {
        unsigned char t[4];
        for (int i = 0; i < 4; ++i) {
            t[i] = State[c * 4 + i];
        }
        result[c * 4 + 0] = gf_mul(2, t[0]) ^ gf_mul(3, t[1]) ^ t[2] ^ t[3];
        result[c * 4 + 1] = t[0] ^ gf_mul(2, t[1]) ^ gf_mul(3, t[2]) ^ t[3];
        result[c * 4 + 2] = t[0] ^ t[1] ^ gf_mul(2, t[2]) ^ gf_mul(3, t[3]);
        result[c * 4 + 3] = gf_mul(3, t[0]) ^ t[1] ^ t[2] ^ gf_mul(2, t[3]);
    }
    return result;
}

// AES-128 Encryption
std::string AES128_Encrypt(const std::string& x, const std::string& K) {
    std::vector<unsigned char> State = hex_to_bytes(x);
    std::vector<unsigned char> expanded_key = KeyExpansion(K);
    // Extract round keys
    std::vector<std::vector<unsigned char>> RoundKeys(11, std::vector<unsigned char>(16));
    for (int i = 0; i < 11; ++i) {
        for (int j = 0; j < 16; ++j) {
            RoundKeys[i][j] = expanded_key[i * 16 + j];
        }
    }
    // Initial round key addition
    State = AddRoundKey(State, RoundKeys[0]);
    // 9 rounds
    for (int i = 1; i < 10; ++i) {
        State = SubBytes(State);
        State = ShiftRows(State);
        State = MixColumns(State);
        State = AddRoundKey(State, RoundKeys[i]);
    }
    // Final round
    State = SubBytes(State);
    State = ShiftRows(State);
    State = AddRoundKey(State, RoundKeys[10]);
    // Convert back to hex string
    return bytes_to_hex(State);
}

int main() {

    std::string x;
    std::string K;
    std::cin>>K >>x;

    // std::string x = "00112233445566778899aabbccddeeff";
    // std::string K = "000102030405060708090a0b0c0d0e0f";
    std::string y = AES128_Encrypt(x, K);
    std::cout << y << std::endl;
    return 0;
}