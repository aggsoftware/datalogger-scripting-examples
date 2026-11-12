{ Task: Parse repeated <Label_><counter>n</counter><data>x</data></Label_> blocks of an XML packet into VALUEn variables. }
{ Input: FULL_DATA_PACKET with the XML text. }
{ Output: VALUE1, VALUE2, ... one per block. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

var
 i, i1, i2: integer;
 dp, s, s1, s2: string;
 
function ExtractBetween(const AData, AName: string): string;
var
 i, i1, i2: integer;
begin
  Result := '';
  i1 := posex('<' + AName + '>', AData, 1);
  if i1 <= 0 then
   exit;
  i1 := i1 + length(AName) + 2;
  i2 := posex('</' + AName + '>', AData, i1);
  if i2 <= 0 then
   exit;
  Result := copy(AData, i1, i2 - i1);
end;
 
begin
 dp := GetVariable('FULL_DATA_PACKET');
 i := 1;
 repeat
  i1 := posex('<Label_', dp, i);
  if i1 <= 0 then
   break;
  i2 := posex('</Label_>', dp, i1 + 6);
  if i2 <= 0 then
   break;
  s := copy(dp, i1, i2 - i1 + 8);
  s1 := ExtractBetween(s, 'counter');
  s2 := ExtractBetween(s, 'data');
  SetVariable('VALUE' + s1, s2);
  i := i2 + 8;
 until false;
end.