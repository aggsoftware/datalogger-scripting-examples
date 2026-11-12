{ Task: Make sure the variables NAME1, NAME2 and NAME3 exist in every packet, so that export modules always get the same columns. }
{ Input: Any packet. }
{ Output: Missing variables added with an empty value. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

const
 // list of names
 sName = 'NAME1;NAME2;NAME3';
var
 i, j: integer;
 sl: TStringList;
begin
 sl := TStringList.Create;
 try
  sl.Text := AnsiReplaceStr(sName, ';', Chr(13));
  // check all variables in loop
  for i:=0 to sl.Count-1 do
   begin
    if not IsVariableDefined(sl[i]) then
     begin
      // set an empty variable value 
      // if the variable does not exist in the received data packet
      SetVariable(sl[i], '');
     end;
   end;
 finally
  sl.Free;
 end;
end.