from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Pokemon:
    id: int
    name: str
    specie: str
    type: str
    description: str
    height: float
    weight: float

    def __init__(self, id, name, specie, type, description, height, weight):
        self.id = id
        self.name = name
        self.specie = specie
        self.type = type
        self.description = description
        self.height = height
        self.weight = weight

class PokeAdd(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    name: str = Field(min_length=1)
    specie: str = Field(min_length=1)
    type: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=200)
    height: float = Field(gt=0)
    weight: float = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example":{
                "name": "Pineco",
                "specie": "Bagworm Pokemon",
                "type": "Bug",
                "description": "It hangs and waits for flying-insect prey to come near. It does not move about much on its own.",
                "height": 0.6,
                "weight": 7.2
            }
        }
    }

POKEMONS = [
    Pokemon(1, 'Bulbasaur', 'Seed Pokemon', 'Grass-Poison', 
            'There is a plant seed on its back right from the day this Pokémon is born. ' \
            'The seed slowly grows larger.', 0.7, 6.9),
    Pokemon(2, 'Ivysaur', 'Seed Pokemon', 'Grass-Poison', 
            'There is a plant bulb on its back. When it absorbs nutrients, ' \
            'the bulb is said to blossom into a large flower.', 1.0, 13.0),
    Pokemon(3, 'Venusaur', 'Seed Pokemon', 'Grass-Poison', 
            'A bewitching aroma wafts from its flower. ' \
            'The fragrance becalms those engaged in a battle.', 2.0, 100.0),
    Pokemon(4, 'Charmander', 'Lizard Pokemon', 'Fire', 
            'From the time it is born, a flame burns at the tip of its tail. ' \
            'Its life would end if the flame were to go out.', 0.6, 8.5),
    Pokemon(5, 'Charmeleon', 'Flame Pokemon', 'Fire', 
            'It lashes about with its tail to knock down its foe. ' \
            'It then tears up the fallen opponent with sharp claws.', 1.1, 19.0),
    Pokemon(6, 'Charizard', 'Lizard Pokemon', 'Fire-Flying', 
            'Its wings can carry this Pokémon close to an altitude of 4,600 feet. ' \
            'It blows out fire at very high temperatures.', 1.7, 90.5),
]

# GET

@app.get("/pokedex", status_code=status.HTTP_200_OK)
async def read_all_pokedex():
    return POKEMONS

@app.get("/pokedex/{pokedex_id}", status_code=status.HTTP_200_OK)
async def retrieve_pokemon(pokedex_id: int = Path(gt=0)):
    for pokemon in POKEMONS:
        if pokemon.id == pokedex_id:
            return pokemon
    raise HTTPException(status_code=404, detail='Item not found')

@app.get("/pokedex/name/", status_code=status.HTTP_200_OK)
async def retrieve_poke_by_name(pokemon_name: str = Query(min_length=1)):
    pokemons_to_return = []
    for pokemon in POKEMONS:
        if pokemon.name.lower().find(pokemon_name.lower()) != -1:
            pokemons_to_return.append(pokemon)
    return pokemons_to_return

@app.get("/pokedex/type/", status_code=status.HTTP_200_OK)
async def retrieve_poke_by_type(type: str = Query(min_length=1)):
    pokemons_to_return = []
    for pokemon in POKEMONS:
        if pokemon.type.lower().find(type.lower()) != -1:
            pokemons_to_return.append(pokemon)
    return pokemons_to_return

# POST

@app.post("/add-pokemon", status_code=status.HTTP_201_CREATED)
async def add_pokemon(unseen_pokemon: PokeAdd):
    new_pokemon = Pokemon(**unseen_pokemon.model_dump())
    POKEMONS.append(find_pokedex_id(new_pokemon))

def find_pokedex_id(pokemon: Pokemon):
    pokemon.id = 1 if len(POKEMONS) == 0 else POKEMONS[-1].id + 1
    
    return pokemon

# PUT

@app.put("/pokemon/update_pokemon", status_code=status.HTTP_204_NO_CONTENT)
async def update_pokemon(pokemon: PokeAdd):
    poke_changed = False
    for i in range(len(POKEMONS)):
        if POKEMONS[i].id == pokemon.id:
            POKEMONS[i] = pokemon # type: ignore
            poke_changed = True
    if not poke_changed:
        raise HTTPException(status_code=404, detail='Item not found')

# DELETE
@app.delete("/pokedex/{pokedex_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon(pokedex_id: int = Path(gt=0)):
    poke_changed = False
    for i in range(len(POKEMONS)):
        if POKEMONS[i].id == pokedex_id:
            POKEMONS.pop(i)
            poke_changed = True
            break
    if not poke_changed:
        raise HTTPException(status_code=404, detail='Item not found')