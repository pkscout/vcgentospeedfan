#SpeedFan log file header names mapped to vcgencmd options
#SpeedFan log must have at least 2 columns or it won't work
mappings = ( ('Core.temp', 'measure_temp'),
             ('SDRAM_C.voltage', 'measure_volts sdram_c'),
             ('SDRAM_I.voltage', 'measure_volts sdram_i'),
             ('SDRAM_P.voltage', 'measure_volts sdram_p') )

#text from the vcgencmd output that should be stripped
striptext = { 'temp=' : '',
              '\'C' : '',
              'volt=': '',
              'V': '' }
              
#the SpeedFan log file has to be a minimum number of lines to be read correctly
minlines = 20

#if another instance of script is running, amount of time (in seconds) to wait before giving up
aborttime = 30

#number of script logs to keep
logbackups = 1

#for debugging you can get a more verbose log by setting this to True
debug = False

