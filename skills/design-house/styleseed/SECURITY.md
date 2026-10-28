# Security Policy

## Reporting a Vulnerability

StyleSeed is a design system (markdown rules, React components, CSS) with no
backend and no runtime services, so the attack surface is small. Still, if you
find a security issue — for example a vulnerable dependency, an XSS vector in a
component, or a supply-chain concern — we'd like to hear about it.

**Please report privately** to **bitjaru0402@naver.com** rather than opening a
public issue. Include:

- A description of the issue and where it is (file/component)
- Steps to reproduce, if applicable
- The version / commit you found it on

We aim to acknowledge reports within a few days and will credit you (if you
want) once a fix ships.

## Supported Versions

The latest release on `main` is the supported version. Security fixes land
there first; older tags are not separately patched.

## Scope

In scope: the published components, skills, scaffold, and dependencies in this
repo. Out of scope: third-party deployments of StyleSeed and projects that have
copied/modified the engine.
