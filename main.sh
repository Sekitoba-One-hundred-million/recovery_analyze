dir='common'
file_list=`ls analyze`
write_file_name="$dir/name.py"
list_file="$dir/list.txt"

rm -rf $dir
mkdir $dir
echo 'class Name:' >> $write_file_name
echo '    def __init__( self ):' >> $write_file_name

for file_name in $file_list; do
    base='        self.'
    ARR=(${file_name//./ })
    name=${ARR[0]}
    # echo $file_name
    echo "$base$name = \"$name\"" >> $write_file_name
    echo $name >> $list_file
done

re_dir="recovery_score"
us_dir="users_score"

cp -r $dir $re_dir/
cp -r $dir $us_dir/

python $re_dir/main.py
python $us_dir/main.py
