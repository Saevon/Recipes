#define A_SEXTET   0x11111100
#define B_SEXTET_1 0x00000011
#define B_SEXTET_2 0x11110000
#define C_SEXTET_1 0x00001111
#define C_SEXTET_2 0x11000000
#define D_SEXTET_1 0x00111111



/*
* Converts an array/struct of 3 chars (bytes) to 4 chars
*    split into the individual hextet values (but stored as bytes)
*/
inline sextet_to_char(const char &in_stream, char &out_stream) {
    out_stream[0] = (in_stream[0] & A_SEXTET) >> 2;
    out_stream[1] = in_stream[0] & B_SEXTET_1) << 4) + (in_stream[1] & B_SEXTET_2) >> 4;
    out_stream[2] = in_stream[1] & C_SEXTET_1) << 2) + (in_stream[2] & C_SEXTET_2) >> 2;
    out_stream[3] = in_stream[0] & D_SEXTET_1;
}


/*
* Converts an array of hextet encoded bytes
*   to a longer array of bytes
*
* WARNING! does not handle the end padding with ==
*/
void sextets_to_chars(const char &in_stream, char &out_stream, uint len) {
    for (uint i=0; i <= len; i += 3) {
        sextet_to_char(in_stream, out_stream);
    }
}

