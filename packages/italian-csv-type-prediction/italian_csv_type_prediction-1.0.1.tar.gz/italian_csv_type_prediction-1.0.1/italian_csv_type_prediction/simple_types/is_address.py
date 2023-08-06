from .is_string import is_string
from .is_municipality import is_municipality
from .is_region import is_region
from .is_name import is_name


def is_address(candidate) -> bool:
    """Return boolean representing if candidate may be an italian address.

    Notes
    ------------------------------
    Sestiere is a kind of place in Venetian.

    """
    return is_string(candidate) and any(candidate.lower().startswith(target+" ") for target in (
        "via", "strada", "stretto", "piazza", "corso", "piazzale",
        "rue", "viale", "v.le", "largo", "p.za", "stradale",
        "piazzetta", "sestiere", "galleria", "p.zza", "scalinata",
        "vicolo", "isola", "lungarno", "v.", "citta", "contrada",
        "statale", "c.", "borgo", "p.", "vico", "loc.", "stradone",
        "calle", "c.so", "frazione", "passeggiata", "viuzzo",
        "salita", "rione", "lungomare", "campo", "riviera", "C.da",
        "località", "fraz.", "lungotevere", "cavalcavia", "circonvallazione",
        "scesa", "parco", "traversa", "rv.", "ponte", "monte", "piano",
        "bg.", "valle", "sobborgo", "c.da", "case", "casa", "l.go", "strade",
        "lungo", "circ.ne", "atrio", "contrada", "piaz", "p.le", "residenza",
        "p.zale", "borgata", "portici", "p.tta", "calata", "trav.", "str.",
        "quartiere", "ctr.", "lago", "citta'", "lungolago", "cortile", "sobb.",
        "vill.", "villaggio", "rio", "contr.", "vicoletto",
    )) and not (
        is_municipality(candidate) or
        is_region(candidate) or
        is_name(candidate)
    )
