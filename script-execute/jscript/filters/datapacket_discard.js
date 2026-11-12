// Task: Pass only every 5th data packet to the export modules; the others are discarded. JScript version.
// Input: Any parsed data packet.
// Output: A COUNTER variable in each packet; 4 of 5 packets discarded.
// Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin
// Source: AGG Software, Script execute plugin samples
// License: MIT, see LICENSE in the repository root

var v1;
var sName = "COUNTER";

{
 // checks that a variable is stored before
 if ( IsVariableStored(sName) )
   // retrieves a stored variable
   v1 = PopVariable(sName);
 else
   // otherwise initialize our counter
   v1 = 0;
 // add or changes a variable in a data packet
 SetVariable(sName, v1+1);
 // stores a value between script executions
 PushVariable(sName, v1+1);

 // the script pass to an export module every 5th data packet only
 if((v1 % 5)!=0)
  DiscardDataPacket();

}
