# Workflow analysis methods

## Software and interface

Use static analysis to find candidate behavior in manuals, screenshots, authorized code, and sample configurations. Use runtime observation to verify states through the normal interface with test data. Record the version, role, and starting state. Change one condition at a time and note which changes affect the outcome. A branch in source code suggests a hypothesis. An outcome observed during a test documents the tested configuration. [Awesome Reversing · Software](https://github.com/ReversingID/Awesome-Reversing/blob/master/software-reversing.md)

## Export formats

Compare two authorized exports made with a single input field changed. Record structure, field types, empty values, ordering, and differences. Use standard parsers for JSON and CSV. For a documented binary format, use an available declarative parser such as Kaitai Struct to inspect the structure. Cite the sample and field location. [Awesome Reversing · Format](https://github.com/ReversingID/Awesome-Reversing/blob/master/format-reversing.md)

## Data and schemas

For an authorized dump or SQLite copy, inspect the copy in read-only mode. Start with the schema. Use declared keys and constraints to form hypotheses about relationships. Verify visible behavior with test data and cite the relevant table and column. [Awesome Reversing · Database](https://github.com/ReversingID/Awesome-Reversing/blob/master/database-reversing.md)

For important rules, look for agreement between the observed workflow and the resulting artifact. When sources disagree, record the versions and conditions and keep the question open until the difference is explained.
