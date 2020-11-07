import pathlib
HOLDS_SETS = {'A','B','OS'}
SETUPS = ['2016'] # FIXME?
GRADES = ['6A', '6A+', '6B', '6B+', '6C', '6C+',
          '7A', '7A+', '7B', '7B+', '7C', '7C+',
          '8A', '8A+', '8B', '8B+'
          ]
DB_PATH = pathlib.Path(__file__).parent.absolute().joinpath("moon_problems.db")
