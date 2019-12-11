# usage - awk -f 'extract_performance.awk' model_info.txt model_performance.txt > model_info.csv

# inputs generated with:
# $ grep "model_name" results/*/results.txt > bond_models.txt
# $ grep -o -P "Performance.*$" results/*/results.txt > bond_performance.txt

FNR==NR{
    model = $2
    predictor = $4
    aug_num = $8
    aug_size = $10
    lookback = $17
    dropout = $20
    type = $26

    gsub("'","", model)
    gsub(",","", model)

    gsub("^.*/","", predictor)
    gsub("'","", predictor)
    gsub(",","", predictor)

    gsub(",","", aug_num)
    
    gsub(",","", aug_size)
    gsub("}","", aug_size)
    
    gsub(",","", lookback)
    gsub("}","", lookback)
    
    gsub(",","", dropout)
    
    gsub(",","", type)
    gsub("}","", type)
    gsub("'","", type)
    
    if (type == "regressor")
        a[model] = sprintf("%s;%s;%s;%s;%s;%s;%s", model, predictor, aug_num, aug_size, lookback, dropout, type)
}

FNR!=NR{
    model = $1
    t = $3
    p = $5
    l = $11
    r_5 = $13
    r = $15
    r_95 = $17
    
    gsub(",","", t)
    gsub(",","", p)
    gsub(",","", l)
    gsub(",","", r_5)
    gsub(",","", r)
    gsub(",","", r_95)

    gsub("^[^/]*/","", model)
    gsub("/.*$", "", model)

    if (model in a)
        printf "%s;%s;%s;%s;%s;%s;%s\n", a[model], t, p, l, r_5, r, r_95
}
