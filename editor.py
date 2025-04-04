"""================================================================"""
              #=MODULES FOR PIC SIMULAROR=#
"""================================================================"""
from System.cpu import MAIN
from System.cpu import INST, ADR
cpu = MAIN() 
q = INST()
a = ADR
"""================================================================"""
              #=EDITOR CODE FOR PIC SIMULAROR=#
"""================================================================"""
program = [

    q.MOVLW,    100, # charge 100 dans W
    q.MOVLG,    50, # charge 50 dans G
    q.STOP,     3,
    q.MOVWF,    a.ddr[0], # Tranfert W dans l'adresse 0
    q.MOVGF,    a.ddr[1], # Transfert G dans l'adresse 1
    q.STOP,     3,
    q.MOGF,     a.ddr[0], # charge G avec la valeur de 0
    q.MOVF,     a.ddr[1], # charge W avec la valeur de 1
    q.STOP,     3,
    q.PUSH,     2, # Ecrire la valeur de G dans l'EEPROM
    q.PUSH,     1, # Ecrire la valeur de G dans l'EEPROM
    q.MOVWF,    a.ddr[2],
    q.END,
]
"""================================================================"""
              #=LOADING CODE FOR PIC SIMULAROR=#
"""================================================================"""
cpu.load_program(program)
cpu.run()
