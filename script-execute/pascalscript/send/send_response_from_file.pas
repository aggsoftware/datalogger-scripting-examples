{ Task: Answer the command renew from a TCP or UDP client by streaming the file C:\Files\<data source>\data.bin to it in 1 KB blocks, then delete the file. }
{ Input: Packets with CMD and DATA_SOURCE_NAME (ASCII parser). }
{ Output: The file contents sent to the client; the command packet discarded. }
{ Product: Advanced Serial Data Logger, Advanced TCP/IP Data Logger, Data Logger Suite and the other AGG data loggers with the Script execute plugin }
{ Source: AGG Software, Script execute plugin samples }
{ License: MIT, see LICENSE in the repository root }

{*******************************************}
{ Example:                                  }
{ sending a file in a response to a command }
{ for tcp or udp client                     }
{*******************************************}

const
    data_block_size = 1024;
var cmd, file_name, data_packet: string;
    fs: TFileStream;
    nSize: integer;
begin
 if IsVariableDefined('CMD') and
    IsVariableDefined('DATA_SOURCE_NAME') then
  begin
   // retrieves a parser variable
   cmd := GetVariable('CMD');
   if cmd = 'renew' then
    begin
     DiscardDataPacket();
     file_name := 'C:\Files\'+GetVariable('DATA_SOURCE_NAME')+'\data.bin';
     if FileExists(file_name) then
      try
       fs := TFileStream.Create(file_name, fmOpenRead);
       try
        repeat
         SetLength(data_packet, data_block_size);
         nSize := fs.Read(data_packet, data_block_size);
         if nSize>0 then
          begin
           SetLength(data_packet, nSize);
           SendString(data_packet);
          end
         else
          break;
        until false;
       finally
        fs.Free;
       end;
       DeleteFile(file_name);
      except
      end;
    end;
  end;
end.