for i in {3..100} 
do

    mv MaSimCyc_$i/monthly_data_0.txt 1-Monthly\ Data/monthly_cyc_$i.txt
    mv MaSimCyc_$i/mut_arrival.txt 2-Mutation\ Pair/mutpair_cyc_$i.txt
    mv MaSimCyc_$i/summary_0.txt 3-Summary\ Data/summary_cyc_$i.txt

done