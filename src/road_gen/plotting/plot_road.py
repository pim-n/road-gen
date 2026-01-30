from matplotlib import pyplot as plt

from ..generators.random_road_generator import RandomRoadGenerator
from ..generators.segmented_road_generator import SegmentedRoadGenerator

def plot_road(
    x,
    y,
    generator: RandomRoadGenerator | SegmentedRoadGenerator,
    save: bool = False,
    filename: str = "out.jpg"
    ):

    plt.plot(x, y, '-b')
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
        
    title_str = (
        f"$L = {generator.length}$ m, " +
        f"$v = {generator.velocity}$ m/s, " +
        f"$\\Delta s = {generator.ds} m$"
                 )
        
    if isinstance(generator, RandomRoadGenerator):
        title_str += (
            "\n" + 
            f"Prob(straight) $= {generator.straight_section_prob}$, " +
            f"Max rel. size $= {generator.straight_section_max_rel_size}$"
        )
    else:
        title_str += (
            f"$, \\alpha = {generator.alpha}$" +
            "\n" +
            str(generator.segments)
            )

    plt.title(title_str)

    plt.tight_layout()
    
    if save:
        plt.savefig(filename)
    else:
        plt.show()