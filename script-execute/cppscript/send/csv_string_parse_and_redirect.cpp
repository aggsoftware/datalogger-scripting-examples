// Task: Turn a proprietary $ROV,heading,... line into a standard $GPHDT NMEA sentence with a checksum and send it to COM1. Written without bitwise operators, which the script engine lacks.
// Input: FULL_DATA_PACKET like $ROV,185.2,-4.4,2.1,566,checksum.
// Output: $GPHDT,185.2,T*hh sent to the data source COM1.
// Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin
// Source: AGG Software, Script execute plugin samples
// License: MIT, see LICENSE in the repository root

// ---------------------------------------------------------------------------
// ASDL Script Plugin - NO bitwise operators, NO STL, NO includes
// Reads: $ROV,185.2,-4.4,2.1,566,checksum
// Extracts 2nd value as heading
// Outputs: $GPHDT,185.2,T*CS
// ---------------------------------------------------------------------------

// Compute NMEA0183 checksum without bitwise operators
String ComputeChecksum(String s)
{
    int chk = 0;
    int i = 1;

    // XOR implemented manually without ^ operator
    while (i <= Length(s))
    {
        int c = Ord(s[i]);

        // XOR = (A + B) - 2 * (A AND B)
        // Since AND is not allowed, emulate XOR with bit rules:
        // incrementally recompute bit-by-bit using arithmetic only

        int bit = 1;
        int newChk = 0;

        int a = chk;
        int b = c;

        while (bit <= 128)   // process 8 bits
        {
            int abit = trunc(a / bit) % 2;
            int bbit = trunc(b / bit) % 2;

            // XOR truth table implemented via addition/comparison
            int xbit = 0;
            if (((abit == 1) && (bbit == 0)) || ((abit == 0) && (bbit == 1)))
                xbit = 1;

            newChk = newChk + (xbit * bit);
            bit = bit * 2;
        }

        chk = newChk;
        i = i + 1;
    }

    // Convert checksum to *HH format using arithmetic only
    int high = trunc(chk / 16);
    int low  = trunc(chk % 16);

    String res = "*";

    if (high < 10) res = res + Chr(high + 48);
    else res = res + Chr(high + 55);

    if (low < 10) res = res + Chr(low + 48);
    else res = res + Chr(low + 55);

    return res;
}

// Extract a comma-separated field without STL
String GetField(String s, int fieldNum)
{
    int i = 1;
    int current = 1;
    int start = 1;

    while (i <= Length(s))
    {
        if (copy(s, i, 1) == ",")
        {
            if (current == fieldNum)
                return copy(s, start, i - start);

            current = current + 1;
            start = i + 1;
        }
        i = i + 1;
    }

    // last field
    if (current == fieldNum)
        return copy(s, start, Length(s) - start + 1);

    return "";
}

// ---------------------------------------------------------------------------
// ASDL event: called when new data arrives from COM1
// ---------------------------------------------------------------------------
{
    // Extract 2nd field - heading
    String line = GetVariable("FULL_DATA_PACKET");
    String headingStr = GetField(line, 2);

    if (headingStr == "")
    {
        DbgLog("No heading found in: " + line, 1);
    }
    else
    {
      // Build body (no checksum yet)
      String body = "GPHDT," + headingStr + ",T";

      // Add NMEA checksum
      String crc = ComputeChecksum(body);
      String nmea = "$" + body + crc + Chr(13) + Chr(10);
      //DbgLog("CRC: " + crc, 1);

      SendDataToDataSource("COM1", nmea);
    }
}