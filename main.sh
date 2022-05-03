dir='common'
file_list=`ls analyze`
write_file_name="$dir/name.py"
list_file="$dir/list.txt"

echo "1: all update"
echo "2: name update"
echo "3: recovery_score update"
echo "4: users_score update"

tag=""
read -p "Enter 1,2,3,4 > " tag

if [ ! $tag = "1" ] && [ ! $tag = "2" ] && [ ! $tag = "3" ] && [ ! $tag = "4" ]; then
    echo "Wrong number"
    #echo "Enter 1,2,3,4"
fi

if [ $tag = "1" ] || [ $tag = "2" ]; then 
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
fi

if [ $tag = "1" ] || [ $tag = "3" ]; then
    python $re_dir/main.py
fi

if [ $tag = "1" ] || [ $tag = "4" ]; then
    python $us_dir/main.py
fi
