// Task: If any of ITEM1..ITEM9 is True, send a text line with the time stamp, MODBUS_DESC and the value to COM1; otherwise discard the packet.
// Input: A packet from the MODBUS parser with ITEMn boolean variables.
// Output: Lines on COM1 for true items; packets without a true item discarded.
// Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin
// Source: AGG Software, Script execute plugin samples
// License: MIT, see LICENSE in the repository root

/*
 Redirect a data packet to COM1 if one of "ITEM1..ITEM10" 
 parser variables has the boolean "True" value
 In all other cases, discard a data packet
*/
int i;
string name;
string data;
variant v;
bool bCanDiscard;
{
  bCanDiscard = true;
  for(i = 1; i < 10; i++)
  {
    name = "ITEM" + IntToStr(i);
    if (IsVariableDefined(name))
    {
      v = GetVariable(name);
      if (v)
      {
        data = VarToStr(GetVariable("DATE_TIME_STAMP")) + " " +
         VarToStr(GetVariable("MODBUS_DESC")) + " " +
         VarToStr(v) +
         CHR(13) + CHR(10);
        SendDataToDataSource("COM1", data);
        bCanDiscard = false;
      }
    }
  }
  if (bCanDiscard)
  {
    DiscardDataPacket();
  }
}
