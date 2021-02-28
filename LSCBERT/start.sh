CURRENT_DIR=`pwd`
export SQUAD_DIR=$CURRENT_DIR/data

python run_squad.py \
  --model_type albert \
  --model_name_or_path wptoux/albert-chinese-large-qa \
  --do_train \
  --do_eval \
  --do_lower_case \
  --train_file $SQUAD_DIR/DRCD_training.json \
  --predict_file $SQUAD_DIR/DRCD_dev.json \
  --per_gpu_train_batch_size 6 \
  --per_gpu_eval_batch_size 6 \
  --learning_rate 1e-5 \
  --num_train_epochs 2.0 \
  --warmup_steps 1000 \
  --max_seq_length 512 \
  --max_query_length 50 \
  --max_answer_length 300 \
  --doc_stride 256 \
  --output_dir output_DRCD_albert \
  --save_steps 10000