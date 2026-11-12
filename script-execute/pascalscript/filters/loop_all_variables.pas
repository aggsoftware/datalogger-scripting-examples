{ Task: Walk through all VALUEn variables of a packet (for example MODBUS registers of several posts), create one export row per value that changed since the last packet, classify the value into Stop / Work / Finish and extract a truck number; discard the packet when nothing changed. }
{ Input: A packet with VALUE1..VALUEn integer variables. }
{ Output: Rows with IDPost, IDEvents and IDtruck, one per changed value. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

var i, idx, nTruck, nProcessed: integer;
 sName: string;
 vValue, vPrevValue: integer;
begin
 // loop through all variables in a data packet
 nProcessed := 0;
 for i := 0 to GetVariableCount - 1 do
  begin
   sName := GetVariableNameByIndex(i);
   // process only variables with name like VALUE1, VALUE2, etc.
   if copy(sName, 1, 5) = 'VALUE' then
    begin
     // check that we have a previous value
     if IsVariableStored(sName) then
      vPrevValue := PopVariable(sName)
     else
      vPrevValue := -1;

     vValue := GetVariableByIndex(i);

     // process only if a values changes
     if vPrevValue <> vValue then
      begin
       // save the current value
       PushVariable(sName, vValue);

       // in this example we need to create a new row for each processed value
       if nProcessed > 0 then
        NewRow();

       // process data
       idx := StrToIntDef(copy(sName, 6, 2), 0) + 10;
       SetVariable('IDPost', 'P' + IntToStr(idx));
       nTruck := 0;
       if vValue >= 2000 then
        begin
         SetVariable('IDEvents', 'Finish');
         nTruck := vValue - 2000;
        end
       else if vValue >= 1000 then
        begin
         SetVariable('IDEvents', 'Work');
         nTruck := vValue - 1000;
        end
       else
        begin
         SetVariable('IDEvents', 'Stop');
         nTruck := vValue;
        end;
       SetVariable('IDtruck', nTruck);
       nProcessed := nProcessed + 1;
      end;
    end;
  end;

 // ignore the data packet if nothing changed in incoming data
 if nProcessed = 0 then
  DiscardDataPacket('', true);
end.