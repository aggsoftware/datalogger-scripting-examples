{ Task: Add BATCH_NO, PARAMETER and AREA to every packet from the first row of a CSV file that an operator maintains. }
{ Input: C:\Logs\Text File.csv, first row: batch,parameter,area. }
{ Output: Three new variables in every packet. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

{*******************************************}
{ Example:                                  }
{ adds new variables from the first row of  }
{ a CSV file                                }
{*******************************************}

const
   file_name = 'C:\Logs\Text File.csv';
var s, s2: string;
    n1, n2: integer;
    sl: TStringList;
begin
 if FileExists(file_name) then
  try
   sl := TStringList.Create;
   try
    sl.LoadFromFile(file_name);
    if sl.Count > 0 then // check that the file is not empty
     begin
      s := sl[0];
      n1 := pos(',', s);
      if n1 > 0 then
       begin
        n2 := posex(',', s, n1 + 1);
        s2 := copy(s, 1, n1 - 1);
       end
      else
       begin
        n2 := 0;
        s2 := s;
       end;
      SetVariable('BATCH_NO', s2);
              
      if n2 > 0 then
       begin
        s2 := copy(s, n1 + 1, n2 - n1 - 1);
        SetVariable('PARAMETER', s2);
        s2 := copy(s, n2 + 1, length(s));
        SetVariable('AREA', s2);
       end
      else if n1 > 0 then
       begin
        s2 := copy(s, n1 + 1, length(s));
        SetVariable('PARAMETER', s2);
       end;
     end;
   finally
    sl.Free;
   end;
  except
  end;
end.