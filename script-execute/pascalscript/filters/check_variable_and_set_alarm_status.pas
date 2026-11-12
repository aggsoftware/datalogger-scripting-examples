{ Task: Outside working hours (18:30 to 07:30) watch one tag and raise an alarm when its value drifts by 1 or more from the value at the start of the quiet period. }
{ Input: A packet with the tag Node1.sensor_presure.Tag1 (OPC or MODBUS parser). }
{ Output: ALARM1 = A or N and ALARM2 = 1 or 0 added to the packet; messages in the program log. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

const
 tag_name = 'Node1.sensor_presure.Tag1';
 tag_alarm1 = 'ALARM1';
 tag_alarm2 = 'ALARM2';
 tag_check_started = 'CHECK_STARTED';
var
 v, v0: double;
 alarm: boolean;
 check_alarm: boolean;
 data: string;
 dt, dt1, dt2: TDateTime;

begin
 if not IsVariableDefinedValid(tag_name) then
  exit;

 alarm := false;

 v := GetVariable(tag_name);

 dt := Frac(Now);
 dt2 := EncodeTime(18, 30, 0, 0);
 dt1 := EncodeTime(7, 30, 0, 0);

 check_alarm := not ((dt > dt1) and (dt < dt2));
 if check_alarm then
  begin
   if not IsVariableStored(tag_check_started) then
    begin
     PushVariable(tag_check_started, v);
     v0 := v;
    end
   else
    v0 := PopVariable(tag_check_started);

   alarm := abs(v0 - v) >= 1;
  end
 else
  DeleteVariable(tag_check_started);

 DbgLog('Checking alarm: ' + BoolToStr(check_alarm), 2);
 DbgLog('Alarm state: ' + BoolToStr(alarm), 2);

 if alarm then
  begin
   SetVariable(tag_alarm1, 'A');
   SetVariable(tag_alarm2, 1);
   DbgLog('Sending alarm', 1);
  end
 else
  begin
   SetVariable(tag_alarm1, 'N');
   SetVariable(tag_alarm2, 0);
  end;
end.