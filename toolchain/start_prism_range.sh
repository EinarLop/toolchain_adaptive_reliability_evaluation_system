cd prism

for HOURS in {0..400000..1000}; do
    echo $HOURS `./bin/prism -importtrans ctmc/ctmc.tra -ctmc -pf "P=? [ F=$HOURS (x!=1) ]" | grep Result | awk '{print $2}'`
done

cd ..
