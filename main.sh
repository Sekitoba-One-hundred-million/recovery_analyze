dir='common'
list_file="$dir/list.txt"
file_list=`cat ${list_file}`
write_file_name="$dir/name.py"
re_dir="recovery_score"
us_dir="users_score"
learn_dir="learn"
genetic_dir="genetic"
money_test_dir="money_test"

tag=""

if [ $# -eq 1 ]; then
    tag=$1
fi

if [ !$tag = "1" ] && [ !$tag = "2" ] && [ !$tag = "3" ] && [ !$tag = "4" ]; then
    tag=""
fi

if [ -z $tag ]; then
    echo "1: name update"
    echo "2: recovery_score update"
    echo "3: users_score update"
    echo "4: GA start"
    echo "5: recovery and GA start"

    read -p "Enter 1,2,3,4,5 > " tag
fi

if [ !$tag = "1" ] && [ !$tag = "2" ] && [ !$tag = "3" ] && [ !$tag = "4" ] && [ !$tag = "5" ]; then
    echo "Wrong number"
    exit 1
fi

rm -rf ${write_file_name}
touch ${write_file_name}
echo 'class Name:' >> $write_file_name
echo '    def __init__( self ):' >> $write_file_name
    
for name in $file_list; do
    base='        self.'
    minus_name=${name}_minus
    # echo $file_name
    echo "$base$name = \"$name\"" >> $write_file_name
    echo "$base$minus_name = \"$minus_name\"" >> $write_file_name
done

cp -r $dir $re_dir/
cp -r $dir $us_dir/
cp -r $dir $learn_dir/
cp -r $dir $genetic_dir

if [ $tag = "2" ]; then
    cd /Users/kansei/ghq/github.com/Sekitoba-One-hundred-million/sekitoba_library; pip install .; cd /Users/kansei/ghq/github.com/Sekitoba-One-hundred-million/recovery_analyze
    mpiexec -n 6 python $re_dir/main.py
fi

if [ $tag = "3" ]; then
    python $us_dir/main.py
fi

if [ $tag = "4" ]; then
    python $genetic_dir/main.py
fi

if [ $tag = "5" ]; then
    cd /Users/kansei/ghq/github.com/Sekitoba-One-hundred-million/sekitoba_library; pip install .; cd /Users/kansei/ghq/github.com/Sekitoba-One-hundred-million/recovery_analyze
    mpiexec -n 6 python $re_dir/main.py
    python $genetic_dir/main.py
fi

rm -rf storage
