width = 5
height = 6


map_dict = {}
key = ""
for column in range(0, width):
  key += str(column)
  for row in range(0, height):
    key += str(row)
    map_dict[int(key)] = "  "
    key = str(column)
  key = ""


def print_current_game_state():
  col_num_line = ["  ", "X"]
  top_and_bottom_line = [" ", "Y+"]
  line_length = width*3-1
  #Adding labels for each column
  for column in range(0, width):
    col_num = "0" + str(column) + " "
    col_num_line.append(col_num)
  #Ammending last column lable to have and "X" at the end
  del col_num_line[-1]
  col_num = "0" + str(column) + "X"
  col_num_line.append(col_num)
  #Printing column label line
  for i in col_num_line:
    print(i, end="")
  print()
  j = 0
  #Adding the top and bottom border to a list to print later
  while j < line_length:
    top_and_bottom_line.append("-")
    j += 1
  top_and_bottom_line.append("+")
  #Printing top map border
  for k in top_and_bottom_line:
    print(k, end="")
  print()
  #Adding the each coordinate to a list to print
  for row in range(0, height):
    row_num = "0" + str(row)
    middle_lines = [row_num, "|"]
    for column in range(0, width):
      key = int(str(column)+str(row))
      middle_lines.append(map_dict[key])
      middle_lines.append("|")
    #Printing each line on the map
    for l in middle_lines:
      print(l, end="")
    print()
  #Printing the bottom map border
  for l in top_and_bottom_line:
    print(l, end="")
  print()

print_current_game_state()


map_dict[11] = "~~"
map_dict[32] = "FF"
map_dict[41] = "GG"

print_current_game_state()
