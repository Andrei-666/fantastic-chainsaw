import sys

def local_file(file_name): #deschidem fisierul config
    f=open(file_name,"r")
    lista=[]
    for x in f:
        if x[0]!="#":
            lista.append(x.strip()) #facem o lista cu toate valorile din fisier care nu sunt comentarii
    return lista

def get_section_list(content): #functie pentru crearea listei de sectiuni
    lista=[]
    for x in content:
        if len(x)>1 and x[-1]==":":
            lista.append(x[0:len(x)-1])  #adaugam fiecare sectiune in lista
    return lista

def get_section_content(content,section_name): #functie pentru a scoate valorile in functie de sectiune
        s=0
        f=0
        lista=[]
        k=0
        for x in content:
            if x=="End" and k==1:
                k=0
                break
            if k==1:
                lista.append(x)
            if section_name in x:
                k=1

        return lista


def section_checker(sct_list, sct_cnt_states, sct_cnt_sigma, sct_cnt_transitions, start, final,string): #verificam corectitudinea fisierelor pentru a rula programul corect
    ok=1
    if len(sct_list) != 5:
        print("Nu sunt definiti toti parametri!")
        ok=0
    if len(sct_cnt_states) == 0:
        print("Nicio stare nu este definita!")
        ok=0
    if len(sct_cnt_sigma) == 0:
        print("Nu exista input-uri definite!")
        ok=0
    if len(sct_cnt_transitions) < (len(sct_cnt_sigma) * len(sct_cnt_states)):
        print("DFA-ul nu este complet!")
        ok=0
    if len(sct_cnt_start) != 1:
        print("DFA-ul nu are o stare initiala.")
        ok=0
    if len(sct_cnt_final) < 1:
        print("DFA-ul nu are o stare finala.")
        ok=0
    for symbol in string:
        if symbol not in sct_cnt_sigma:
            print(f"Simbolul {symbol} din input nu este definit în Sigma!")
            ok=0
    for x in sct_cnt_start:
        if x not in sct_cnt_states:
            print(f"Starea initiala {x} nu este definita.")
    for x in sct_cnt_final:
        if x not in sct_cnt_states:
            print(f"Starea finala {x} nu este definita.")
    return ok

def input_checker(string,sct_cnt_start,sct_cnt_final,sct_cnt_transitions): #verificam daca dfa ul ajunge in starea finala
    string_list=[]
    cstate=sct_cnt_start[0]
    for x in string:#parcurgem input ul
        string_list.append(x)
    for x in string_list:
        index=0
        for y in sct_cnt_transitions:
            if y.startswith(f"{cstate}, {x}"):  #actualizam starea actuala
                cstate=y[-2:]
                break
            index += 1
    if cstate in sct_cnt_final:
        return True
    else:
        return False

def epsilon_closure_from_set(states, transitions):#functie pentru inchiderea epsilon a unui set de stari
    closure=set()
    for state in states:
        closure.update(epsilon_closure(state, transitions))
    return closure

def epsilon_closure(state, transitions): #functie pentru inchiderea epsilon a unei singure stari
    closure={state}
    stack=[state]
    while stack:
        current=stack.pop()
        for t in transitions:
            parts=t.split(", ")
            if parts[0] == current and parts[1] == 'e':
                if parts[2] not in closure:
                    closure.add(parts[2])
                    stack.append(parts[2])
    return closure

def mutare(states, symbol, transitions): #calculam starile urmatoare
    next_states=set()
    for state in states:
        for t in transitions:
            parts=t.split(", ")   #verificam daca exista o tranzitie valida pt un simbol anume
            if parts[0] == state and parts[1] == symbol:
                next_states.add(parts[2])
    return next_states


def nfa_to_dfa(states, sigma, transitions, start, final_states): #convertire config nfa in dfa
    dfa_states=[start]
    dfa_transitions=[]
    dfa_start='_'.join(sorted(epsilon_closure(start, transitions)))
    dfa_final=[]
    unmarked_states=[dfa_start]
    marked_states=set()

    if set(dfa_start.split('_')).intersection(final_states): #verificam daca staeea initiala este si finala
        dfa_final.append(dfa_start)

    while unmarked_states:  #parcurgem starile care nu sunt de start sau nu sunt etichetate pana acum
        current=unmarked_states.pop()
        marked_states.add(current)

        for symbol in sigma:
            if symbol != 'e':
                next_state='_'.join(sorted(epsilon_closure_from_set(mutare(current.split('_'), symbol, transitions), transitions))) #calculam stara urmatoare
                if next_state:
                    dfa_transitions.append(f"{current}, {symbol}, {next_state}") #adaugam tranzitia in lista de tranzitii valide
                    if next_state not in marked_states and next_state not in unmarked_states:
                        unmarked_states.append(next_state)
                        if set(next_state.split('_')).intersection(final_states): #verificam daca e stare finala si daca e o adaugam in lista de stari finale
                            dfa_final.append(next_state)
                        if next_state not in dfa_states:
                            dfa_states.append(next_state)  # adaugam noua stare
    return dfa_states, sigma, dfa_transitions, dfa_start, dfa_final

if __name__ == "__main__":
    if len(sys.argv) != 3:  # verificam daca primim toate fisierele
        sys.exit(1)
        
    config_file_nfa=sys.argv[1]
    config_file_dfa=sys.argv[2]

    content=local_file(config_file_nfa)
    sct_list=get_section_list(content)
    sct_cnt_states=get_section_content(content, "States")
    sct_cnt_sigma=get_section_content(content, "Sigma")
    sct_cnt_transitions=get_section_content(content, "Transitions")
    sct_cnt_start=get_section_content(content, "Start")
    sct_cnt_final=get_section_content(content, "Final")

    # facem liste pentru a lucra mai usor
    states=set(sct_cnt_states)
    sigma=set(sct_cnt_sigma)
    transitions=set(sct_cnt_transitions)
    start=sct_cnt_start[0]
    final_states=set(sct_cnt_final)

    dfa_states, dfa_sigma, dfa_transitions, dfa_start, dfa_final=nfa_to_dfa(states, sigma, transitions, start,final_states)
    dfa_states.append("D")
    trap_transitions=[]  #adaugam tranzitii catre trap state unde nu avem tranzitii catre alte stari
    for state in dfa_states:
        for symbol in sigma:
            if not any(t for t in dfa_transitions if t.startswith(f"{state}, {symbol}")):
                trap_transitions.append(f"{state}, {symbol}, D")

    dfa_transitions.extend(trap_transitions) #le adaugam la final ca sa se afiseze utlimele
    with open(config_file_dfa, "w") as f:
        f.write("Sigma:\n")
        for sym in dfa_sigma:
            f.write(f"    {sym}\n")
        f.write("End\n")

        f.write("States:\n")
        for state in dfa_states:
            state=state.strip()  
            if state:  #ne asiguram ca linia nu va ramane goala
                f.write(f"    {state}\n")
        f.write("End\n")

        f.write("Start:\n")
        f.write(f"    {dfa_start.replace(' ', '')}\n")  
        f.write("End\n")

        f.write("Final:\n")
        for final_state in dfa_final:
            f.write(f"    {final_state.replace(' ', '')}\n")  
        f.write("End\n")

        f.write("Transitions:\n")
        for transition in dfa_transitions:
            f.write(f"    {transition}\n")
        f.write("End\n")
