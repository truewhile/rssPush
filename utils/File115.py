from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FileInfo:
    cid: str
    aid: str
    pid: str
    n: str
    m: int
    cc: str
    sh: str
    pc: str
    t: str
    te: str
    tu: str
    tp: str
    to: str
    e: str
    p: int
    ns: str
    u: str
    fc: int
    fdes: int
    hdf: int
    ispl: int
    fvs: int
    check_code: int
    check_msg: str
    fuuid: int
    fl: List
    issct: int
    score: int