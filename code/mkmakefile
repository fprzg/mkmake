#! /bin/python3

help_str = '''.PHONY: help
## help: print this help message
help:
	@echo 'Usage'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'
'''


confirm_str = '''.PHONY: confirm
confirm:
	echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y]
'''

print(help_str)
print(confirm_str)
