# Specification Equivalence

Formal verification and specification validation are separate assurance questions.

A proof checker answers a bounded question:

> Does the formal statement follow from the declared formal assumptions inside the declared proof system?

Scientific and engineering review must still answer:

> Does the formal statement faithfully represent the intended real-world, scientific, mathematical, or engineering claim?

The `FormalProofRecord` therefore carries two independent states:

1. `checker.state`
2. `specification_equivalence.state`

A checker `PASS` cannot automatically elevate an unresolved specification-equivalence review into overall discovery `PASS`.

This separation is mandatory because a perfectly checked proof of the wrong or incomplete formal statement is still insufficient evidence for the intended claim.
