# mkmake

Small utility for creating Makefile files.

## Installation
The script gets installed in **~/.local/bin**. If such directory doesn't exist, it gets created.
To install, run `make install` on the root of the directory of the git repository.

## Usage
There are a few keywords:
* `NAME the/rule/name`: Sets the name of the rule. If there's no name, it raises an error. If there's more than one name, also raises an error.
* `PHONY`: Adds the rule as `.PHONY`.
* `DESC the actual description`: Sets the description of the rule. Optional.
* `REQ another/rule`: If you want to execute another rule before the current one, you can add it here. You can add more than one rule, or none.
* `STEP echo "This is the step"`: You use this to add the steps of the recipe. You can add one, or none.

Default behavior is to append rules to an existing Makefile if there's one if $PWD. If there is not, it creates one. You can output to stdout with `-P` or overwrite the current Makefile with `-O`.

```bash
mkmake -dP "NAME update DESC Updates the system (super user privileges required) REQ confirm STEP @echo Updating system... STEP @sudo apt -y update && echo System updated"
```

outputs to stdout the following:

```Makefile
## help: shows this message.
.PHONY: help
help: 
	@echo 'Usage'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'


## confirm: asks the user for confirmation.
.PHONY: confirm
confirm: 
	@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]


## update: Updates the system (super user privileges required).
update: confirm
	@echo Updating system...
	@sudo apt -y update && echo System updated
```