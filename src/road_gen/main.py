import argparse

from matplotlib import pyplot as plt

from .generators.random_road_generator import RandomRoadGenerator
from .generators.segmented_road_generator import SegmentedRoadGenerator
from .plotting.plot_road import plot_road
from .prefabs import prefabs
from .utils import export

def add_common_args(parser):
    """Add common arguments to a subparser."""
    parser.add_argument("--length", "-l", type=int, required=True, help="Length of road in meters.")
    parser.add_argument("--ds", "-s", type=int, required=True, help="Step size in meters.")
    parser.add_argument("--velocity", "-v", type=float, required=True, help="Velocity in meters per second. Needed to determine the minimum radius of turns.")

    parser.add_argument("--mu", type=float, required=False, help="Friction coefficient. Defaults to 0.7, which represents dry asphalt.")
    parser.add_argument("--g", type=float, required=False, help="Acceleration due to gravitation. Defaults to 9.81 meters per second.")
    
    parser.add_argument("--seed", type=int, required=False, help="Fix a seed for reproducibility")
    parser.add_argument("--save", action="store_true", required=False, help="Save all outputs. If false, just plots.")
    
def main():
    parser = argparse.ArgumentParser(description="Generate stuff with two methods.")
    subparsers = parser.add_subparsers(dest="method", required=True)

    random_parser = subparsers.add_parser("random", help="Generate a random road according to parameters.")
    random_parser.add_argument("--straight_section_prob", type=float, required=False, help="Probability at every step i that a straight section will start. Defaults to 0.05.")
    random_parser.add_argument("--straight_section_max_rel_size", type=float, required=False, help="The maximum size that straight section(s) can have relative to the total length of the path. Defaults to 0.1.")
    add_common_args(random_parser)
    
    segment_parser = subparsers.add_parser("segments", help="Generate a road according to a list of segments.")
    segment_parser.add_argument("--segments", nargs="+", type=str, required=True, help=f"List of segments. Choose from {str(prefabs.PREFABS.keys())}")
    segment_parser.add_argument("--alpha", type=float, required=False, help="Dirichlet distribution concentration parameter. A high alpha distributes total length more evenly across segments.")
    add_common_args(segment_parser)
    
    args = parser.parse_args()

    try:
        if not all(v > 0 for v in (args.length, args.ds, args.velocity)):
            raise ValueError("Length, step size, and velocity must be positive values.")

        init_args = {
            "length": args.length,
            "ds": args.ds,
            "velocity": args.velocity,
        }

        if args.mu:
            init_args["mu"] = args.mu
        if args.g:
            init_args["g"] = args.g
        if args.seed:
            init_args["seed"] = args.seed

        generate_args = {}
        if args.method == "random":
            generator = RandomRoadGenerator(**init_args)
            
            if args.straight_section_prob:
                generate_args["straight_section_prob"] = float(args.straight_section_prob)
            if args.straight_section_max_rel_size:
                generate_args["straight_section_max_rel_size"] = float(args.straight_section_max_rel_size)

        elif args.method == "segments":
            generator = SegmentedRoadGenerator(**init_args)
            
            if args.alpha:
                generate_args["alpha"] = args.alpha
                
            generate_args["segments"] = list(args.segments)
            
        x, y = generator.generate(**generate_args)
        
        if args.save:
            basename = str(generator.seed)
            plot_road(x, y, generator, save = True, filename = basename+".jpg")
            export.coords_to_json(x, y, filename = basename+".json")
            export.params_to_json(generator, filename = basename+".params.json")
        else:
            plot_road(x, y, generator)

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()