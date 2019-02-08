echo "compile - multiply"
./compile.py multiply
echo

echo "compile - sort"
./compile.py sort
echo

echo "run - multiply"
./run.py multiply c_long 2 2
echo

echo "run - sort"
./run.py sort c_mergesort 3 1 2
echo

echo "time - multiply"
./time.py multiply 1 2 2
echo

echo "time - sort"
./time.py sort 1 random 10
echo