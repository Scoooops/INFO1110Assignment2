import sys

# Please implement this function according to Section "Read Configuration File"
def load_config_file(filepath):
  try:  #Checking if file exists
    config = open(filepath, 'r')
  except FileNotFoundError:
    raise FileNotFoundError
  else: #Checking the file has the right format
    config_test = open(filepath, 'r')
    line = str(config_test.readline()).rstrip()
    if line[0:6] != "Frame:":
      raise SyntaxError("Invalid Configuration File: format error!")
    line = str(config_test.readline()).rstrip("\n")
    if line[0:7] != "Water: ":
      raise SyntaxError("Invalid Configuration File: format error!")
    line = str(config_test.readline()).rstrip("\n")
    if line[0:6] != "Wood: ":
      raise SyntaxError("Invalid Configuration File: format error!")
    line = str(config_test.readline()).rstrip("\n")
    if line[0:6] != "Food: ":
      raise SyntaxError("Invalid Configuration File: format error!")
    line = str(config_test.readline()).rstrip("\n")
    if line[0:6] != "Gold: ":
      raise SyntaxError("Invalid Configuration File: format error!")

  #Defining important coordinates
  home_base_coords = [[1,1], [0,1], [1,0], [2,1], [1,2]]
  p1_surrounding_coords = [[0,1], [1,0], [2,1], [1,2]]
  p2_surrounding_coords = []
  current_coords = []

  #A function to check the input for each resource is valid
  def set_coords(resource, resource_name):
    resource_coords = resource
    resource_coord_values = []
    resource_coord_points = []
    counter = 0
    j = 0
    i = 0
    #Taking x and y coordinates for each resource point
    while i < len(resource_coords):
      if resource_coords[i] == " ":
        resource_coord_values.append(str(resource_coords[j:i]))
        j = i+1
      i += 1
    if resource_coords[i-1] != " ":
        resource_coord_values.append(str(resource_coords[j:i]))
    for num in resource_coord_values:
      try:  #Checking if each value is an integer
        num = int(num)
      except ValueError:
        raise ValueError("Invalid Configuration File: " + resource_name +\
                          " contains non integer characters!")
    for num in resource_coord_values:
      if int(num)<0:    #Checking values are not negative
        raise ValueError("Invalid Configuration File: " + resource_name +\
                          " contains non integer characters!")
    if len(resource_coord_values)%2 != 0:  #Checking for even number of values
      raise SyntaxError("Invalid Configuration File: " + resource_name+\
                        " has an odd number of elements!")
    while counter<len(resource_coord_values):
      if not 0<=int(resource_coord_values[counter])<=board_width:
        raise ArithmeticError("Invalid Configuration File: " +\
                                resource_name + " contains a position"
                                " that is out of map.")
      else:
        counter += 2
    counter = 1
    while counter<len(resource_coord_values):
      #Checking all values are in the boundary of the game
      if not 0<=int(resource_coord_values[counter])<=board_height:
        raise ArithmeticError("Invalid Configuration File: " +\
                                resource_name + " contains a position "
                                "that is out of map.")
      else:
        counter += 2
    i = 2
    j = 0
    while i<=len(resource_coord_values):
      point = []    #List that will contain a single point at a time
      for points in resource_coord_values[j:i]:
        point.append(int(points))
      if point in home_base_coords:
        raise ValueError("Invalid Configuration File: The positions "
                            "of home bases or the positions next to "
                            "the home bases are occupied!")
      if point in current_coords:
        raise SyntaxError("Invalid Configuration File: Duplicate "
                            "position ({})!".format(point)\
                            .replace("[", "").replace("]", ""))
      #Adding the point to the main list of resource coordinates
      resource_coord_points.append(point)
      current_coords.append(point)
      i += 2
      j += 2
    return(resource_coord_points)

  #Loop to check the validity of the frame input and change map accordingly
  while True:
    line = str(config.readline()).rstrip()
    if line[0:2] == "Fr":
      line = line.replace(" ", "")
      x = line.find("x")    #Making sure frame is in format widthxheight
      if x == -1:
        raise SyntaxError("Invalid Configuration File: frame should "
                            "be in format widthxheight!")
      else:
        try:    #Cheching to make sure both values are integers
          board_width = int(line[(line.find(":")+1):x])
          board_height = int(line[x+1:])
        except ValueError:
          raise SyntaxError("Invalid Configuration File: frame "
                            "should be in format widthxheight!")
        if board_width<0 or board_height<0:
          raise SyntaxError("Invalid Configuration File: frame "
                            "should be in format widthxheight!")
        #If frame input it acceptable, add all the base location and
        #surrounding coords
        if 4<board_width<8 and 4<board_height<8:
          base_two = [board_width-2, board_height-2]
          home_base_coords.insert(1, base_two)
          home_base_coords.append([board_width-3, board_height-2])
          home_base_coords.append([board_width-2, board_height-3])
          home_base_coords.append([board_width-1, board_height-2])
          home_base_coords.append([board_width-2, board_height-1])
          p2_surrounding_coords.append([board_width-3, board_height-2])
          p2_surrounding_coords.append([board_width-2, board_height-3])
          p2_surrounding_coords.append([board_width-1, board_height-2])
          p2_surrounding_coords.append([board_width-2, board_height-1])
          continue
        else:
          raise ArithmeticError("Invalid Configuration File: width "
                                "and height should range from 5 to "
                                "7!")
    #Function to implement each resource coordinate to the list of resources
    def check_resource_coords(resource_string_name, resource_coords,\
                                resource_list_variable, line):
        if line == resource_string_name:
          resource_list_variable = []
          return(resource_list_variable)
        else:
          string = resource_string_name + " "
          resource_coords = line.strip(string)
          string = string.strip(": ")
          resource_list_variable = set_coords(resource_coords, string)
          return(resource_list_variable)

    #Checking for each resource and adding it to the list of resources
    if line[0:2] == "Wa":
      waters = check_resource_coords("Water:", "water", "waters", line)
      continue
    if line[0:2] == "Wo":
      woods = check_resource_coords("Wood:", "wood", "woods", line)
      continue
    if line[0:2] == "Fo":
      foods = check_resource_coords("Food:", "food", "foods", line)
      continue
    if line[0:2] == "Go":
      golds = check_resource_coords("Gold:", "gold", "golds", line)
      continue
    else:
      config.close()
      break

  width, height = board_width, board_height
  print("Configuration file {} was loaded.".format(filepath))
  return(width, height, waters, woods, foods, golds, current_coords,
            home_base_coords, p1_surrounding_coords, p2_surrounding_coords)

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python3 little_battle.py <filepath>")
    sys.exit()
  width, height, waters, woods, foods, golds, resource_occupied_spaces,\
  home_base_coords, p1_surrounding_coords, p2_surrounding_coords =\
  load_config_file(sys.argv[1])

  #Defining a dictionary that whit each key relating to a coordinate
  map_dict = {}
  key = ""
  for column in range(0, width):
    key += str(column)
    for row in range(0, height):
      key += str(row)
      map_dict[int(key)] = "  "
      key = str(column)
    key = ""

  #A function that prints the map using the map dictionary
  def print_current_game_state():
    if width == 5:
      print("  X00 01 02 03 04X")
      print(" Y+--------------+")
      for row in range(0, height):
        col_num = "0" + str(row)
        print(col_num + "|{}|{}|{}|{}|{}|".format(map_dict[int("0"+\
                str(row))], map_dict[int("1"+str(row))], map_dict\
                [int("2"+str(row))], map_dict[int("3"+str(row))],\
                map_dict[int("4"+str(row))]))
      print(" Y+--------------+")
    if width == 6:
      print("  X00 01 02 03 04 05X")
      print(" Y+-----------------+")
      for row in range(0, height):
        col_num = "0" + str(row)
        print(col_num + "|{}|{}|{}|{}|{}|{}|".format(map_dict[int("0"+str\
                (row))], map_dict[int("1"+str(row))],map_dict[int("2"+str\
                (row))], map_dict[int("3"+str(row))], map_dict[int("4"+str\
                (row))],map_dict[int("5"+str(row))]))
      print(" Y+-----------------+")
    if width == 7:
      print("  X00 01 02 03 04 05 06X")
      print(" Y+--------------------+")
      for row in range(0, height):
        col_num = "0" + str(row)
        print(col_num + "|{}|{}|{}|{}|{}|{}|{}|".format(map_dict[int("0"+str\
        (row))], map_dict[int("1"+str(row))], map_dict[int("2"+str(row))],\
        map_dict[int("3"+str(row))], map_dict[int("4"+str(row))], map_dict\
        [int("5"+str(row))], map_dict[int("6"+str(row))]))
      print(" Y+--------------------+")

  #Defining a function to print the prices of the units
  def print_prices():
    print("Recruit Prices:\n"
            "  Spearman (S) - 1W, 1F\n"
            "  Archer (A) - 1W, 1G\n"
            "  Knight (K) - 1F, 1G\n"
            "  Scout (T) - 1W, 1F, 1G")

  #Defining a funtion to print the current players resources
  def print_current_player_resources(player_num):
    if player_num == 1:
      f_count = p1_resources.count("F")
      g_count = p1_resources.count("G")
      w_count = p1_resources.count("W")
      print("[Your Asset: Wood - {} Food - {} Gold - {}]".format\
            (w_count, f_count, g_count))
    else:
      f_count = p2_resources.count("F")
      g_count = p2_resources.count("G")
      w_count = p2_resources.count("W")
      print("[Your Asset: Wood - {} Food - {} Gold - {}]".format\
            (w_count, f_count, g_count))

  year = 617

  #Game setup
  map_dict[11] = "H1"   #Implementing H1 to map
  base_2_coords = int(str(home_base_coords[1][0])+str(home_base_coords[1][1]))
  map_dict[base_2_coords] = "H2"    #Implementing H2 to map

  #Defining a funtion to add each resource point to the map dictionary
  def add_resource_to_map(resource, symbol):
    for coords in resource:
      key = ""
      key += str(coords[0])+str(coords[1])
      map_dict[int(key)] = symbol

  add_resource_to_map(waters, "~~")
  add_resource_to_map(woods, "WW")
  add_resource_to_map(foods, "FF")
  add_resource_to_map(golds, "GG")
  print("Game Started: Little Battle! (enter QUIT to quit the game)\n")
  print("Please check the battlefield, commander.")
  print_current_game_state()
  print("(enter DIS to display the map)\n")
  print_prices()
  print("(enter PRIS to display the price list)\n")

  p1 = [map_dict[11]]   #Player 1 base
  p2 = [map_dict[base_2_coords]]    #Player 2 base
  #Defining player resources
  p1_resources = ["W", "W", "F", "F", "G", "G"]
  p2_resources = ["W", "W", "F", "F", "G", "G"]
  #A list to store each players current units and their coordinates
  p1_units = []
  p2_units = []
  #A list to store each players units they are yet to place ater purchasing
  p1_unit_to_place = []
  p2_unit_to_place = []
  player_turn = 1
  p1_pieces = ["A1", "K1", "T1", "S1"]
  p2_pieces = ["A2", "K2", "T2", "S2"]

  #A class for the units
  class Units:
    def __init__(self, name, reach, cost, def_by, defs, p1_name, p2_name):
      self.name = name
      self.reach = reach
      self.cost = cost
      self.defeatedby = def_by
      self.defeats = defs
      self.p1 = p1_name
      self.p2 = p2_name

    #Defining a function that handles the battles between units
    def battle(unit_one, unit_two, start, key, player_turn):
      coords = str(key)
      #Turning the map key into a coordinate
      if len(coords) == 1:
        coord = [0, int(coords[0])]
      else:
        coord = [int(coords[0]), int(coords[1])]
      #Checking to see which unit loses
      if unit_one.name == unit_two.name:    #Both units lose
        print("We destroyed the enemy {} with massive loss!".format\
                (unit_two.name))
        if player_turn == 1:
          p1_units.remove([unit_one.name, start])
          p2_units.remove([unit_two.name, coord])
          player_current_units.remove([unit_one.name, start])
        else:
          p1_units.remove([unit_two.name, coord])
          p2_units.remove([unit_one.name, start])
          player_current_units.remove([unit_one.name, start])
        map_dict[key] = "  "
      if unit_one.name in unit_two.defeatedby:  #Moving unit wins
        print("Great! We defeated the enemy {}!".format(unit_two.name))
        if player_turn == 1:
          p2_units.remove([unit_two.name, coord])
          map_dict[key] = unit_one.p1
          player_current_units.remove([unit_one.name, start])
          i = p1_units.index([unit_one.name, start])
          p1_units[i][1] = coord
        else:
          p1_units.remove([unit_two.name, coord])
          map_dict[key] = unit_one.p2
          player_current_units.remove([unit_one.name, start])
          i = p2_units.index([unit_one.name, start])
          p2_units[i][1] = coord
      if unit_one.name in unit_two.defeats: #Moving unit loses
        print("We lost the army {} due to your command!".format(unit_one.name))
        if player_turn == 1:
          p1_units.remove([unit_one.name, start])
          player_current_units.remove([unit_one.name, start])
        else:
          p2_units.remove([unit_one.name, start])
          player_current_units.remove([unit_one.name, start])
      return

    #Defining a function that handles the purchasing of units
    def purchase(unit, player_resources, player_num):
      #Checking to make sure player has enough resources for unit
      for resource in unit.cost:
        if resource not in player_resources:
          print("Insufficient resources. Try again.")
          return(-1)
        else:
          continue
      #Adding unit to player inventory
      if player_num == 1:
        p1_unit_to_place.append(unit.p1)
        for resource in unit.cost:
          p1_resources.remove(resource)
      else:
        p2_unit_to_place.append(unit.p2)
        for resource in unit.cost:
          p2_resources.remove(resource)
      return

    #A function to handle the placement of newly purchased units
    def place_purchase_unit(unit, player_num):
      while True:
        coords = input("You want to recruit a {}. Enter two integers"
                        " as format ‘x y’ to place your army.\n"\
                        .format(unit.name))
        #Checking for DIS, QUIT, PRIS or invalid inputs
        if coords == "QUIT":
          exit()
        if coords == "DIS":
          print("Please check the battlefield, commander.")
          print_current_game_state()
          print()
          continue
        if coords == "PRIS":
          print_prices()
          print()
          continue
        if coords == "":
          print("Sorry, invalid input. Try again.\n")
          continue
        i = 0
        #Turning input into a coordinate
        while i < len(coords):
          if coords[i] == " ":
            x_value = coords[0:i]
            y_value = coords[i+1:]
            break
          i += 1
        if i == len(coords):
          print("Sorry, invalid input. Try again.\n")
          continue
        try:
          int(x_value)
          int(y_value)
        except ValueError:
          print("Sorry, invalid input. Try again.\n")
          continue
        coord = [int(x_value), int(y_value)]
        #Checking to see if coordinate is in position surrounding the players
        #base and if so, placing the unit on the map
        if player_num == 1:
          if coord in p1_surrounding_coords:
            key = int(str(coord[0])+str(coord[1]))
            if map_dict[key] == "  ":
              map_dict[key] = unit.p1
              p1_units.append([unit.name, coord])
              p1_unit_to_place.remove(unit.p1)
              print()
              print("You has recruited a {}.\n".format(unit.name))
              break
            else:
              print("You must place your newly recruited unit"
                    " in an unoccupied position next to your"
                    " home base. Try again.\n")
          else:
            print("You must place your newly recruited unit in an"
                    " unoccupied position next to your home base."
                    " Try again.\n")
        else:
          if coord in p2_surrounding_coords:
            key = int(str(coord[0])+str(coord[1]))
            if map_dict[key] == "  ":
              map_dict[key] = unit.p2
              p2_units.append([unit.name, coord])
              p2_unit_to_place.remove(unit.p2)
              print()
              print("You has recruited a {}.\n".format(unit.name))
              break
            else:
              print("You must place your newly recruited unit"
                    " in an unoccupied position next to your"
                    " home base. Try again.\n")
          else:
            print("You must place your newly recruited unit in an"
                  " unoccupied position next to your home base."
                  " Try again.\n")

    #A function to handle the movement of units
    def move_unit(unit, start, to, player_turn, p1_resources,\
                        p2_resources, p1_units, p2_units):
      #Turning from and to coordinates into a key
      #to use with the map dictionary
      from_key = (str(start[0])+str(start[1]))
      to_key = (str(to[0])+str(to[1]))
      passes_key = ""
      unit_start_coord = [int(start[0]),int(start[1])]
      unit_to_coord = [int(to[0]),int(to[1])]
      if player_turn == 1:
        player_resources = p1_resources
      else:
        player_resources = p2_resources
      while True:
        #If unit is a Scout, define a key for the space that is moved over
        if unit.name == "Scout":
          if (0>int(to_key[0]) or int(to_key[0])>=width or\
              0>int(to_key[1]) or int(to_key[1])>=height):
            print("Invalid move. Try again.")
            return
          if int(from_key[0]) == int(to_key[0]):
            if not((int(to_key[1]) == int(from_key[1])-1) or\
                    (int(to_key[1]) == int(from_key[1])+1) or\
                    (int(to_key[1]) == int(from_key[1])-2) or\
                    (int(to_key[1]) == int(from_key[1])+2)):
              print("Invalid move. Try again.")
              return
            if int(to_key[1]) == int(from_key[1])+2:
              passes_key = int(str(to_key[0])+\
                                str(int(from_key[1])+1))
            if int(to_key[1]) == int(from_key[1])-2:
              passes_key = int(str(to_key[0])+\
                                str(int(from_key[1])-1))
          elif int(from_key[1]) == int(to_key[1]):
            if not((int(to_key[0]) == int(from_key[0])-1) or\
                    (int(to_key[0]) == int(from_key[0])+1) or\
                    (int(to_key[0]) == int(from_key[0])-2) or\
                    (int(to_key[0]) == int(from_key[0])+2)):
              print("Invalid move. Try again.")
              return
            if int(to_key[0]) == int(from_key[0])+2:
              passes_key = int((str(int(from_key[0])+1)+str(to_key[1])))
            if int(to_key[0]) == int(from_key[0])-2:
              passes_key = int((str(int(from_key[0])-1)+str(to_key[1])))
        else:
          if int(from_key[0]) == int(to_key[0]):
            if not(int(to_key[1]) == (int(from_key[1])-1) or\
                    (int(to_key[1]) == int(from_key[1])+1)):
              print("Invalid move. Try again.")
              return
          elif int(from_key[1]) == int(to_key[1]):
            if not((int(to_key[0]) == (int(from_key[0])-1)) or\
                    (int(to_key[0]) == int(from_key[0])+1)):
              print("Invalid move. Try again.")
              return
        break
      start_coord = "(" + str(start[0]) + ", " + str(start[1]) + ")"
      to_coord = "(" + str(to[0]) + ", " + str(to[1]) + ")"
      to_key = int(to_key)
      from_key = int(from_key)
      #Checking for more invalid moves
      if player_turn == 1:
        if map_dict[to_key] in p1_pieces:
          print("Invalid move. Try again.")
          return
        if map_dict[to_key] == "H1":
          print("Invalid move. Try again.")
          return
      else:
        if map_dict[to_key] in p2_pieces:
          print("Invalid move. Try again.")
          return
        if map_dict[to_key] == "H2":
          print("Invalid move. Try again.")
          return
      #If no invalid moves have been made, will print the message
      print()
      print("You have moved {} from {} to {}.".format(unit.name, start_coord,\
            to_coord))
      map_dict[from_key] = "  "
      if passes_key != "":
        #Checking to see if Scout is lost moving over water
        if map_dict[passes_key] == "~~":
          print("We lost the army {} due to your command!".format(unit.name))
          if player_turn == 1:
            for units in p1_units:
              if unit.name == units[0]:
                if (int(units[1][0]) == int(start[0]) and\
                    int(units[1][1]) == int(start[1])):
                  p1_units.remove(units)
                  player_current_units.remove(units)
            return(p1_units)
          else:
            for units in p2_units:
              if unit.name == units[0]:
                if (int(units[1][0]) == int(start[0]) and\
                    int(units[1][1]) == int(start[1])):
                  p2_units.remove(units)
                  player_current_units.remove(units)
            return(p2_units)
        #Checking to see if Scout is moving over a space with enemy unit
        if (map_dict[passes_key] in p1_pieces) or\
            (map_dict[passes_key] in p2_pieces):
          #If opposite player Scout on passing space, then run battle function
          if player_turn == 1:
            if map_dict[passes_key] in p2_pieces:
              if map_dict[passes_key] == "A2":
                Units.battle(T, A, start, passes_key, 1)
              if map_dict[passes_key] == "S2":
                Units.battle(T, S, start, passes_key, 1)
              if map_dict[passes_key] == "K2":
                Units.battle(T, K, start, passes_key, 1)
              if map_dict[passes_key] == "T2":
                Units.battle(T, T, start, passes_key, 1)
              return(p1_units, p2_units)
          if player_turn == 2:
            if map_dict[passes_key] in p1_pieces:
              if map_dict[passes_key] == "A1":
                Units.battle(T, A, start, passes_key, 2)
              if map_dict[passes_key] == "S1":
                Units.battle(T, S, start, passes_key, 2)
              if map_dict[passes_key] == "K1":
                Units.battle(T, K, start, passes_key, 2)
              if map_dict[passes_key] == "T1":
                Units.battle(T, T, start, passes_key, 2)
              return(p1_units, p2_units)
        #Checking to see if Scout moves over a resource
        if player_turn == 1:
          if map_dict[passes_key] == "WW":
            Units.collect_resource("Wood", "W", p1_resources)
            map_dict[passes_key] = "  "
          if map_dict[passes_key] == "FF":
            Units.collect_resource("Food", "F", p1_resources)
            map_dict[passes_key] = "  "
          if map_dict[passes_key] == "GG":
            Units.collect_resource("Gold", "G", p1_resources)
            map_dict[passes_key] = "  "
        if player_turn == 2:
          if map_dict[passes_key] == "WW":
            Units.collect_resource("Wood", "W", p2_resources)
            map_dict[passes_key] = "  "
          if map_dict[passes_key] == "FF":
            Units.collect_resource("Food", "F", p2_resources)
            map_dict[passes_key] = "  "
          if map_dict[passes_key] == "GG":
            Units.collect_resource("Gold", "G", p2_resources)
            map_dict[passes_key] = "  "
        #Checking to see if Scout moves over the enemy base, winning the game
        if player_turn == 1:
          if map_dict[passes_key] == "H2":
            player_win(year, 1, unit)
        if player_turn == 2:
          if map_dict[passes_key] == "H1":
            player_win(year, 2, unit)
      #Now checking where the unit has moved to
      #Checking to see if unit moves to the enemy base, winning the game
      if player_turn == 1:
        if map_dict[to_key] == "H2":
          player_win(year, 1, unit)
      if player_turn == 2:
        if map_dict[to_key] == "H1":
          player_win(year, 2, unit)
      #Checking to see if unit moves to water and is lost
      if map_dict[to_key] == "~~":
        print("We lost the army {} due to your command!".format(unit.name))
        if player_turn == 1:
          for units in p1_units:
            if unit.name == units[0]:
              if (int(units[1][0]) == int(start[0]) and\
                  int(units[1][1]) == int(start[1])):
                p1_units.remove(units)
                player_current_units.remove(units)
          return(p1_units)
        else:
          for units in p2_units:
            if unit.name == units[0]:
              if (int(units[1][0]) == int(start[0]) and\
                  int(units[1][1]) == int(start[1])):
                p2_units.remove(units)
                player_current_units.remove(units)
          return(p2_units)
      #If the new space is a resource, it will be collected accordingly
      if player_turn == 1:
        if map_dict[to_key] == "WW":
          Units.collect_resource("Wood", "W", p1_resources)
          p1_units =\
          update_map_key(1, unit, unit_start_coord, unit_to_coord, to_key,\
                            p1_units, player_current_units)
        if map_dict[to_key] == "FF":
          Units.collect_resource("Food", "F", p1_resources)
          p1_units =\
          update_map_key(1, unit, unit_start_coord, unit_to_coord, to_key,\
                            p1_units, player_current_units)
        if map_dict[to_key] == "GG":
          Units.collect_resource("Gold", "G", p1_resources)
          p1_units =\
          update_map_key(1, unit, unit_start_coord, unit_to_coord, to_key,\
                            p1_units, player_current_units)
      else:
        if map_dict[to_key] == "WW":
          Units.collect_resource("Wood", "W", p2_resources)
          p2_units =\
          update_map_key(2, unit, unit_start_coord, unit_to_coord, to_key,\
                            p2_units, player_current_units)
        if map_dict[to_key] == "FF":
          Units.collect_resource("Food", "F", p2_resources)
          p2_units =\
          update_map_key(2, unit, unit_start_coord, unit_to_coord, to_key,\
                            p2_units, player_current_units)
        if map_dict[to_key] == "GG":
          Units.collect_resource("Gold", "G", p2_resources)
          p2_units =\
          update_map_key(2, unit, unit_start_coord, unit_to_coord, to_key,\
                            p2_units, player_current_units)
      if map_dict[to_key] == "  ":
        if player_turn == 1:
          p1_units =\
          update_map_key(1, unit, unit_start_coord, unit_to_coord, to_key,\
                            p1_units, player_current_units)
        else:
          p2_units =\
          update_map_key(2, unit, unit_start_coord, unit_to_coord, to_key,\
                            p2_units, player_current_units)
      #If the new space if an enemy unit, run the battle function accordingly
      if (map_dict[to_key] in p1_pieces) or\
            (map_dict[to_key] in p2_pieces):
        if player_turn == 1:
          if map_dict[to_key] in p2_pieces:
            if map_dict[to_key] == "A2":
              Units.battle(unit, A, start, to_key, 1)
            if map_dict[to_key] == "S2":
              Units.battle(unit, S, start, to_key, 1)
            if map_dict[to_key] == "K2":
              Units.battle(unit, K, start, to_key, 1)
            if map_dict[to_key] == "T2":
              Units.battle(unit, T, start, to_key, 1)
        else:
          if map_dict[to_key] in p1_pieces:
            if map_dict[to_key] == "A1":
              Units.battle(unit, A, start, to_key, 2)
            if map_dict[to_key] == "S1":
              Units.battle(unit, S, start, to_key, 2)
            if map_dict[to_key] == "K1":
              Units.battle(unit, K, start, to_key, 2)
            if map_dict[to_key] == "T1":
              Units.battle(unit, T, start, to_key, 2)
      #If not done so already, return each players unit and resource lists
      if player_turn == 1:
        p1_resources = player_resources
        return(p1_units, p2_units, p1_resources)
      else:
        p2_resources = player_resources
        return(p1_units, p2_units, p2_resources)

    #A function that adds resources to the players inventory
    def collect_resource(name, resource, resources):
      resources.append(resource)
      resources.append(resource)
      print("Good. We collected 2 {}.".format(name))

  #Defining each unit in their class
  S = Units("Spearman", 1, ["W", "F"], ["Archer"], ["Knight", "Scout"],\
            "S1", "S2")
  A = Units("Archer", 1, ["W", "G"], ["Knight"], ["Spearman", "Scout"],\
            "A1", "A2")
  K = Units("Knight", 1, ["F", "G"], ["Spearman"], ["Archer", "Scout"],\
            "K1", "K2")
  T = Units("Scout", 2, ["W", "F", "G"], ["Spearman", "Archer", "Knight"],\
            [], "T1", "T2")

  #A function that handles the victory of a player
  def player_win(year, player_num, unit):
      print("The army {} captured the enemy’s capital.\n".format(unit.name))
      name = input("What’s your name, commander?\n")
      print()
      print("***Congratulation! Emperor {} unified the country in {}.***"\
            .format(name, year))
      exit()

  #A function that is used to change player turn, and year if needed
  def change_player_turn(player_turn, year):
    if player_turn == 1:
      player_turn = 2
    else:
      player_turn = 1
      year +=1
    return(player_turn, year)

  #A function that updates that map dictionary after a unit has moved
  def update_map_key(player_turn, unit, start_coord, end_coord, end_key,\
                        player_units, player_current_units):
    player_current_units.remove([unit.name, start_coord])
    i = player_units.index([unit.name, start_coord])
    player_units[i][1] = end_coord
    if player_turn == 1:
      map_dict[end_key] = unit.p1
    else:
      map_dict[end_key] = unit.p2
    return(player_units)

  # The loop that runs through the game
  while True:
    print("-Year {}-\n".format(year))
    while True:
      print("+++Player {}'s Stage: Recruit Armies+++\n".format(str\
            (player_turn)))
      #Defining the current players resources
      if player_turn == 1:
        current_player_resources = p1_resources
      else:
        current_player_resources = p2_resources
      if len(current_player_resources) != 0:
        print_current_player_resources(player_turn)
        while True:
          #Checkig to see if the player can make any purchases
          can_purchase_scout = True
          can_purchase_archer = True
          can_purchase_knight = True
          can_purchase_spearman = True
          if len(current_player_resources) != 0:
            for resource in S.cost:
              if resource not in current_player_resources:
                  can_purchase_spearman = False
            for resource in A.cost:
              if resource not in current_player_resources:
                  can_purchase_archer = False
            for resource in K.cost:
              if resource not in current_player_resources:
                  can_purchase_knight = False
            for resource in T.cost:
              if resource not in current_player_resources:
                  can_purchase_scout = False
            if can_purchase_scout == False and can_purchase_archer == False\
                and can_purchase_knight == False and can_purchase_spearman\
                == False:
              #Negative case, move onto move army stage
              print("No resources to recruit any armies.")
              break
          #Checking to see if player has any valid places to put their new unit
          if player_turn == 1:
            for i in p1_surrounding_coords:
              key = int(str(i[0])+str(i[1]))
              if map_dict[key] == "  ":
                d = 0
                break
              else:
                d = 1
                continue
            if d == 1:
              #Negative case, move onto move army stage
              print("No place to recruit new armies.")
              break
          if player_turn == 2:
            for i in p2_surrounding_coords:
              key = int(str(i[0])+str(i[1]))
              if map_dict[key] == "  ":
                d = 0
                break
              else:
                d = 1
                continue
            if d == 1:
              #Negative case, move onto move army stage
              print("No place to recruit new armies.")
              break
          print()
          #Asking for a unit choice
          unit_choice = input("Which type of army to recruit,"
                                " (enter) ‘S’, ‘A’, ‘K’, or ‘T’? Enter"
                                " ‘NO’ to end this stage.\n")
          #Player gives correct input, run function to purchase the unit
          if unit_choice == "S" or unit_choice == "T" or\
            unit_choice == "K" or unit_choice == "A":
            if player_turn == 1:
              if unit_choice == "S":
                #Function will return -1 if the player can't afford this unit
                a = Units.purchase(S, p1_resources, 1)
                if a != -1:
                  print()
                  Units.place_purchase_unit(S, 1)
              elif unit_choice == "K":
                a = Units.purchase(K, p1_resources, 1)
                if a != -1:
                  print()
                  Units.place_purchase_unit(K, 1)
              elif unit_choice == "A":
                a = Units.purchase(A, p1_resources, 1)
                if a != -1:
                  print()
                  Units.place_purchase_unit(A, 1)
              else:
                a = Units.purchase(T, p1_resources, 1)
                if a != -1:
                    print()
                    Units.place_purchase_unit(T, 1)
            else:
              if unit_choice == "S":
                a = Units.purchase(S, p2_resources, 2)
                if a != -1:
                  print()
                  Units.place_purchase_unit(S, 2)
              elif unit_choice == "K":
                a = Units.purchase(K, p2_resources, 2)
                if a != -1:
                  print()
                  Units.place_purchase_unit(K, 2)
              elif unit_choice == "A":
                a = Units.purchase(A, p2_resources, 2)
                if a != -1:
                  print()
                  Units.place_purchase_unit(A, 2)
              else:
                a = Units.purchase(T, p2_resources, 2)
                if a != -1:
                  print()
                  Units.place_purchase_unit(T, 2)
            if len(current_player_resources) == 0:
              print_current_player_resources(player_turn)
              #Negative case, move onto move army stage
              print("No resources to recruit any armies.")
              break
            if a == -1:
              continue
            print_current_player_resources(player_turn)
            continue
          #Checking for DIS, QUIT, PRIS or invalid inputs
          else:
            if unit_choice == "QUIT":
              exit()
            elif unit_choice == "DIS":
              print("Please check the battlefield, commander.")
              print_current_game_state()
              continue
            elif unit_choice == "PRIS":
              print_prices()
              continue
            elif unit_choice == "NO":
              player_current_units = []
              break
            else:
              #Invalid input given, will ask again
              print("Sorry, invalid input. Try again.")
        break
      else:
        #Negative case, move onto move army stage
        print_current_player_resources(player_turn)
        print("No resources to recruit any armies.")
      break
    print()
    #Move armies stage
    print("===Player {}'s Stage: Move Armies===".format(str(player_turn)))
    player_current_units = []
    #Assigning a list tha tracks the current units
    #eligible to move on a given turn: player_current_units
    if player_turn == 1:
      for units in p1_units:
          player_current_units.append(units)
    else:
      for units in p2_units:
          player_current_units.append(units)
    while True:
      if len(player_current_units) == 0:
        print()
        #If no armies to move in given turn, change player turn
        print("No Army to Move: next turn.\n")
        player_turn, year = change_player_turn(player_turn, year)
        break
      print()

      while True:
        print("Armies to Move:")
        knight_coords = []
        spearman_coords = []
        archer_coords = []
        scout_coords = []
        #Adding the coordinates of each units of the player in order to print
        for unit in player_current_units:
          if unit[0] == "Spearman":
            coord = "(" + str(unit[1][0]) + ", " +str(unit[1][1])+ ")"
            spearman_coords.append(coord)
          if unit[0] == "Archer":
            coord = "(" + str(unit[1][0]) + ", " +str(unit[1][1])+ ")"
            archer_coords.append(coord)
          if unit[0] == "Knight":
            coord = "(" + str(unit[1][0]) + ", " +str(unit[1][1])+ ")"
            knight_coords.append(coord)
          if unit[0] == "Scout":
            coord = "(" + str(unit[1][0]) + ", " +str(unit[1][1])+ ")"
            scout_coords.append(coord)
        #Converting the coordinate from a list item to a string, (x, y)
        if len(spearman_coords) > 0:
          x = ""
          for coord in spearman_coords:
            x += coord + ", "
          x = x[:-2]
          print("  Spearman: " + x)
        if len(archer_coords) > 0:
          x = ""
          for coord in archer_coords:
            x += coord + ", "
          x = x[:-2]
          print("  Archer: " + x)
        if len(knight_coords) > 0:
          x = ""
          for coord in knight_coords:
            x += coord + ", "
          x = x[:-2]
          print("  Knight: " + x)
        if len(scout_coords) > 0:
          x = ""
          for coord in scout_coords:
            x += coord + ", "
          x = x[:-2]
          print("  Scout: " + x)
        print()
        #Asking for an input for the unit move
        move = input("Enter four integers as a format ‘x0 y0 x1 y1’"
                        " to represent move unit from (x0, y0) to"
                        " (x1, y1) or ‘NO’ to end this turn.\n")
        moves = []
        d = 0
        #Checking for DIS, QUIT, PRIS or invalid inputs
        if move == "QUIT":
          exit()
        elif move == "DIS":
          print("Please check the battlefield, commander.")
          print_current_game_state()
          break
        elif move == "PRIS":
          print_prices()
          break
        elif move == "NO":
          player_current_units = []
          break
        elif move.isspace() == True:
          print("Invalid move. Try again.")
          break
        elif move == "":
          print("Invalid move. Try again.")
          break
        j = 0
        i = 0
        #Turning the input into a to and from coordinate
        #and checking its validity
        while i < len(move):
          if move[i] == " ":
            moves.append(str(move[j:i]))
            j = i+1
          i += 1
        if move[i-1] != " ":
            moves.append(str(move[j:i]))
        if len(moves) != 4: #If more than 4 values are given ask again
          print("Invalid move. Try again.\n")
          continue
        for num in moves:
          try:
            int(num)
          except ValueError:    #If values aren't integers ask again
            print("Invalid move. Try again.")
            e = 1
            break
          else:
            e = 0
        if e == 0:
          if (0<int(moves[2]) and int(moves[2])>width and\
            0<int(moves[3]) and int(moves[3])>height):
            print("Invalid move. Try again.\n")
            continue
        elif e == 1:
          break
        #Checking to see if the from coordinate matches
        #any of the player's unit's positions
        for unit in player_current_units:
          if ((int(moves[0]) == int(unit[1][0])) and (int(moves[1])
                == int(unit[1][1]))):
            from_coord = [int(moves[0]), int(moves[1])]
            to_coord = [int(moves[2]), int(moves[3])]
            d = 1
            #Moving the according unit using the move_unit function
            if unit[0] == "Archer":
              Units.move_unit(A, from_coord, to_coord,player_turn,\
                              p1_resources, p2_resources, p1_units,\
                              p2_units)
              break
            if unit[0] == "Knight":
              Units.move_unit(K, from_coord, to_coord, player_turn,\
                              p1_resources, p2_resources, p1_units,\
                              p2_units)
              break
            if unit[0] == "Spearman":
              Units.move_unit(S, from_coord, to_coord, player_turn,\
                              p1_resources, p2_resources, p1_units,\
                              p2_units)
              break
            if unit[0] == "Scout":
              Units.move_unit(T, from_coord, to_coord, player_turn,\
                              p1_resources,p2_resources, p1_units,\
                              p2_units)
              break
            else:
              continue
        if d == 0:
          #If the from coordinate didn't match any units, ask again
          print("Invalid move. Try again.\n")
          continue
        else:
          break
      #If the player doesn't have any units left to move this turn,
      #change player turn
      if len(player_current_units) == 0:
        print()
        if move != "NO":
          print("No Army to Move: next turn.\n")
        player_turn, year = change_player_turn(player_turn, year)
        break
      #If the player still has units to move, ask again
      else:
        continue
