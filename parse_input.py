# Functions for parsing user input and printing help messages

import sys
import logging

PLATONIC_SOLIDS = {"tetrahedron":4, "octahedron":6,"cube":8,"icosahedron":12,"dodecahedron":20, "fullerene60":60}
POLYENES = {"linear_polyene", "cyclic_polyene", "platonic"}

# Help message
def print_help():
    print("Help Message")
    print("  To calculate the Huckel energies for specified pi-system, run:")
    print("    python main.py [structure] [number of atoms, optional]")
    print("  The possible structures are: ")
    print("    "+", ".join(POLYENES) + ", " + ", ".join(PLATONIC_SOLIDS.keys()))
    print("  Flags:")
    print("    -h --help       Displays this message")
    print("    -o --optimized  Use general solution for linear and cyclic polyenes instead of solving eigenvalues")
    print("  Example inputs:")
    print("    - python main.py cyclic_polyene 6")
    print("    - python main.py cube")
    print("    - python main.py platonic 4")
    print("    - python main.py fullerene60")
    print("  The output energies are relative to the atom energies, and are not scaled (alpha=0, beta=-1).")

FLAGS = {"o": "optimized", "h": "help"}

def extract_flags():
    """
    Extracts the -x and --xxx flags from sys.argv.

    Returns the flags and the rest of arguments with flags removed
    """
    flags = []
    args = []

    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            flag = arg[2:]
            if flag in FLAGS.values():
                flags.append(flag)
            else:
                logging.warning(f"Unrecognized flag '--{flag}'")
        elif arg.startswith("-"):
            flag = arg[1:]
            if flag in FLAGS:
                flags.append(FLAGS[flag])
            else:
                logging.warning(f"Unrecognized flag '-{flag}'")
        else:
            args.append(arg)

    return flags, args

def parse_user_input() -> (str, int, [str]):
    """
    Parses the console input. If the parsing is successful, returns (<structure_type>, <number_of_atoms>, <flags>).
    Otherwise returns ("no_calc", 0, <flags>)
    """
    flags, args = extract_flags()

    if "help" in flags:
        print_help()

    # NO ARGUMENTS OR HELP
    if len(args) == 0:
        logging.warning("No arguments provided. Run 'python main.py -h' to get help message")
        return ("no_calc",0,flags)
    # ONE ARGUMENT
    elif len(args) == 1:
        structure = args[0]

        if structure in PLATONIC_SOLIDS:
            return ("platonic",PLATONIC_SOLIDS[structure],flags)
        elif structure in POLYENES:
            logging.error("You need to specify the number of atoms")
            return ("no_calc",0,flags)
        else:
            logging.error(f"The structure '{structure}' has not been recognized.")
            logging.info(f"The possible structures are: {', '.join(list(POLYENES) + list(PLATONIC_SOLIDS.keys()))}")
            return ("no_calc",0,flags)
    # TWO AND MORE ARGUMENTS
    elif len(args) >= 2:
        if len(args) > 2:
            logging.warning(f"There are too many arguments, the following are ignored: {' '.join(args[2:])}")
        
        structure = args[0]

        if structure in PLATONIC_SOLIDS:
            logging.warning(f"The atom count is not required for specific platonic solids, the following argument is ignored: {args[1]}")
            return ("platonic",PLATONIC_SOLIDS[structure],flags)
        elif structure in POLYENES:
            try:
                n_atoms = int(args[1])
            except:
                logging.warning(f"Cannot parse '{args[1]}' to an integer")
                return ("no_calc",0,flags)

            if structure == "platonic":
                if n_atoms not in PLATONIC_SOLIDS.values():
                    logging.error("The number of atoms does not match any platonic solid")
                    logging.info(f"The possible values are: {', '.join([f'{v}' for v in PLATONIC_SOLIDS.values()])}")
                    return ("no_calc",0,flags)
                else:
                    return ("platonic", n_atoms,flags)
            elif structure == "cyclic_polyene":
                if n_atoms < 3:
                    logging.error("A cyclic polyene must have at least 3 atoms")
                    return ("no_calc",0,flags)
                else:
                    return ("cyclic_polyene", n_atoms, flags)
            else:
                if n_atoms < 2:
                    logging.error("Linear polyene must have at least 2 atoms")
                    return ("no_calc",0,flags)
                else:
                    return ("linear_polyene", n_atoms,flags)
        else:
            logging.error(f"The structure '{args[0]}' has not been recognized.")
            logging.info(f"The possible structures are: {', '.join(list(POLYENES) + list(PLATONIC_SOLIDS.keys()))}")
            return ("no_calc",0,flags)
    
    logging.error("Unreachable code")
    return ("no_calc",0,flags)