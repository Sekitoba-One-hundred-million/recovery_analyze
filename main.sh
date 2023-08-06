dir='common'
file_list=`ls analyze`
write_file_name="$dir/name.py"
list_file="$dir/list.txt"
re_dir="recovery_score"
us_dir="users_score"
learn_dir="learn"
genetic_dir="genetic"
money_test_dir="money_test"

echo "1: name update"
echo "2: recovery_score update"
echo "3: users_score update"
echo "4: GA start"
echo "5: money test start"

tag=""
read -p "Enter 1,2,3,4,5 > " tag

if [ !$tag = "1" ] && [ !$tag = "2" ] && [ !$tag = "3" ] && [ !$tag = "4" ] && [ !$tag = "5" ]; then
    echo "Wrong number"
    exit 1
fi

rm -rf $dir
mkdir $dir
echo 'class Name:' >> $write_file_name
echo '    def __init__( self ):' >> $write_file_name
    
for file_name in $file_list; do
    base='        self.'
    ARR=(${file_name//./ })
    name=${ARR[0]}
    minus_name=${name}_minus
    # echo $file_name
    echo "$base$name = \"$name\"" >> $write_file_name
    echo "$base$minus_name = \"$minus_name\"" >> $write_file_name
    echo $name >> $list_file
    echo $minus_name >> $list_file
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
    python $money_test_dir/main.py
fi

rm -rf storage
