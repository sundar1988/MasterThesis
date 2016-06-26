def script():
    
    helpScript=("To select device: /?select=devicename & setvalue=number\n"
                            "\n"
                            "devicename and setvalue: \n"
                            "-->Street Lamp = streetlamp           setvalue = required Lux\n"      
                            "-->Front Lamp (Down)= frontlampdown   setvalue = required Lux\n"
                            "-->Front Lamp (Up)= frontlampup       setvalue = required Lux\n"
                            "-->Front Lamp (Mid)= frontlampmid     setvalue = required Lux\n"
                            "-->Lamp Right= lampright              setvalue = required Lux\n"
                            "-->Lamp Left= lampleft                setvalue = required Lux\n"
                            "-->Cable Car= cablecar                setvalue = PWM Speed\n"
                            "\n"
                            "-->Cable car rotation Counter = setcounter  setvalue = counter value\n"
                            "\n"
                            "Turn OFF all Lamps:    /lampoff\n"
                            "Read counter value:    /getcountervalue\n"
                            "Reset counter:         /resetcounter\n"
                            "Set RPM counter:       /setrpmcounter\n"
                            "Get RPM value:         /getrpm\n"
                            "Reset RPM counter:     /resetrpm\n")
    return helpScript
