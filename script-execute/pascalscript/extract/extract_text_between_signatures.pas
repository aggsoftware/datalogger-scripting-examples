{ Task: Extract the text between two signatures, here the number after "value": in a JSON fragment, into a new variable. }
{ Input: VALUE1 containing a JSON fragment. }
{ Output: VALUE2 with the extracted text. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

// Returns an empty string if one of the signatures is not found.
// Extracts the first occurrence only.
function ExtractBetween(const S, StartSig, EndSig: string): string;
var
  StartPos, EndPos: Integer;
begin
  Result := '';
  StartPos := Pos(StartSig, S);
  if StartPos = 0 then Exit;

  StartPos := StartPos + Length(StartSig);
  EndPos := Pos(EndSig, Copy(S, StartPos, 65535));
  if EndPos = 0 then Exit;

  Result := Copy(S, StartPos, EndPos - 1);
end;

var
 s1, s2: string;

begin
 s1 := GetVariable('VALUE1'); // gets a value from the current data packet
 s2 := ExtractBetween(s1, '"value":', '}');
 SetVariable('VALUE2', s2); // store the extracted value into a new variable
end.
