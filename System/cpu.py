import json, time
class MAIN:
    def __init__(self):
        self.memoryData = [0] * 128 # Memoire de données (2048 bits => 256 Octets => 0.25 Ko).
        self.memoryProgram = [0] * 128 # Memoire de program (1024 bits => 128 Octets => 0.13 Ko).
        self.running = False # Gestionnaire de l'état de marche du cpu (shutdown / END).
        self.w = 0 # Registre accumulateur qui represente la memoire de travaille (La RAM1).
        self.cp = 0 # Compteur de programme, qui pointe l'instructio en cours (Idicateur d'instruction à executer).
        """ BANQUE MEMOIRE DE SAUVEGARDE PERMANANT """
        self.backup_start = 0 # Debut du backup dans memoryData
        self.backup_end = 64 # Réservation de (64 Octets) pour le backup dans memoryData. 
        self.backup_pointer = self.backup_start # Pointeur vers la prochaines case/Octets libre (Dans les 56 cases/Octets).
   
    def load_program(self, program): 
        """charge un programme en memoire en reservant les 64 premieres cases pour les instructions"""
        if len(program) > len(self.memoryProgram):
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
                print(f"\033[94m Chargement de la valeur {self.w} à l'adresse {self.cp}.\033[0m")

            elif opcode == 2: # MOVWF, Instruction de transfert de la données de l'accumulateur (w) à une adresse (Precise).
                self.cp +=1 # Attente d'une valeur (adresse en decimal).
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(38): Address memoire invalide {address}.")
                self.memoryData[address] = self.w
                print(f"\033[94m Ecriture de la valeur chargée dans l'accumulator à l'adresse {address}.\033[0m")

            elif opcode == 3: # MOVF, Instruction de transfert d'une donnée d'une adress dans la memoire de travail (W).
                self.cp += 1 # Attente d'une valeur (adresse en decimal)
                address = self.memoryProgram[self.cp]
                if address >= len(self.memoryData):
                    raise ValueError(f"Error(46): Adresse memoire invalide {address}.")
                self.w = self.memoryData[address]
                print(f"\033[94m Recharge l'accumulateur avec la valeur ({self.w}) charger à l'adresse {address}.\033[0m")

            elif opcode == 4:
                pass

            elif opcode == 5:
                pass

            elif opcode == 6:
                pass
            
            elif opcode == 35: # END, arrêt du processuce d'execution.
                self.running = False
                print(f"\033[91m Mise en arrêt du cpu: {self.running}\033[0m")
            
            self.cp+=1 # Passe à l'instruction suivante.
            self.display_state() # Afficher l'état final.
            self.save_to_file() # Charger les information memoire.

    def save_to_file(self, file1="data.json", file2="program.json"):
        with open("./System/memory/" + file1, 'w') as f:
            json.dump(self.memoryData, f)
        with open("./System/memory/" + file2, 'w') as f:
            json.dump(self.memoryProgram, f)
    
    def display_state(self):
         """affiche lles informations sur l'execution execution"""
         print("\033[33m<============================================================>\033[0m")
         print("\033[33m\t\t=== ETAT DU CPU ===\033[0m")
         print(f"=> Status du CPU: {self.running}")
         print(f"=> Compteur de program (cp): {self.cp}")
         print(f"=> Accumulateur(RAM1): {self.w}")
         print("\033[33m<============================================================>\033[0m")

class INST:
    """ Contient une bibliotheque des fonctionnalités (Instructions utilisables) """
    MOVLW = 1
    MOVWF = 2
    MOVF  = 3
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

class PORT:
    ''' REPECTOIRE DES LIGNES DE PORTS'''
    A = [0] * 5 # Cinq (3) lignes d'adresses pour le  ports A
    B = [0] * 8 # huite (8) lignes d'adresses pour le ports B