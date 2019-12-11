# usage: bash batch_submit.sh

for i in {1..500}
do
    sed s/@NUM/$i/g submit_au.sh > submit_model_${i}.sh
    sed s/@NUM/$i/g model_461.json > rub_model_${i}.json
    sbatch submit_model_${i}.sh
    echo "submitted model $i"
    rm submit_model_${i}.sh
done
