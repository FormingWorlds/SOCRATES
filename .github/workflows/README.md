The build workflow compiles the code and makes the zip file in the [Action artifacts](https://github.com/FormingWorlds/SOCRATES/actions). Any push to the master branch will trigger the workflow to compile the code

How to make a release:

1. Tag a version of the code, e.g. `git tag 1.0.0`
2. Push the tag, `git push origin tag 1.0.0`
3. The [action-gh-release action](https://github.com/softprops/action-gh-release) detects a tagged commit and makes a [release](https://github.com/FormingWorlds/SOCRATES/releases)
4. The release contains a zip file with the compiled code
5. Update the release notes if necessary
