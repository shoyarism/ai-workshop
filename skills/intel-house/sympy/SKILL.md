---
name: sympy
description: "SymPy is a Python library for symbolic mathematics that enables exact computation using mathematical symbols rather than numerical approximations."
license: https://github.com/sympy/sympy/blob/master/LICENSE
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: "https://github.com/sympy/sympy"
---

# SymPy - Symbolic Mathematics in Python

## Overview

SymPy is a Python library for symbolic mathematics that enables exact computation using mathematical symbols rather than numerical approximations. This skill provides comprehensive guidance for performing symbolic algebra, calculus, linear algebra, equation solving, physics calculations, and code generation using SymPy.

## When to Use This Skill

Use this skill when:
- Solving equations symbolically (algebraic, differential, systems of equations)
- Performing calculus operations (derivatives, integrals, limits, series)
- Manipulating and simplifying algebraic expressions
- Working with matrices and linear algebra symbolically
- Doing physics calculations (mechanics, quantum mechanics, vector analysis)
- Number theory computations (primes, factorization, modular arithmetic)
- Geometric calculations (2D/3D geometry, analytic geometry)
- Converting mathematical expressions to executable code (Python, C, Fortran)
- Generating LaTeX or other formatted mathematical output
- Needing exact mathematical results (e.g., `sqrt(2)` not `1.414...`)

## Core Capabilities

### 1. Symbolic Computation Basics

**Creating symbols and expressions:**
```python
from sympy import symbols, Symbol
x, y, z = symbols('x y z')
expr = x**2 + 2*x + 1

# With assumptions
x = symbols('x', real=True, positive=True)
n = symbols('n', integer=True)
```

**Simplification and manipulation:**
```python
from sympy import simplify, expand, factor, cancel
simplify(sin(x)**2 + cos(x)**2)  # Returns 1
expand((x + 1)**3)  # x**3 + 3*x**2 + 3*x + 1
factor(x**2 - 1)    # (x - 1)*(x + 1)
```