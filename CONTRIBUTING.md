# Contributing guidelines

The guidelines on this page are written in the context of the PROTEUS planetary evolution framework. This distribution of SOCRATES is considered a submodule of the PROTEUS framework. This page provides an overview on contributing to PROTEUS itself and the ecosystem. Anyone who makes a Pull Request to the `main` branch should read this document *fully* first.

## Licensing and credit

PROTEUS and its submodules are *free* software and also *open source* software. Roughly, this means that the users have the freedom to run, copy, distribute, study, change and improve the software. The term "free software" is a matter of liberty, not price or monetary value [[ref]](https://www.gnu.org/philosophy/free-sw.html).

The principle purpose of PROTEUS and its submodules is to generate data to make scientific conclusions and write papers. It is generally expected that the primary author of a paper is the person who contributed the most work to that project. We ask that:

1. authorship is offered to the Contributors to PROTEUS based on the relevance of their work in a paper,
2. appropriate credit is provided in the Acknowledgements section of the paper,
3. the Maintainers are made aware of when PROTEUS results are used in a scientific paper.

A suggested acknowledgement is:
> We thank the people who have contributed to PROTEUS and its broader ecosystem for their support and enabling the scientific outputs of this paper. PROTEUS (version XX.XX.XX) may be found online at https://github.com/FormingWorlds

<b>
In summary:

* you generally own all of the code you write and material you create,
* you give irrevocable permission for the code to be used under the license when distributed,
* you are requested to offer authorship and give credit in papers as appropriate.
</b>

PROTEUS would not exist without the efforts of the wider community. Contributions from research scientists, software developers, students, and many others have made development of the current framework possible. Thank you for your interest in contributing, and the immense task of simulating the lifetimes of entire planets and stars.

"Alone we can do do so little; together we can do so much." - Helen Keller

## How do I contribute?

Contributing is relatively straightforward. We use Git to manage the source code, and GitHub to host it online. Here is a simple workflow:

1. Download the code and make sure that it runs on your machine
2. Create a new 'branch' called `MY_BRANCH` using Git: `git checkout -b MY_BRANCH`
3. Make changes to the code as you so desire
4. Add these changes to the repository: `git add .`
5. Commit these changes with a message: `git commit -m MESSAGE`
6. Push these changes to GitHub: `git push -u origin MY_BRANCH`
7. When you've got a neat set of changes, make a 'pull request' on GitHub [here](https://github.com/FormingWorlds/SOCRATES/pulls). This makes you a Contributor to the project.
8. One of the Maintainers of the project will review the request.
9. When ready, the changes will be merged into the `main` branch and are made live!

A series of 'hooks' will check the syntax and validity of your code when committing. With a significant number of people contributing to the codebase, automatic checks are important for preventing programming errors, bugs, stylistic problems, and large files from being committed to the repositories [[ref]](https://en.wikipedia.org/wiki/Lint_(software)).

Currently, the Maintainers of the code are: Harrison Nicholls and Tim Lichtenberg.

## Development rules

### Versioning

We target Python version 3.12 and is not intended to work on earlier versions of Python.
We also target Linux and MacOS as the *only* supported operating systems. Windows and BSD are not supported.

### Large files, output, and input data

Large files should **not** be committed to the repository. This means that model results, plots, and files you create during analysis should not be be staged and committed to an online branch. Including these (even accidentally) in the repository will make Git operations sluggish and make version control tricky, as Git is only meant for managing text (e.g. code) files.

You can make files/folders invisible to Git by prepending `nogit_` to their names. For example, anything in a folder called `nogit_analysis/` will be ignored by Git. Large files could then be safely placed in this folder. Model outputs are generated in the `output/` folder, which is also ignored by Git.
