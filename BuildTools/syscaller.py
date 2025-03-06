import os
import subprocess
import sys
import time

class Colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def display_logo():
    logo = r"""
                 ++****+++====                              
             =++++****++++===---:                           
             =++++****+++===---:::                          
            =++++****++++===---:::  +%                      
            =++++****+++===----::  -:---               ++=# 
           ==+++****++++===---:::  +:---===+++#=**#***++=:  
           =++++****+++===---:::  -:---====+++*******+++=-  
          *=+++****++++===---:::  +:---===++++***#***++=:   
          =++++****+++===----::+ -:---====+++*******+++=:   
          =+++****++++===---:::  +:---===++++***#***++=:    
         =++++****+++====---::: -:---====+++*******+++=:    
         =+++****:::=+==---:::  +:---===++++***#***+++:     
        =+::             :-::: =:---====+++********++=:     
             -***++++-      :  =:---===++++***#***++=:      
        ===++***++++===---     ::---===+++********++=:      
       -==+++***++++==---::.    :=-===++++***#***++-:       
      -===++***++++===--::..  *#    :++++*****=:::          
      -==+++***++++==---::.  +--==*              %**-       
     -===++***++++===--::..  *-===++++****####*****-        
     -==+++***++++==---::.   --===++++****###******-        
    ====++***++++===--::..  +-===++++****####*****-         
    -==+++***++++==---::.   --===++++****###******-         
    ===++****+++===--:::.  +-===++++****####*****-          
   -==+++***++++==---::.:  --===++++****###******-          
   ===++*****+++==--:::.  +-====+++****####*****-           
  -=+...         ..-::..  --===++++****###******-           
                     ..  =-====+++*****###*****=            
                         =-===++++****###******-            
                           :==+++*****###****=:             
                              ::*****##++:: 
    """
    print(f"{Colors.OKBLUE}{logo}{Colors.ENDC}")

def run_validation_check():
    print(f"{Colors.OKBLUE}Running Validation Check...{Colors.ENDC}")
    result = subprocess.run(['python', 'Validator/valid.py'], capture_output=True, text=True)
    print(result.stdout)
    input(f"{Colors.OKGREEN}Press Enter to Continue...{Colors.ENDC}")

def run_compatibility_check():
    print(f"{Colors.OKBLUE}Running Compatibility Check...{Colors.ENDC}")
    result = subprocess.run(['python', 'Compatibility/compatibility.py'], capture_output=True, text=True)
    print(result.stdout)
    input(f"{Colors.OKGREEN}Press Enter to Continue...{Colors.ENDC}")

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_logo()
        print(f"{Colors.OKBLUE}=== SysCaller BuildTools CLI ==={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1. Run Validation Check{Colors.ENDC}")
        print(f"{Colors.OKGREEN}2. Run Compatibility Check{Colors.ENDC}")
        print(f"{Colors.OKGREEN}3. Exit{Colors.ENDC}")
        choice = input(f"{Colors.BOLD}Select an Option (1-3): {Colors.ENDC}")
        if choice == '1':
            run_validation_check()
        elif choice == '2':
            run_compatibility_check()
        elif choice == '3':
            print(f"{Colors.FAIL}Exiting...{Colors.ENDC}")
            time.sleep(1)
            break
        else:
            print(f"{Colors.WARNING}Invalid Option. Please try Again.{Colors.ENDC}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
