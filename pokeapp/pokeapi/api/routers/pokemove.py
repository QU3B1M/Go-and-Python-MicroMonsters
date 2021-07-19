from typing import List

from fastapi import APIRouter, HTTPException

from ..database.schemas import PokeMove
from ..database.repositories import PokeMoveRepository, PokeTypeRepository
from ..models import PokeMoveIn, PokeMoveOut


router = APIRouter(prefix="/pokemove", tags=["PokeMoves"])


@router.get("/", response_model=List[PokeMoveOut])
async def get_all_pokemoves():
    """
    ## Retrieves a PokeMove List.

    Path Parameters
    ---------------
        None

    Body Parameters
    ---------------
        None

    Returns
    -------
        List[PokeMove]
    """
    moves: List[PokeMove] = await PokeMoveRepository.get_all()
    return [await move.dict() for move in moves]


@router.get("/{id}", response_model=PokeMoveOut)
async def get_pokemove(id: int):
    """
    ## Retrieves a PokeMove by ID.

    Path Parameters
    ---------------
        id: int                 PokeMove ID.

    Body Parameters
    ---------------
        None

    Returns
    -------
        id: int                                 PokeMove ID.
        name: str                               Name of the PokeMove.
        effect: str                             Effect of the PokeMove.
        type: PokeTypeBase                      Type of the PokeMove.
        category:str [physical/special/status]  Category of the PokeMove.

    """
    pokemove: PokeMove = await PokeMoveRepository.get(id=id)
    if not pokemove:
        raise HTTPException(404, detail="PokeMove not found.")

    return await pokemove.dict()


@router.post("/create", response_model=PokeMoveOut)
async def create_pokemove(poke_in: PokeMoveIn):
    """
    ## Creates a PokeMove.

    Path Parameters
    ---------------
        None

    Body Parameters
    ---------------
        name: str                               Name of the PokeMove.
        effect: str                             Effect of the PokeMove.
        type: PokeTypeBase                      Type of the PokeMove.
        category:str [physical/special/status]  Category of the PokeMove.


    Returns
    -------
        id: int                                 PokeMove ID.
        name: str                               Name of the PokeMove.
        effect: str                             Effect of the PokeMove.
        type: PokeTypeBase                      Type of the PokeMove.
        category:str [physical/special/status]  Category of the PokeMove.

    """

    if not await PokeTypeRepository.exists(id=poke_in.type_id):
        raise HTTPException(status_code=422, detail="Invalid type_id (PokeType).")
    # Creates the PokeMove
    pokemove: PokeMove = await PokeMoveRepository.create(poke_in)

    return await pokemove.dict()


@router.put("/update/{id}", response_model=PokeMoveOut)
async def update_pokemove(id: int, poke_in: PokeMoveIn):
    """
    ## Updates a PokeMove by ID.

    Path Parameters
    ---------------
        id:int                                  PokeMove ID.

    Body Parameters
    ---------------
        name: str                               Name of the PokeMove.
        effect: str                             Effect of the PokeMove.
        type: PokeTypeBase                      Type of the PokeMove.
        category:str [physical/special/status]  Category of the PokeMove.


    Returns
    -------
        id: int                                 PokeMove ID.
        name: str                               Name of the PokeMove.
        effect: str                             Effect of the PokeMove.
        type: PokeTypeBase                      Type of the PokeMove.
        category:str [physical/special/status]  Category of the PokeMove.

    """
    if not await PokeMoveRepository.exists(id=id):
        raise HTTPException(status_code=404, detail="PokeMove not found.")

    if not await PokeTypeRepository.exists(id=poke_in.type_id):
        raise HTTPException(status_code=422, detail="Invalid type_id (PokeType).")

    return await PokeMoveRepository.update(poke_in, id=id)


@router.delete("/delete/{id}", response_model=bool)
async def delete_pokemove(id: int):
    """
    ## Deletes a PokeMove by ID.

    Path Parameters
    ---------------
        PokeMove ID.

    Body Parameters
    ---------------
        None

    Returns
    -------

        None

    """
    if not await PokeMoveRepository.exists(id=id):
        raise HTTPException(status_code=404, detail="PokeMove not found.")
    return await PokeMoveRepository.delete(id=id)