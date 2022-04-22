from little_battle import load_config_file
# Don't remove any comments in this file
folder_path = "./invalid_files/"

# Please create appropriate invalid files in the folder "invalid_files"
# for each unit test according to the comments below and
# then complete them according to the function name


def test_file_not_found(filepath):
  # no need to create a file for FileNotFound
  try:
    load_config_file(folder_path + filepath)
  except FileNotFoundError:
    pass
  else:
    raise AssertionError("Should raise FileNotFoundError")

def test_format_error(filepath):
  # add "format_error_file.txt" in "invalid_files"
  try:
    load_config_file(folder_path + filepath)
  except SyntaxError:
    pass
  else:
    raise AssertionError("Should raise SyntaxError: Invalid Configuration"
                                "File: format error!")

def test_frame_format_error(filepath):
  # add "frame_format_error_file.txt" in "invalid_files"
  try:
    load_config_file(folder_path + filepath)
  except SyntaxError:
    pass
  except Exception:
    raise AssertionError("Should raise SyntaxError: Invalid Configuration"
                            "File: frame should be in format widthxheight!")

def test_frame_out_of_range(filepath):
  # add "format_out_of_range_file.txt" in "invalid_files"
  try:
    load_config_file(folder_path + filepath)
  except ArithmeticError:
    pass
  except Exception:
    raise AssertionError("Should raise ArithmeticError: Invalid"
                            " Configuration File: width and height should"
                            " range from 5 to 7!")

def test_non_integer(filepath):
  # add "non_integer_file.txt" in "invalid_files"
  try:
    load_config_file(folder_path + filepath)
  except SyntaxError:
    pass
  except Exception:
    raise AssertionError("Should raise SyntaxError: Invalid Configuration"
                            " File: frame should be in format"
                            " widthxheight!")

def test_out_of_map(filepath):
  # add "out_of_map_file.txt" in "invalid_files"
  try:
    load_config_file(folder_path + filepath)
  except ArithmeticError:
    pass
  except Exception:
    raise AssertionError("Should raise ArithmeticError: Invalid"
                            " Configuration File: <line_name> contains a"
                            " position that is out of map.")

def test_occupy_home_or_next_to_home(filepath_one, filepath_two):
  # add two invalid files: "occupy_home_file.txt" and
  # "occupy_next_to_home_file.txt" in "invalid_files"
  try:
    load_config_file(folder_path + filepath_one)
  except ValueError:
    pass
  except Exception:
    raise AssertionError("Should raise ValueError: Invalid Configuration"
                            " File: The positions of home bases or the"
                            " positions next to the home bases are"
                            " occupied!")
  try:
    load_config_file(folder_path + filepath_two)
  except ValueError:
    pass
  except Exception:
    raise AssertionError("Should raise ValueError: Invalid Configuration"
                            " File: The positions of home bases or the"
                            " positions next to the home bases are"
                            " occupied!")

def test_duplicate_position(filepath_one, filepath_two):
  # add two files: "dupli_pos_in_single_line.txt" and
  # "dupli_pos_in_multiple_lines.txt" in "invalid_files"
  try:
    load_config_file(folder_path + filepath_one)
  except SyntaxError:
    pass
  except Exception:
    raise AssertionError("Should raise SyntaxError: Invalid Configuration"
                            " File: Duplicate position (x, y)!")
  try:
    load_config_file(folder_path + filepath_two)
  except SyntaxError:
    pass
  except Exception:
    raise AssertionError("Should raise SyntaxError: Invalid Configuration"
                            " File: Duplicate position (x, y)!")


def test_odd_length(filepath):
  # add "odd_length_file.txt" in "invalid_files"
  try:
    load_config_file(folder_path + filepath)
  except SyntaxError:
    pass
  except Exception:
    raise AssertionError("Should raise SyntaxError: Invalid Configuration"
                            " File: <line_name> has an odd number of"
                            " elements!")

def test_valid_file(filepath):
  # no need to create file for this one, just test loading config.txt
  try:
    load_config_file(filepath)
  except Exception:
    raise AssertionError("Should print Configuration file config.txt"
                            " was loaded.")
  else:
    pass

# you can run this test file to check tests and load_config_file
if __name__ == "__main__":
  test_file_not_found("hello.txt")
  test_format_error("format_error_file.txt")
  test_frame_format_error("frame_format_error_file.txt")
  test_frame_out_of_range("format_out_of_range_file.txt")
  test_non_integer("non_integer_file.txt")
  test_out_of_map("out_of_map_file.txt")
  test_occupy_home_or_next_to_home("occupy_home_file.txt",\
                                    "occupy_next_to_home_file.txt")
  test_duplicate_position("dupli_pos_in_single_line.txt",\
                        "dupli_pos_in_multiple_lines.txt")
  test_odd_length("odd_length_file.txt")
  test_valid_file("config.txt")
