#! /bin/python3

import argparse
import re
import sys

class NameFieldNotIncludedError(Exception):
	"""Exception thrown when MakefileRule.from_str is called without a NAME parameter"""
	def __init__(self, message="Cannot create a MakefileRule without a name"):
		super().__init__(message)

class MakefileRule:
	phony = True

	def __init__(self, name, phony=True, description=None, requires=[], recipe=[]):
		self.name = name
		self.phony = phony
		self.description = description
		self.requires = requires
		self.recipe = recipe

	def __str__(self) -> str:
		as_str = ""
		if self.description != None:
			as_str += f"## {self.name}: {self.description}\n"
		if self.phony:
			as_str += f".PHONY: {self.name}\n"
		as_str += f"{self.name}: {' '.join(req for req in self.requires)}\n"
		as_str += ''.join(f"\t{step}\n" for step in self.recipe)
		return as_str

	@classmethod
	def from_dict(cls, rule_dict):
		if rule_dict["NAME"] == None:
			raise NameFieldNotIncludedError

		return cls(rule_dict["NAME"],
			phony=rule_dict["PHONY"],
			description=rule_dict["DESC"],
			requires=rule_dict["REQ"],
			recipe=rule_dict["STEP"])

	@classmethod
	def from_str(cls, rule_str):
		keywords = [ "PHONY", "NAME", "DESC", "REQ", "STEP"]
		keywords_str = rf"{ '|'.join(re.escape(k) for k in keywords) }"
		pattern = re.compile(rf"({keywords_str})\s(.*?)(?=(?:{keywords_str})|$)")

		matches = pattern.findall(rule_str)

		rule_dict = {
			"PHONY": False,
			"NAME": None,
			"DESC": None,
			"REQ": [],
			"STEP": [],
		}

		for match in matches:
			keyword, content = match
			content = content.strip()

			match keyword:
				case "PHONY":
					rule_dict[keyword] = True
				case "NAME":
					if content == "" or content == None:
						raise NameFieldNotIncludedError
					rule_dict[keyword] = content
				case "DESC":
					rule_dict[keyword] = content
				case "REQ" | "STEP":
					rule_dict[keyword].append(content)

		return  cls.from_dict(rule_dict)

	@classmethod
	def from_params(cls, name, phony=None, description=None, requires=[], recipe=[]):
		return cls(name,
			phony=phony if phony != None else cls.phony,
			description=description,
			requires=requires,
			recipe=recipe)

	@classmethod
	def disable_phony(cls):
		cls.phony = False

	@classmethod
	def enable_phony(cls):
		cls.phony = True


class MakefileRuleList:
	def __init__(self):
		self.rules = {}

	def add_rule(self, new_rule):
		self.rules[new_rule.name] = new_rule

	def add_rule_str(self, new_rule_str):
		new_rule = MakefileRule.from_str(new_rule_str)
		self.rules[new_rule.name] = new_rule

	def __str__(self) -> str:
		return '\n\n'.join(str(rule) for name, rule in self.rules.items())


def main():
	parser = argparse.ArgumentParser(
		prog='mkmake',
		description='Utility for automated Makefile creation.'
	)

	parser.add_argument('-p', '--disable-phony', action='store_true', help='prevent rules from being added to .PHONY.')
	parser.add_argument('-d', '--add-default-rules', action='store_true', help='add \'help\' and \'confirm\'.')
	parser.add_argument('-P', '--print', action='store_true', help='print to string instead of Makefile.')
	parser.add_argument('-O', '--overwrite', action='store_true', help='overwrite Makefile.')
	parser.add_argument('rules', nargs='*', help='list of rules.')
	args = parser.parse_args()

	rules = MakefileRuleList()
	if args.disable_phony:
		MakefileRule.disable_phony()

	if not args.add_default_rules and len(args.rules) == 0:
		parser.print_help()
		sys.exit(1)

	if args.add_default_rules:
		rules.add_rule(MakefileRule.from_params('help', description='shows this message.', recipe=["@echo 'Usage'", "@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'" ]))
		rules.add_rule(MakefileRule.from_params('confirm', description='asks the user for confirmation.', recipe=["@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]"]))

	for rule in args.rules:
		try:
			rules.add_rule_str(rule)
		except NameFieldNotIncludedError as e:
			print(f"Error: '{e}' with rule '{rule}'.")
			sys.exit(1)
	
	if args.print:
		print(rules)
	else:
		mode = 'a' if not args.overwrite else 'w'
		with open('Makefile', mode) as f:
			print(rules, file=f)


if __name__ == "__main__":
	main()
