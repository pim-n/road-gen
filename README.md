# RoadGen

Generate road segments in a 2D Cartesian plane.

## Installation

Ensure you have Python `>= 3.12` installed. Clone the repository using

```
git clone git@github.com:pim-n/road-gen.git
cd road-gen
```

or

```
git clone https://github.com/pim-n/road-gen.git
cd road-gen
```

then, with a virtual environment (Python `>= 3.12`) active:

```
pip install .
```

## Usage

Within the virtual environment you can now run the `road-gen` command:

```
road-gen --help
```

## Example - random road

A minimal random road needs a length $L$, step size $\Delta s$ and velocity $v$:

```
road-gen random --length 1000 --ds 10 --velocity 10
```

or in short form

```
road-gen random -l 1000 -s 10 -v 10
```

This will show the resulting random road in a plot, but it's not saved after you close the window. To save the results, add the `--save` flag

```
road-gen random -l 1000 -s 10 -v 10 --save
```

which will produce 3 files starting with the unique seed number used to generate the road.

## Reproducability

You can reproduce results by adding a seed with the `--seed` flag.

## Other

For more info, just see `road-gen --help` or `road-gen random --help`.