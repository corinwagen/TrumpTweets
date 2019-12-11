# usage: bash batch_submit.sh

for i in {1..2000}
do
    sed s/@NUM/$i/g submit.sh > submit_model_${i}.sh
    sbatch submit_model_${i}.sh
    echo "submitted model $i"
    rm submit_model_${i}.sh
done
