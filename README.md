# Data logger scripting examples

Ready-to-load scripts for the two programmable modules of the AGG Software data loggers: the **Script execute** plugin (PascalScript, C++Script, JScript, BasicScript) and the **Python plugin**. Every file starts with the same header: what the script does, what data it expects, what comes out, and which products run it.

Used with [Advanced Serial Data Logger](https://www.aggsoft.com/serial-data-logger.htm), [Advanced TCP/IP Data Logger](https://www.aggsoft.com/tcpip-data-logger.htm), [Data Logger Suite](https://www.dataloggersuite.com/) and the other loggers of the family. Plugin pages: [Script execute](https://www.aggsoft.com/data-logger-plugins/scriptexec.htm).

## Layout

```
script-execute/
  pascalscript/   filters/ extract/ files/ send/ state/
  cppscript/      filters/ send/
  jscript/        filters/
  basicscript/    filters/
python-plugin/
  parser/ filters/ export/ events/ query/ api/
```

## Script execute: how to load a script

1. In the logger, open the configuration, **Modules**, **Data filter**, and add **Script execute**.
2. Choose the language of the file and paste the script, or load the file.
3. The script runs once per data packet. Parser variables are read with `GetVariable`, changed or added with `SetVariable`, and a packet is dropped with `DiscardDataPacket`.

Functions used by the examples:

| Function | Purpose |
|---|---|
| `GetVariable(name)`, `SetVariable(name, value)` | read or write a variable of the current packet |
| `IsVariableDefined(name)`, `IsVariableDefinedValid(name)` | check that a variable exists (and holds a valid value) |
| `GetVariableCount`, `GetVariableNameByIndex(i)`, `GetVariableByIndex(i)` | walk through all variables |
| `PushVariable(name, value)`, `PopVariable(name)`, `IsVariableStored(name)`, `DeleteVariable(name)` | keep values between script runs |
| `DiscardDataPacket` | drop the current packet before export |
| `NewRow` | start a new export row inside one packet |
| `SendString`, `SendByte`, `SendData` | send bytes back to the data source |
| `SendDataToDataSource(name, data)` | send bytes to another data source, for example `COM1` |
| `DbgLog(text, level)` | write to the program log (0 error, 1 warning, 2 info) |

## Script execute examples

| File | Task |
|---|---|
| pascalscript/filters/datapacket_discard.pas | pass only every 5th packet (also in cppscript, jscript, basicscript) |
| pascalscript/filters/filter_out_value_by_timeout.pas | per-sensor rate limit, one packet per 10 s |
| pascalscript/filters/aggregate_and_filter_out_data.pas | combine two sensors' packets into one, then rate-limit |
| pascalscript/filters/loop_all_variables.pas | one export row per changed VALUEn, with Stop/Work/Finish classification |
| pascalscript/filters/check_variable_and_set_alarm_status.pas | night-time drift alarm on one tag |
| pascalscript/filters/check_variable_defined.pas | guarantee that NAME1..NAME3 exist in every packet |
| pascalscript/state/pop_push.pas | a counter kept between runs |
| pascalscript/extract/extract_text_between_signatures.pas | text between two signatures into a new variable |
| pascalscript/extract/extract_xml_tag_data.pas | repeated XML blocks into VALUEn |
| pascalscript/files/add_variables_from_csv_file.pas | batch data from the first row of a CSV file |
| pascalscript/files/create_overwrite_xml_file.pas | scoreboard XML rewritten on every packet |
| pascalscript/send/send_data.pas | the three output calls |
| pascalscript/send/send_response_from_file.pas | stream a file to a TCP/UDP client on command |
| cppscript/send/csv_string_parse_and_redirect.cpp | $ROV line to a $GPHDT NMEA sentence with checksum, sent to COM1 |
| cppscript/send/datapacket_redirect_or_discard.cpp | forward a line to COM1 when a MODBUS flag is true, else discard |

## Python plugin: how to load a script

1. Install the Python plugin and Python 3 on the logging PC.
2. Add the plugin as a parser, a filter, an export module or an event handler, depending on which function the script implements, and point it at the file.
3. The script implements `ParseData`, `FilterData`, `ExportData` or `EventData`; `main()` runs once when the plugin loads.

| File | Task |
|---|---|
| parser/parser_ascii_data.py | parse `<STX>v1;v2;v3<ETX>` packets (sample bytes in parser_ascii_data.sample.txt) |
| filters/filter_iterate_rows.py | the skeleton of a row-based filter |
| filters/filter_new_list.py | build a new outgoing list |
| filters/filter_replace_variable_in_list.py | replace one item in every row |
| export/export_create_csv.py | daily CSV file with selected columns |
| export/export_insert_to_mysql.py | insert rows into MySQL |
| events/event_by_timer.py | raise a custom event every 5 s |
| events/event_send_email.py | email when a packet contains a given text (here " 911") |
| query/query_send_request_by_event.py | send a request once the port is open |
| query/query_send_request_periodically.py | send a request every 5 s from a timer thread |
| api/plugin_functions_demo.py | every plugin API call in one file |

## Contributing

Send a pull request with one script per task, the same six-line header, and no customer data in the examples. Questions about the API go to support@aggsoft.com.

## License

MIT. Copyright AGG Software.
