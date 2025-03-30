"""================================================================"""
              #=MODULES FOR PIC SIMULAROR=#
"""================================================================"""
from System.cpu import MAIN
from System.cpu import INST, ADR, PORT
cpu = MAIN() 
port = PORT()
q = INST()
a = ADR
"""================================================================"""
              #=EDITOR CODE FOR PIC SIMULAROR=#
"""================================================================"""
program = [

    q.MOVLW, 99,
    q.MOVWF, port.A[0]*5,
    q.MOVLW, 0,
    q.MOVF,  port.A[4],
    q.END
]
"""================================================================"""
              #=LOADING CODE FOR PIC SIMULAROR=#
"""================================================================"""
cpu.load_program(program)
cpu.run()
