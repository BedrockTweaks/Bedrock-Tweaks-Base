import os
import shutil

if str(os.getcwd()).endswith("system32"):
    doubleclicked = True
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
else:
    doubleclicked = False

from custom_functions import *

check("clrprint")
from clrprint import clrprint

check("ujson")
from ujson import *

check("pyperclip")


def update_size():
    global clm, lins, min_clm, clms, pclms
    clm = shutil.get_terminal_size().columns
    lins = shutil.get_terminal_size().lines
    min_clm = 42
    clms = clm // min_clm
    pclms = -1


update_size()


def clmthing():
    global pclms, clms
    pclms += 1
    if pclms == clms:
        pclms = 0
        print("\n")


def load_json(path):
    with open(path, "r") as file:
        return loads(file.read())


# Menu Up and Down stuff
down = {
    "main_menu": ["pack_select", "selected_packs"],
    "pack_select": ["select_pack"]
}
up = {
    "select_pack": "pack_select",
    "pack_select": "main_menu",
    "selected_packs": "main_menu"
}


# Command validation for below
def val_command(menu, command):
    if type(command) == list:
        if command[0] == "back":
            return ["page", "pack_select", command[1]]
        elif menu == "pack_select":
            return ["page", "select_pack", command[0], command[1], command[2]]
        elif menu == "select_pack" and command[0] == "select":
            packjson = load_json(f"{cdir()}/jsons/packs/{command[1]}")
            topic = packjson["topic"]

            selpackjson = load_json(f"{cdir()}/jsons/others/selected_packs.json")
            selpackjson[topic].append("".join(command[2].split()))
            selpackjson["raw"].append("".join(command[2].split()))

            dump_json(f"{cdir()}/jsons/others/selected_packs.json", selpackjson)

            clrprint(f"{command[2]} has been added to Selected Packs!", clr="green")
            return ["page", up[menu], f'{"".join(topic.replace(" ", "_").lower().split())}.json']
        elif menu == "select_pack" and command[0] == "unselect":
            packjson = load_json(f"{cdir()}/jsons/packs/{command[1]}")
            topic = packjson["topic"]
            selpackjson = load_json(f"{cdir()}/jsons/others/selected_packs.json")

            for i in range(len(selpackjson[topic])):
                if selpackjson[topic][i] == "".join(command[2].split()):
                    selpackjson[topic].pop(i)
                    break
            for i in range(len(selpackjson["raw"])):
                if selpackjson["raw"][i] == "".join(command[2].split()):
                    selpackjson["raw"].pop(i)
                    break

            dump_json(f"{cdir()}/jsons/others/selected_packs.json", selpackjson)
            clrprint(f"{command[2]} has been removed from Selected Packs!", clr="green")

            return ["page", up[menu], f'{"".join(topic.replace(" ", "_").lower().split())}.json']
    elif type(command) == str:
        if command == "back":
            return ["page", up[menu]]
        elif menu == "main_menu" and command not in ["exit", "show selected packs"]:
            return ["page", "pack_select", command]
        elif menu == "main_menu" and command == "show selected packs":
            return ["page", "selected_packs"]
        elif command == "exit":
            clrprint("Exited program.", clr="yellow")
            exit(0)
        else:
            raise ValueError(f"{command} is not a valid command!")


# Menu Screen showing categories
def main_menu():
    choice = None
    while choice is None:
        update_size()
        clear()
        clrprint("Main Menu", clr="default")

        clrprint("\nCategories", clr="purple")
        menu_commands = [""]

        # Sort the list of files before iterating over them
        pack_files = sorted(os.listdir(f"{cdir()}/jsons/packs"))
        for i, filename in enumerate(pack_files):
            clmthing()
            loadpackjson = load_json(f'{cdir()}/jsons/packs/{filename}')
            print(f'{i + 1}. {loadpackjson["topic"]}', end="")
            print(" " * (min_clm - len(f'{i + 1}. {loadpackjson["topic"]}')), end="")
            menu_commands.append(filename.lower())
        clrprint("\n\nOthers", clr="purple")

        print(f"{len(pack_files) + 1}. Show Selected Packs", end="")
        print(" " * (min_clm - 23), end="")
        menu_commands.append("show selected packs")
        clmthing()

        print(f"{len(pack_files) + 2}. Exit Program")
        menu_commands.append("exit")

        choice = input("\nEnter your choice.\n").lower()
        progged = prog_search(choice, menu_commands)
        if choice == "":
            choice = None
        elif choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif progged:
            choice = menu_commands[progged]
        else:
            choice = None
    return choice


def pack_select(topic):
    choice = None
    while choice is None:
        update_size()
        packs = load_json(f"{cdir()}/jsons/packs/{topic}")
        incpacks = load_json(f"{cdir()}/jsons/others/incomplete_packs.json")
        selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")

        clear()
        clrprint(f'Main Menu -> {packs["topic"]}\n', clr="default")
        clrprint("Red", "means this pack has not been finished and cannot be selected", clr="r,y")
        clrprint("Green", "means this pack has been selected", clr="g,y")
        clrprint("Blue", "means this pack conflicts with another pack and cannot be selected\n", clr="b,y")
        clrprint("Packs", clr="purple")
        menu_commands = [""]

        for i in range(len(packs["packs"])):
            clmthing()
            if packs["packs"][i]["pack_id"] in incpacks[packs["topic"]]:
                clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="red")
                menu_commands.append("")
            elif packs["packs"][i]["pack_id"] in selpacks[packs["topic"]]:
                clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="green")
                menu_commands.append(packs["packs"][i]["pack_name"])
            else:
                conflict = False
                for c in packs["packs"][i]["conflict"]:
                    if c in selpacks["raw"]:
                        clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="blue")
                        conflict = True
                        break
                if not conflict:
                    clrprint(f'{i + 1}. {packs["packs"][i]["pack_name"]}', end="", clr="white")
                menu_commands.append(packs["packs"][i]["pack_name"])
            print(" " * (min_clm - len(f'{i + 1}. {packs["packs"][i]["pack_name"]}')), end="")

        clrprint("\n\nOthers", clr="purple")
        print(f'{i + 2}. Go Back (back)', end="")
        print(" " * (min_clm - len(f'{i + 2}. Go Back (back)')), end="")
        menu_commands.append("back")
        clmthing()
        print(f'{i + 3}. Exit Program')
        menu_commands.append("exit")
        choice = input("Enter your choice.\n")
        progged = prog_search(choice, menu_commands)
        if choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif progged:
            choice = menu_commands[progged]
        else:
            choice = None
        if choice == "":
            choice = None
    if choice.lower() in ["exit", "back"]:
        return choice
    else:
        return [topic, choice, menu_commands.index(choice)]


def selected_packs():
    choice = None
    while choice is None:
        update_size()
        clear()
        clrprint("Main Menu -> Selected Packs\n", clr="default")
        menu_commands = [""]
        selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")

        hasitem = False
        for key, value in selpacks.items():
            if value != [] and key != "raw":
                hasitem = True
                sortedsel = sorted(value)
                clrprint(key, clr="green")
                for item in sortedsel:
                    print(f"\t- {item}")
        if not hasitem:
            clrprint("There is nothing selected ._.\nMaybe head back and select some packs!", clr="yellow")
        clrprint("\nOptions", clr="purple")
        print(f"1. Go Back (back)")
        menu_commands.append("back")

        print("\n2. Exit Program (exit)")
        menu_commands.append("exit")
        choice = input("Enter your choice.\n")
        if choice == "":
            choice = None
        elif choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif choice in ["back", "exit"]:
            pass
        else:
            choice = None
    return choice


def select_pack(topic, pack, index):
    choice = None
    while choice == None:
        packs = load_json(f"{cdir()}/jsons/packs/{topic}")
        selpacks = load_json(f"{cdir()}/jsons/others/selected_packs.json")

        clear()
        clrprint(f'Main Menu -> {packs["topic"]} -> {pack}\n', clr="default")
        print(packs["packs"][int(index) - 1]["pack_description"])
        menu_commands = [""]
        conflict = False
        for i in packs["packs"][index - 1]["conflict"]:
            if i in selpacks["raw"]:
                clrprint(f"{pack} has a conflict with {i}!", clr="b")
                clrprint(f"Unselect {i} to select {pack}!", clr="b")
                conflict = True
                break
        uns = "S"
        if "".join(pack.split()) in selpacks[packs["topic"]]:
            clrprint(f"{pack} has already been selected!", clr="green")
            uns = "Uns"
        if uns == "Uns" and conflict:
            # Just a joke, but seriously, this part
            # is here if someone adds a conflicting pack
            # manually and tries to break the script
            clrprint(f"Both {pack} and {i} are selected...", clr="red")
            raise SyntaxError("not a chance")
        if conflict:
            clrprint(f"\n1. {uns}elect {pack} ({uns.lower()}elect)", clr="red")
            menu_commands.append("")
        else:
            print(f"\n1. {uns}elect {pack} ({uns.lower()}elect)")
            menu_commands.append(f"{uns.lower()}elect")

        print("\n2. Go Back (back)")
        menu_commands.append("back")

        print(f"\n3. Exit Program (exit)")
        menu_commands.append("exit")

        choice = input("\nEnter your choice.\n").lower()
        progged = prog_search(choice, menu_commands)
        if choice.isnumeric():
            try:
                choice = menu_commands[int(choice)]
            except IndexError:
                choice = None
        elif progged:
            choice = menu_commands[progged]
        else:
            choice = None
        if choice == "":
            choice = None
    if choice == "back":
        return [choice, f'{topic.replace(" ", "_").lower()}']
    elif choice == "exit":
        return choice
    else:
        return [choice, f'{topic.replace(" ", "_").lower()}', pack]


command = ["page", "main_menu"]
try:
    while True:
        if command[0] == "page" and command[1] == "main_menu":
            command = main_menu()
            command = val_command("main_menu", command)
        elif command[0] == "page" and command[1] == "pack_select":
            command = pack_select(command[2])
            command = val_command("pack_select", command)
        elif command[0] == "page" and command[1] == "select_pack":
            command = select_pack(command[2], command[3], command[4])
            command = val_command("select_pack", command)
        elif command[0] == "page" and command[1] == "selected_packs":
            command = selected_packs()
            command = val_command("selected_packs", command)
        clrprint("If you can see this, I suffered about 8 hours in total for this", clr="purple")
        clrprint("Please send help", clr="purple")
except KeyboardInterrupt:
    val_command("keyboard_interrupt", "exit")