from typing import Dict, Set


def get_complement_dict(caption:str, orgs_to_slownikize_set:Set[str], mods_set:set[str])->Dict[str,str]:
    #tutaj masz po lewej tabelki pokazać orgs_to_slownikize_set, a po prawej mods_set i kazać przypisać
    #jak wszystko jest przypisane to można skończyć, jak nie to przerywasz proces
    if len(orgs_to_slownikize_set) == 1:
        org_to_add = list(orgs_to_slownikize_set)[0]
        mod = list(mods_set)[0]
        complement_dict = {}
        complement_dict[org_to_add] = mod
    else:
        raise NotImplementedError

    return complement_dict