{ Task: Combine the readings of two sensors (DISPLAY=1 and 2) that arrive in separate packets into one packet with VALUE1, UNIT1, VALUE2, UNIT2; ignore sensors 3 and 4; pass the combined packet at most every 10 s. }
{ Input: Packets with DISPLAY, VALUE and UNIT. }
{ Output: One combined packet per 10 s; all other packets discarded. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

// This scripts filteres out values by timeout (10 seconds by default)
// So, all data export plugin will not receive values very often
const
 sTimestampName = 'LASTTIMESTAMP';
 sReceivedFlag = 'RECEIVED_FLAG';
 dtTimeout = 10/86400; // 10 seconds
var
 sDisplay, sName, sFlag, sTmp: string;
 dtNow, dtLast: TDateTime;
 v: variant;
begin
 // incoming data packets contains values for different sensors
 // we need to control each sensor separately
 sDisplay := VarToStr(GetVariable('DISPLAY'));
 
 if (sDisplay = '3') or (sDisplay = '4') then
  begin
   DiscardDataPacket(); // ignore this data packet from some sensors
   exit; // do not execute sequential code
  end;  
  
 // we need to store a last timestamp for each sensor separately
 sName := 'VALUE' + sDisplay;
 v := GetVariable('VALUE'); // gets a value from the current data packet
 PushVariable(sName, v); // save the received value
 sName := 'UNIT' + sDisplay;
 v := GetVariable('UNIT'); 
 PushVariable(sName, v);
 
 sFlag := '00'; // means: nothing received yet
 // check a stored flag
 if IsVariableStored(sReceivedFlag) then
  begin
   sTmp := PopVariable(sReceivedFlag);
   if length(sTmp) = 2 then
    sFlag := sTmp;
  end;
  
 // set a flag of received data for the necessary sensor  
 if (sDisplay = '1') then
  sFlag[1] := '1'
 else if (sDisplay = '2') then
  sFlag[2] := '1';
  
 if sFlag = '11' then
  begin
   // all data received
   PushVariable(sReceivedFlag, '00'); // reset and save flags
   
   // the additional filter by timeout
   dtNow := Now;
   dtLast := 0;
   // restore the previous timestamp for the necessary sensor if it exists
   if IsVariableStored(sTimestampName) then
    dtLast := PopVariable(sTimestampName);
   if (dtNow - dtLast) >= dtTimeout then
    begin
     PushVariable(sTimestampName, dtNow); // store last timestamp for a next call
     // add stored values from previous data packets to the current packet
     SetVariable('VALUE1', PopVariable('VALUE1'));
     SetVariable('UNIT1', PopVariable('UNIT1'));
     SetVariable('VALUE2', PopVariable('VALUE2'));
     SetVariable('UNIT2', PopVariable('UNIT2'));
     exit; // exit and allow to process this data packet
    end; 
  end
 else
  PushVariable(sReceivedFlag, sFlag); // save the flags state
  
 // ignore the current (last received) data packet
 DiscardDataPacket();
end.