floyd run --gpu \
          --data TcAbdhU7P5vkdzHyUwz9r7:train_data \
          --data nPqNCPMnr4ZyViqRN7vWp4:models \
          --env tensorflow:py2 \
          "python train_frcnn.py --path=annotations_simple.txt --input_weight_path=/models/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5 --num_epochs=14 --parser=simple"

# floyd status
# floyd logs AKpnXqj9BEU6d8KhmygTyb -t
