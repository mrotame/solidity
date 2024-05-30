import typing as t


def get_abi(token) -> t.List[t.Dict[str, t.Any]]:
    abi = []
    for key in token._abi:
        abi.append(token._abi[key])

    return abi
