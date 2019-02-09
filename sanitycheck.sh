echo "compile - multiply"
./compile.py multiply
echo

echo "compile - sort"
./compile.py sort
echo

echo "compile - inversion"
./compile.py inversion
echo

echo "run - multiply"
./run.py multiply c_long 2 2
echo

echo "run - sort"
./run.py sort c_mergesort 3 1 2
echo

echo "run - inversion"
./run.py inversion py_brute_force 3 1 2
echo

echo "time - multiply"
./time.py multiply 1 2 2
echo

echo "time - sort"
./time.py sort 1 random 10
echo

echo "time - inversion"
./time.py inversion 1 random 10
echo