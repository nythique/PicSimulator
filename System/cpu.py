import json, time
class MAIN:
    def __init__(self):
        self.memoryData = [0] * 128 # Memoire de données (2048 bits => 256 Octets => 0.25 Ko).
        self.memoryProgram = [0] * 128 # Memoire de program (1024 bits => 128 Octets => 0.13 Ko).
        self.running = False # Gestionnaire de l'état de marche du cpu (shutdown / END).
        self.w = 0 # Registre accumulateur qui represente la memoire de travaille1 (La RAM1).
        self.g = 0 # Registre accumulateur qui represente la memoire de travaille2 (La RAM2).
        self.cp = 0 # Compteur de programme, qui pointe l'instructio en cours (Idicateur d'instruction à executer).
        """ BANQUE MEMOIRE DE SAUVEGARDE PERMANANT (EEPROM) """
        self.eeprom = self.memoryData[:7]
        ''' REPECTOIRE DES LIGNES DE PORTS'''
        self.A = [0] * 5 # Cinq (3) lignes d'adresses pour le  ports A
        self.B = [0] * 8 # huite (8) lignes d'adresses pour le ports B
   
    def load_program(self, program): 
        """charge un programme en memoire en reservant les 64 premieres cases pour les instructions"""
        if len(program) > 64:
            raise ValueError("Error(19): La tailles du program est superieure à l'espaces réservé (64 Octets).")
        self.memoryProgram[:len(program)] = program # Chargement du program dans la memoire de program.
        self.cp = 0 # Reinitialiser le compteur de programme (Mise à zero).
    
    def run(self):
         """" Execution du program """
         self.running = True # Demarrage du cpu.
         print("\033[92m============================================================\n\033[0m")
         print("\033[92m============>            EXECUTION            <===============\n\033[0m")
         print("\033[92m<============================================================>\n\033[0m")
         while self.running:
            opcode = self.memoryProgram[self.cp] # Recuperation des instructions du program une par une (avec OpCode).

            if opcode == 1: # MOVLW, Instruction de transfert d'une données dans l'accumulateur (W).
                self.cp += 1 # Attente d'une valeur (W).
                self.w = self.memoryProgram[self.cp]
                print(f"\033[94m Chargement de la valeur {self.w} à l'adresse(RAM1) {self.cp}.\033[0m")

            elif opcode == 2: # MOVWF, Instruction de transfert de la données de l'accumulateur (w) à une adresse (Precise).
                self.cp +=1 # Attente d'une valeur (adresse en decimal).
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(43): Address memoire invalide {address}.")
                self.memoryData[address] = self.w
                print(f"\033[94m Ecriture de la valeur chargée dans la RAM1 à l'adresse {address}.\033[0m")

            elif opcode == 3: # MOVF, Instruction de transfert d'une donnée d'une adress dans la memoire de travail (W).
                self.cp += 1 # Attente d'une valeur (adresse en decimal)
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(51): Adresse memoire invalide {address}.")
                self.w = self.memoryData[address]
                print(f"\033[94m Recharge la RAM1 avec la valeur ({self.w}) charger à l'adresse {address}.\033[0m")

            elif opcode == 4: # MOVLG, Instruction de transfert d'une données dans l'accumulateur (G).
                self.cp += 1 # Attente d'une valeur (G).
                self.g = self.memoryProgram[self.cp]
                print(f"\033[94m Chargement de la valeur {self.g} à l'adresse(RAM2) {self.cp}.\033[0m")

            elif opcode == 5: # MOVGF, Instruction de transfert de la données de l'accumulateur (G) à une adresse (Precise).
                self.cp +=1 # Attente d'une valeur (adresse en decimal).
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(64): Address memoire invalide {address}.")
                self.memoryData[address] = self.g
                print(f"\033[94m Ecriture de la valeur chargée dans la RAM2 à l'adresse {address}.\033[0m")

            elif opcode == 6: # MOGF, Instruction de transfert d'une donnée d'une adress dans la memoire de travail (G).
                self.cp += 1 # Attente d'une valeur (adresse en decimal)
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(72): Adresse memoire invalide {address}.")
                self.g = self.memoryData[address]
                print(f"\033[94m Recharge la RAM2 avec la valeur ({self.g}) charger à l'adresse {address}.\033[0m")

            elif opcode == 33: # PUSH, Transfert d'une donnée d'une memoire de travail à l'EEPROM
                self.cp +=1 # Attente d'une valeur (1 ou 2 en fonction de la ram choisie).
                value = self.memoryProgram[self.cp]
                if value == 1:
                    self.eeprom = self.w
                elif value == 2:
                    self.eeprom = self.g
                else:
                    raise ValueError(f"Error(82): RAM{value} sélectionné non disponible.")
            
            elif opcode == 34: # STOP, Marquer une pause de lecture inconditionnelle.
                self.cp +=1 # Attente d'une valeur (temps de pause).
                value = self.memoryProgram[self.cp]
                time.sleep(value)
                print(f"\033[94m Arrêt temporelle de {value} seconde.\033[0m")

            elif opcode == 35: # END, arrêt du processuce d'execution.
                self.running = False
                print(f"\033[91m Mise en arrêt du cpu: {self.running}\033[0m")
            
            self.cp+=1 # Passe à l'instruction suivante.
            self.display_state() # Afficher l'état final.
            self.save_to_file() # Charger les information memoire.

    def save_to_file(self, file1="dataD.json", file2="dataP.json", file3="portA.json", file4="portB.json"):
        with open("./System/collector/" + file1, 'w') as f:
            json.dump(self.memoryData, f)
        with open("./System/collector/" + file2, 'w') as f:
            json.dump(self.memoryProgram[:64], f)
        with open("./System/collector/" + file3, 'w') as f:
            json.dump(self.A, f)
        with open("./System/collector/" + file4, 'w') as f:
            json.dump(self.B, f)
    
    def display_state(self):
         """affiche lles informations sur l'execution execution"""
         print("\033[33m<============================================================>\033[0m")
         print("\033[33m\t\t=== ETAT DU CPU ===\033[0m")
         print(f"=> Status du CPU(RUN)--------->: {self.running}")
         print(f"=> Compteur de program(CP)---->: {self.cp}")
         print(f"=> Accumulateur(RAM1)--------->: {self.w}")
         print(f"=> Accumulateur(RAM2)--------->: {self.g}")
         print(f"=> Stockage(EEPROM)----------->: {self.eeprom}")
         print("\033[33m<============================================================>\033[0m")

class INST:
    """ Contient une bibliotheque des fonctionnalités (Instructions utilisables) """
    #NOTE: RAM1
    MOVLW = 1 # Instruction de transfert d'une données dans l'accumulateur (W).
    MOVWF = 2 # Instruction de transfert de la données de l'accumulateur (w) à une adresse (Precise).
    MOVF  = 3 # Instruction de transfert d'une donnée d'une adress dans la memoire de travail (W).
    #-----------------------------------------------------------------------------------------------
    #NOTE: RAM2
    MOVLG  = 4 # Instruction de transfert d'une données dans l'accumulateur (G).
    MOVGF = 5 # Instruction de transfert de la données de l'accumulateur (G) à une adresse (Precise).
    MOGF  = 6 # Instruction de transfert d'une donnée d'une adress dans la memoire de travail (G).
    #-------------------------------------------------------------------------------------------------
    
    #NOTE: ALL
    PUSH  = 33
    STOP  = 34
    END   = 35 

class ADR:
    ''' Dix (10) adresses disponible (de l'octet 65 à l'octet 75) occupent 10 Octets dans memoryData  '''
    ddr = [0] * 10
    ddr[0] = 65
    ddr[1] = 66
    ddr[2] = 67
    ddr[3] = 68
    ddr[4] = 69
    ddr[5] = 70
    ddr[6] = 71
    ddr[7] = 73
    ddr[8] = 74
    ddr[9] = 75