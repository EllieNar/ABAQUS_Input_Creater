## Buckling and nonlinear analysis

Treat eigenvalue buckling and nonlinear postbuckling as separate analysis
definitions.

Do not assume an eigenvalue buckling result is itself an ultimate capacity.

Nonlinear analyses that use eigenmodes as imperfections must preserve the
required model compatibility between the eigenvalue and nonlinear models.

Solution-control choices such as static general, stabilization, or Riks must
be explicit configuration rather than hidden defaults.

Any defaults derived from literature must identify their source.

## Bending

Three-point and four-point bending configurations require explicit definitions
of:

- support locations;
- load locations;
- load/application method;
- restrained degrees of freedom;
- lateral/torsional restraint assumptions; and
- whether rollers/contact, coupling, or equivalent nodal loading is used.

Do not choose these assumptions silently.

Bending-specific methodology not supported by the supplied reference PDF must
be researched from appropriate authoritative literature and Abaqus
documentation before implementation.