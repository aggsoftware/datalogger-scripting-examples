{ Task: Write a scoreboard XML file (clock, period, scores, fouls, shot clock) from the parser variables on every packet, overwriting the file each time, for example for a video overlay. }
{ Input: Variables TIME, PERIOD, SCORE_HOME, SCORE_GUEST, FOUL_HOME, FOUL_GUEST, SHOT_CLOCK. }
{ Output: c:\logs\my.xml rewritten on every packet. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

const
 filename = 'c:\logs\my.xml';
var
 text, crlf, s: string;
 v: variant;
 fs: TFileStream;
begin
 crlf := chr(13) + chr(10);
 s := GetVariable('TIME');
 Insert('.', s, 3);
 text := '<scoreboard>' + crlf +
  '<clock>' + trim(s) + '</clock>' + crlf;

 s := GetVariable('PERIOD');
 if s = '1' then
  s := s + 'st'
 else if s = '2' then
  s := s + 'nd'
 else if s = '3' then
  s := s + 'rd'
 else if (s = '4') or (s = '5') or (s = '6') or (s = '7') or (s = '8') then
  s := s + 'th'
 else if (s = '9') then
  s := s + 'tn'
 else if (s = '0') then
  s := s + 'OT';

 text := text +  '<period>' + s + '</period>' + crlf;

 s := trim(GetVariable('SCORE_HOME'));
 text := text +  '<homescore>' + s + '</homescore>' + crlf;

 s := trim(GetVariable('SCORE_GUEST'));
 text := text +  '<awayscore>' + s + '</awayscore>' + crlf;

 s := trim(GetVariable('FOUL_HOME'));
 text := text +  '<homefoul>' + s + '</homefoul>' + crlf;

 s := trim(GetVariable('FOUL_GUEST'));
 text := text +  '<awayfoul>' + s + '</awayfoul>' + crlf;

 s := trim(VarToStr(GetVariable('SHOT_CLOCK')));
 text := text +  '<shootclock>' + s + '</shootclock>' + crlf;

 text := text + '</scoreboard>';

 fs := TFileStream.Create(filename, fmCreate);
 try
  fs.Write(text, length(text));
 finally
  fs.Free;
 end;

end.