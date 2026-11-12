{ Task: Send data back to the data source: SendString, SendByte and SendData, chosen by a counter, to show the three output calls. }
{ Input: Any packet. }
{ Output: Bytes written to the port or socket the packet came from. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

var v1:integer;
    sName:string = 'COUNTER';
begin
 // checks that a variable is stored before
 if IsVariableStored(sName) then
   // retrieves a stored variable
   v1 := PopVariable(sName)
 else
   // otherwise initialize our counter
   v1 := 0;
 // add or changes a variable in a data packet
 SetVariable(sName, v1+1);
 // stores a value between script executions
 PushVariable(sName, v1+1);

 // the script pass to an export module only every 5th data packet
 if (v1 mod 5)=1 then
  SendString('Test')
 else if (v1 mod 5)=2 then
  SendString(#01+'Test'+#02)
 else if (v1 mod 5)=3 then
  SendString(#00+'Test'+#00)
 else if (v1 mod 5)=4 then
  SendByte($FF)
 else if (v1 mod 5)=0 then
  begin
   sName := chr(v1);
   SendData(sName);
  end;

end.
