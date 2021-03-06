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

def should_we_build_a_city(turn):
    if turn>30:
        return True
    return False


def is_standing_in_a_city(unit_position, city_tiles):
    for city_tile in city_tiles:
        for city in city_tile.citytiles:
            if (unit_position.x == city.pos.x and unit_position.y == city.pos.y):
                return True
            
    return False

def is_it_night(turn):
    if turn<30:
        return False
    elif turn>39 and turn<70:
        return False
    elif turn>79 and turn<110:
        return False        
    elif turn>119 and turn<150:
        return False                
    elif turn>159 and turn<190:
        return False    
    elif turn>199 and turn<230:
        return False                         
    elif turn>239 and turn<270:
        return False    
    elif turn>279 and turn<310:
        return False                        
    elif turn>319 and turn<350:
        return False                
    return True

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

    wood_tiles = []
    resource_tiles: list[Cell] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                # Get all the wood tiles
                if cell.resource.type == 'wood':
                    wood_tiles.append(cell)

                resource_tiles.append(cell)

    with open(logfile,"a") as f:
        f.write(f"First wood tile: {wood_tiles[0].pos} \n")
    # We want to check if we can build somewhere near first wood tile
    first_wood = wood_tiles[0]
    if first_wood.pos.x != 0:
        cell_north = game_state.map.get_cell(first_wood.pos.x-1, first_wood.pos.y)

    if first_wood.pos.y != 0:
        cell_west = game_state.map.get_cell(first_wood.pos.x, first_wood.pos.y-1)

    cell_east = game_state.map.get_cell(first_wood.pos.x, first_wood.pos.y+1)
    cell_south = game_state.map.get_cell(first_wood.pos.x+1, first_wood.pos.y)
    
    if first_wood.pos.x != 0 and not cell_north.has_resource():
        first_city_build_position = cell_north.pos
        with open(logfile,"a") as f:
            f.write(f"is good: {cell_north.pos} \n")
    if not cell_south.has_resource():
        first_city_build_position = cell_south.pos
        with open(logfile,"a") as f:
            f.write(f"is good: {cell_south.pos} \n")
    if first_wood.pos.y != 0 and not cell_west.has_resource():
        first_city_build_position = cell_west.pos
        with open(logfile,"a") as f:
            f.write(f"is good: {cell_west.pos} \n")
    if not cell_east.has_resource():
        first_city_build_position = cell_east.pos
        with open(logfile,"a") as f:
            f.write(f"is good: {cell_east.pos} \n")    

    # we iterate over all our units and do something with them
    
    with open(logfile,"a") as f:
        f.write(f"Turn: {game_state.turn} \n")
    

    for unit in player.units:
        
        if unit.is_worker() and unit.can_act():
            
            if is_it_night(game_state.turn) and is_standing_in_a_city(unit.pos, player.cities.values()):
                with open(logfile,"a") as f:
                    f.write(f"Its night and we are in a city, we should not move! \n")  
                
            else:
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
                    
                    if should_we_build_a_city(game_state.turn):
                        
                        with open(logfile,"a") as f:
                            f.write(f"We can build a city!! the unit has: {unit.cargo.wood} items \n")
                            f.write(f"Get unit position {unit.pos.x}, {unit.pos.y} \n")
                            
                            #can_i_build_here=unit.can_build(game_state.map.get_cell(unit.pos))
                            #what_is_this = game_state.map.get_cell(unit.pos.x, unit.pos.y)
                            #can_i_build_here = unit.can_build(game_state.map)
                            #f.write(f"Can I build a city here? {what_is_this} \n")
                            #f.write(f"Can I build a city here? {can_i_build_here} \n")
    

                        # Move to the first empty wood city location
                        if unit.pos != first_city_build_position:
                            actions.append(unit.move(unit.pos.direction_to(first_city_build_position)))
                        else:
                            # Build the city
                            action = unit.build_city()
                            actions.append(action)

                        # Find an empty location to build
                        #if unit.can_build(game_state.map) == False:
                        #    with open(logfile,"a") as f:
                        #        f.write(f"Cant build here, move! \n")
    
                        #    build_location = game_state.map.get_cell(1,1)
                        #    actions.append(unit.move(unit.pos.direction_to(build_location.pos)))
                        #else:
                        #    action = unit.build_city()
                        #    actions.append(action)
                        #    with open(logfile,"a") as f:
                        #        f.write(f"Building a City: {action} \n")
                            
                        
                        


                        
                    

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
