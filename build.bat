FN=build.sh

if [[ $0 == "$PWD/repository.circero" ]]; then
	exit
fi

while [[ $PWD != "/" ]]; do
	if [[ -f "$PWD/$FN" ]]; then
		bash "$PWD/$FN" $1
		exit
	else
		cd ..
	fi
done