from arguments.parser import parser
from enums.directions import Directions
from rubik import Rubik
from enums.faces import Faces

if __name__ == '__main__':
    args = parser.parse_args()

    rubik = Rubik(args.options.n)
    print(rubik.cube)
    rubik.move(Directions.TOP_LEFT)
    print(rubik.cube)
    rubik.move(Directions.TOP_RIGHT)
    print(rubik.cube)