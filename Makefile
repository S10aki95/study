ABSOLUTE_PATH := $(shell pwd)
GIT_PATH = https://github.com/shibuiwilliam/ml-system-in-actions

# 環境構築用
# makeコマンドのインストール
# sudo apt install -y make


.PHONY: dev
dev:
	@echo '---------------go updating---------------------'
	# アップデート
	sudo apt update
	sudo apt upgrade

	mkdir tmp/
	git clone $(GIT_PATH) tmp/

	# linuxのライブラリをインストール
	sudo apt install -y build-essential libffi-dev libssl-dev zlib1g-dev \
	liblzma-dev libbz2-dev libreadline-dev libsqlite3-dev libopencv-dev tk-dev

	# pyenv本体のダウンロードとインストール
	git clone https://github.com/pyenv/pyenv.git ~/.pyenv

	# .bashrcの更新
	echo 'export PYENV_ROOT="$(HOME)/.pyenv"' >> ~/.bashrc
	echo 'export PATH="$(PYENV_ROOT)/bin:$(PATH))"' >> ~/.bashrc
	echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
	. $(HOME)/.bashrc

	# 2021/02時点最新のanaconda環境を選択
	pyenv install anaconda3-5.3.1

	# Docker インストール前に削除
	#sudo apt-get update
		
	# docker に必要なインストール
	sudo apt-get install ca-certificates curl gnupg lsb-release
	
	# gpg keyの作成
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

	# aptレポジトリに追加
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
	$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


	# Docker Engine他の一式のインストール
	sudo apt-get install docker-ce docker-ce-cli containerd.io

	# ログインしているユーザーをdockerグループへ追加。
	sudo gpasswd -a $(whoami) docker

	# 次にdocker.sock にグループでの書き込み権限を付与。
	sudo chgrp docker /var/run/docker.sock

	# 最後にdocker daemonを再起動します。
	sudo service docker restart

.PHONY: clean
clean:
	rm -rf tmp
	sudo apt-get remove docker docker-engine docker.io containerd runc