{ Task: Rate-limit a device that reports several sensors: pass a packet from sensor DISPLAY=n only when 10 seconds have passed since the last packet of that sensor. }
{ Input: Packets with the variables DISPLAY and VALUE. }
{ Output: Packets at most every 10 s per sensor; the rest discarded. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

// This scripts filteres out values by timeout (10 seconds by default)
// So, all data export plugin will not receive values very often
const
 sPrefix = 'LASTTIMESTAMP';
 dtTimeout = 10/86400; // 10 seconds
var
 sDisplay, sName: string;
 dtNow, dtLast: TDateTime;
begin
 // incoming data packets contains values for different sensors
 // we need to control each sensor separately
 sDisplay := VarToStr(GetVariable('DISPLAY')); 

 // we need to store a last timestamp for each sensor separately
 sName := sPrefix + sDisplay;

 dtNow := Now;
 dtLast := 0;
 // restore the previous timestamp for the necessary sensor if it exists
 if IsVariableStored(sName) then
  dtLast := PopVariable(sName);
 if (dtNow - dtLast) < dtTimeout then
  DiscardDataPacket() // ignore this data packet
 else
  PushVariable(sName, dtNow); // store last timestamp for a next call
end.