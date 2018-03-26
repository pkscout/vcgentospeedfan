# *  Credits:
# *
# *  v.0.1.0
# *  original VCGenCMD to SpeedFan Log code by pkscout

import atexit, datetime, os, random, sys, time
import data.config as config
from resources.common.xlogger import Logger
from resources.common.fileops import deleteFile, writeFile
from resources.common.transforms import replaceWords

p_folderpath, p_filename = os.path.split( os.path.realpath(__file__) )
lw = Logger( logfile = os.path.join( p_folderpath, 'data', 'logfile.log' ),
             numbackups = config.Get( 'logbackups' ), logdebug = str( config.Get( 'debug' ) ) )

def _deletePID():
    success, loglines = deleteFile( pidfile )
    lw.log (loglines )

pid = str(os.getpid())
pidfile = os.path.join( p_folderpath, 'data', 'create.pid' )
atexit.register( _deletePID )


class Main:
    def __init__( self ):
        self._setPID()
        self._init_vars()
        self._create_speedfan_log()
        
                
    def _setPID( self ):
        basetime = time.time()
        while os.path.isfile( pidfile ):
            time.sleep( random.randint( 1, 3 ) )
            if time.time() - basetime > config.Get( 'aborttime' ):
                err_str = 'taking too long for previous process to close - aborting attempt'
                lw.log( [err_str] )
                sys.exit( err_str )
        lw.log( ['setting PID file'] )
        success, loglines = writeFile( pid, pidfile, wtype='w' )
        lw.log( loglines )        


    def _init_vars( self ):
        self.DATAROOT = os.path.join( p_folderpath, 'data' )
        self.MAPPINGS = config.Get( 'mappings' )
        self.STRIPTEXT = config.Get( 'striptext' )
        self.MINLINES = config.Get( 'minlines' )


    def _create_speedfan_log( self ):
        log_name = os.path.join( self.DATAROOT, 'SFLog%s.csv' % datetime.datetime.now().strftime("%Y%m%d") )
        header = 'Seconds'
        data_row = '12345'
        for mapping in self.MAPPINGS:
            output = os.popen("/opt/vc/bin/vcgencmd %s" % mapping[1]).readline().strip()
            lw.log( ['got %s from vcgencmd' % output] )
            num_output = replaceWords( output, self.STRIPTEXT )
            header = header + '\t' + mapping[0]
            data_row = data_row + '\t' + num_output
        file_text = header
        for x in range( 0, self.MINLINES):
            file_text = file_text + '\n' + data_row
        success, loglines = writeFile( file_text, log_name, wtype='w' )
        lw.log( loglines )



if ( __name__ == "__main__" ):
    lw.log( ['script started'], 'info' )
    Main()
lw.log( ['script finished'], 'info' )