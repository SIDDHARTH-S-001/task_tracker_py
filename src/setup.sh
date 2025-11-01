export main_file_path=$(pwd)
cd $main_file_path
chmod +x main.py
cp main.py task-cli
chmod +x task-cli
echo "export PATH=\"\$PATH:$main_file_path\"" >> ~/.bashrc
bash