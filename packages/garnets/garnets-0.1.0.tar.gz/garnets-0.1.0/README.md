
## Introduction

`garnets` is a very simple wrapper over the
[garnett](https://github.com/glotzerlab/garnett) package. In version
0.7, the API of garnett changed to rename some frame attributes
(positions, orientations, velocities) to their singular
form.

## Usage

`garnets` is mostly designed to be a drop-in replacement for the
garnett import at the top of your file:

```
import garnets as garnett
```

## Caveats

At the moment, only a basic compatibility layer is supported. Writing
trajectories using frame objects that fulfill only the old frame API
will not work, but writing frames that are read from a `garnets` or
`garnett` trajectory should work.