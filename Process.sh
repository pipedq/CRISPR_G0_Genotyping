for i in {1..33}
do
bowtie2 --local --threads 10  --rdg 3,1 -x Ref_Seq_index -1 ${i}_R1_001.fastq.gz -2 ${i}_R2_001.fastq.gz -S ${i}.sam
samtools view  -Sbo ${i}.bam ${i}.sam
samtools view -h -f 2 -F 4 ${i}.bam > ${i}_proper_map
samtools sort -n -o ${i}_proper_map_namesorted.bam ${i}_proper_map
samtools view ${i}_proper_map_namesorted.bam | awk '$0!~/^@/ {key=$0; getline; print key "}" $0;next}{print $0}'> collapsed.sam
awk '$0!~/XS:i:/' collapsed.sam > filtered_collapsed.sam
awk '{n=split($0,a,"}"); for (i = 1; i <= n; ++i) print a[i]}'  filtered_collapsed.sam > filtered_unique.sam
samtools view -h ${i}.sam | head -3 > header
cat header filtered_unique.sam >  jointed.sam
samtools view  -Sbo ${i}_clean.bam jointed.sam
samtools sort -o ${i}_sorted.bam ${i}_clean.bam
samtools index  ${i}_sorted.bam
samtools mpileup -B -d 0 -Q 30 -f Ref_Seq.fa -o ${i}_mpileup ${i}_sorted.bam
done

rm header filtered_unique.sam jointed.sam collapsed.sam filtered_collapsed.sam