## Engineering conventions

Do not invent missing physical dimensions or engineering assumptions.

Before implementing the I-section model, define and document:

- member length;
- overall section depth;
- flange width;
- flange thickness;
- web thickness;
- any modelled root/corner radius;
- coordinate-axis convention; and
- unit convention.

Abaqus has no inherent unit system. All generated values must use one
documented, internally consistent unit system.

Validate perforations before meshing. At minimum reject:

- perforations outside the web;
- perforations intersecting a flange;
- invalid dimensions or corner radii;
- overlapping perforations unless explicitly supported; and
- geometries that cannot satisfy the required mesh constraints.

Keep element-selection logic in one place. Do not scatter hard-coded element
types throughout the writer.

Element selection must consider the analysis assumptions and current Abaqus
element capabilities, not merely whether an element is linear or quadratic.
Permit an explicit user override where technically valid.

Mesh generation must follow the principles in the reference PDF:

- appropriate refinement near perforations;
- regular element patterns where possible;
- controlled element aspect ratios;
- compatibility between hole-region and base meshes;
- mesh-quality checking; and
- remeshing or a clear validation error when constraints cannot be satisfied.

Do not use arbitrary geometric-imperfection amplitudes. Imperfection shape,
mode number, magnitude, and source must be explicit.

Residual stresses, if supported, must be an explicit optional modelling feature
with a documented distribution and Abaqus implementation.

Create node and element sets geometrically using tolerances rather than relying
on exact floating-point equality.

Keep geometry/mesh generation independent from Abaqus `.inp` serialization so
that geometry and mesh logic can be tested without parsing text files.