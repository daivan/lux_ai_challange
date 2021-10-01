import math, sys
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate


logfile = "agent.log"

open(logfile,"w")

with open(logfile,"a") as f:
    f.write(f"-- Starting new game --\n")

DIRECTIONS = Constants.DIRECTIONS
game_state = None

should_we_build_a_city = True


def agent(observation, configuration):
    global game_state
    global should_we_build_a_city

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])
    
    actions = []

    ### AI Code goes down here! ### 
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height

    resource_tiles: list[Cell] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                resource_tiles.append(cell)

    # we iterate over all our units and do something with them
    
    
    for unit in player.units:
        
        if unit.is_worker() and unit.can_act():

            closest_dist = math.inf
            closest_resource_tile = None
            if unit.get_cargo_space_left() > 0:
                # if the unit is a worker and we have space in cargo, lets find the nearest resource tile and try to mine it
                for resource_tile in resource_tiles:
                    if resource_tile.resource.type == Constants.RESOURCE_TYPES.COAL and not player.researched_coal(): continue
                    if resource_tile.resource.type == Constants.RESOURCE_TYPES.URANIUM and not player.researched_uranium(): continue
                    dist = resource_tile.pos.distance_to(unit.pos)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_resource_tile = resource_tile
                if closest_resource_tile is not None:
                    actions.append(unit.move(unit.pos.direction_to(closest_resource_tile.pos)))
            else:
                
                if should_we_build_a_city:
                    
                    with open(logfile,"a") as f:
                        f.write(f"We can build a city!! the unit has: {unit.cargo.wood} items \n")
                        f.write(f"Get unit position {unit.pos.x}, {unit.pos.y} \n")
                        
                        #can_i_build_here=unit.can_build(game_state.map.get_cell(unit.pos))
                        #what_is_this = game_state.map.get_cell(unit.pos.x, unit.pos.y)
                        #can_i_build_here = unit.can_build(game_state.map)
                        #f.write(f"Can I build a city here? {what_is_this} \n")
                        #f.write(f"Can I build a city here? {can_i_build_here} \n")
  

                    
                    # Find an empty location to build
                    if unit.can_build(game_state.map) == False:
                        with open(logfile,"a") as f:
                            f.write(f"Cant build here, move! \n")
   
                        build_location = game_state.map.get_cell(1,1)
                        actions.append(unit.move(unit.pos.direction_to(build_location.pos)))
                    else:
                        action = unit.build_city()
                        actions.append(action)
                        with open(logfile,"a") as f:
                            f.write(f"Building a City: {action} \n")
                        
                    
                    


                    
                

                # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
                elif len(player.cities) > 0:
                    closest_dist = math.inf
                    closest_city_tile = None
                    for k, city in player.cities.items():
                        for city_tile in city.citytiles:
                            dist = city_tile.pos.distance_to(unit.pos)
                            if dist < closest_dist:
                                closest_dist = dist
                                closest_city_tile = city_tile
                    if closest_city_tile is not None:
                        move_dir = unit.pos.direction_to(closest_city_tile.pos)
                        actions.append(unit.move(move_dir))

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))
    
    # Try and build a Unit
    with open(logfile,"a") as f:
        f.write(f"We have this many cities: {player.city_tile_count} \n")
        f.write(f"We have this many units: {len(player.units)} \n")

    if player.city_tile_count>len(player.units):
        with open(logfile,"a") as f:
            f.write(f"We have less units than cities. Can build a unit \n")
            f.write(f"What is this. {player.cities} \n")
        
        for city in player.cities.values():
            for city_tile in city.citytiles:

                with open(logfile,"a") as f:
                    f.write(f"Does this even work? {city_tile} \n") 

                if city_tile.can_act():
                        actions.append(city_tile.build_worker())
                        with open(logfile, "a") as f:
                            f.write(f"Created and worker \n")
        
    return actions
