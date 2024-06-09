
class DFAemulator:
    def __init__(self, config_file):
        self.states, self.alphabet, self.transitions, self.start_state, self.accept_states = self.config(config_file) #initializam emulatorul cu valorile din engine

    def local_file(self, file_name):  #deschidem fisierul config
        with open(file_name, "r") as f:
            return [line.strip() for line in f if not line.startswith("#")]

    def get_section_list(self, content): #functie pentru crearea listei de sectiuni
        return [line[:-1] for line in content if len(line) > 1 and line[-1] == ":"]

    def get_section_content(self, content, section_name): #functie pentru a scoate valorile in functie de sectiune
        section_content = []
        found = False
        for line in content:
            if found:
                if line.strip() == "End":
                    break
                section_content.append(line.strip())
            elif section_name in line:
                found = True
        return section_content

    def config(self, config_file): #functie pt a scoate datlee din config
        content = self.local_file(config_file)
        sct_cnt_states = self.get_section_content(content, "States")
        sct_cnt_sigma = self.get_section_content(content, "Sigma")
        sct_cnt_transitions = self.get_section_content(content, "Transitions")
        sct_cnt_start = self.get_section_content(content, "Start")
        sct_cnt_final = self.get_section_content(content, "Final")

        states = set(sct_cnt_states)
        alphabet = set(sct_cnt_sigma)
        transitions = {}
        for transition in sct_cnt_transitions:
            parts = transition.split(", ")
            transitions[(parts[0], parts[1])] = parts[2]
        start_state = sct_cnt_start[0]
        accept_states = set(sct_cnt_final)
        return states, alphabet, transitions, start_state, accept_states

    def input(self, input_string):  #functie pt a procesa sirul din fisierul de intrare
        current_state = self.start_state
        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return "reject"
        return "accept" if current_state in self.accept_states else "reject"

class DFAChecker: #checker pentru a verifica sirurile date
    def __init__(self, dfa_emulator, input_file):  #introducem fisierul de intrare
        self.dfa_emulator = dfa_emulator
        self.input_strings = self.read_input_file(input_file)

    def read_input_file(self, input_file): #citim fisierul de intrare si sirurile din el
        with open(input_file, "r") as f:
            return f.readlines()

    def check_input_strings(self): #verificam pe rand fiecare sir
        for input_string in self.input_strings:
            result = self.dfa_emulator.input(input_string.strip())
            print(f"Input string: {input_string.strip()}, Result: {result}")


if __name__ == "__main__":
    dfa_emulator = DFAemulator("dfa_config_file") #facem un emulator pt fisierul "dfa_config_file"
    dfa_checker = DFAChecker(dfa_emulator, "input_string") #facem un checker pt fisierul "input_string"
    dfa_checker.check_input_strings()
