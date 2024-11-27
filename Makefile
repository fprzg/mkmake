.PHONY: install
install_dir=${HOME}/.local/bin

install:
	@[ -d ${install_dir} ] || mkdir -p ${install_dir}
	@cp ./code/mkmakefile ${install_dir}
	@chmod 0744 ${install_dir}/mkmakefile
