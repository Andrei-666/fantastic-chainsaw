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
        s = 0
        f = 0
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
    ok = 1
    if len(sct_list) != 5:
        print("Nu sunt definiti toti parametri!")
        ok = 0
    if len(sct_cnt_states) == 0:
        print("Nicio stare nu este definita!")
        ok = 0
    if len(sct_cnt_sigma) == 0:
        print("Nu exista input-uri definite!")
        ok = 0
    if len(sct_cnt_transitions) < (len(sct_cnt_sigma) * len(sct_cnt_states)):
        print("DFA-ul nu este complet!")
        ok = 0
    if len(sct_cnt_start) != 1:
        print("DFA-ul nu are o stare initiala.")
        ok = 0
    if len(sct_cnt_final) < 1:
        print("DFA-ul nu are o stare finala.")
        ok = 0
    for symbol in string:
        if symbol not in sct_cnt_sigma:
            print(f"Simbolul {symbol} din input nu este definit în Sigma!")
            ok = 0
    for x in sct_cnt_start:
        if x not in sct_cnt_states:
            print(f"Starea initiala {x} nu este definita.")
    for x in sct_cnt_final:
        if x not in sct_cnt_states:
            print(f"Starea finala {x} nu este definita.")
    return ok

def input_checker(string,sct_cnt_start,sct_cnt_final,sct_cnt_transitions): #verificam daca dfa ul ajunge in starea finala
    string_list = []
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

if __name__ == "__main__":
    if len(sys.argv) != 3:  #verificam daca primim toate fisierele
        sys.exit(1)


    #extragem toate datele de care avem nevoie din fisiere
    config_file = sys.argv[1]
    input_string_file = sys.argv[2]

    content = local_file(config_file)
    sct_list = get_section_list(content)
    sct_cnt_states = get_section_content(content, "States")
    sct_cnt_sigma = get_section_content(content, "Sigma")
    sct_cnt_transitions = get_section_content(content, "Transitions")
    sct_cnt_start = get_section_content(content, "Start")
    sct_cnt_final = get_section_content(content, "Final")
    # citim input ul
    with open(input_string_file, "r") as f:
        string = f.read().strip()
    #verificam daca DFA ul este valid
    ok = section_checker(sct_list, sct_cnt_states, sct_cnt_sigma, sct_cnt_transitions, sct_cnt_start, sct_cnt_final,string)
    if not ok:
        sys.exit(1)



    if input_checker(string, sct_cnt_start, sct_cnt_final, sct_cnt_transitions):
        print("accept")
    else:
        print("reject")