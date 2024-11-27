.PHONY: install
install_dir=${HOME}/.local/bin

install:
	@[ -d ${install_dir} ] || mkdir -p ${install_dir}
	@cp ./code/mkmake.py ${install_dir}/mkmake
	@chmod 0744 ${install_dir}/mkmake
