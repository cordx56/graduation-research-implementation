from typing import List

def get_type_str_from_candidate(candidate: List[str]) -> str:
    candidate = set(candidate)
    if len(candidate) == 0:
        return 'Any'
    elif len(candidate) == 1:
        return candidate.pop()
    elif len(candidate) == 2 and 'None' in candidate:
        candidate.remove('None')
        return 'Optional[{}]'.format(candidate.pop())
    else:
        if 'float' in candidate and candidate <= {'int', 'float'}:
            return 'float'
        if 'complex' in candidate and candidate <= {'int', 'float', 'complex'}:
            return 'complex'
        return 'Union[{}]'.format(', '.join(candidate))

def get_type_candidate(context, astobj) -> List[str]:
    if astobj.__class__.__name__ == 'Constant':
        # NoneType
        if astobj.value is None:
            return ['None']
        return [type(astobj.value).__name__]
    elif astobj.__class__.__name__ == 'List':
        eltsType = []
        for e in astobj.elts:
            eltsType.extend(get_type_candidate(context, e))
        return ['List[{}]'.format(get_type_str_from_candidate(eltsType))]
    elif astobj.__class__.__name__ == 'Set':
        eltsType = []
        for e in astobj.elts:
            eltsType.extend(get_type_candidate(context, e))
        return ['Set[{}]'.format(get_type_str_from_candidate(eltsType))]
    elif astobj.__class__.__name__ == 'Dict':
        keysType = []
        valuesType = []
        for e in astobj.keys:
            keysType.extend(get_type_candidate(context, e))
        for e in astobj.values:
            valuesType.extend(get_type_candidate(context, e))
        return ['Dict[{}, {}]'.format(get_type_str_from_candidate(keysType), get_type_str_from_candidate(valuesType))]
    elif astobj.__class__.__name__ == 'Tuple':
        eltsType = []
        for e in astobj.elts:
            eltsType.append(get_type_candidate(context, e))
        return ['Tuple[{}]'.format(', '.join(map(get_type_str_from_candidate, eltsType)))]
    else:
        return []
